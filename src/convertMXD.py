import os, locale
import sys
import arcpy
import string
import zipfile
import xml.etree.ElementTree as ET

import lookupEPSG as EPSG
import commonSections as sections
import symbols

print 'Argument List:', str(sys.argv)

def log(txt, offset=0, upper=True):
    if upper:
        txt = txt.upper()
    
    file.write(' ' * offset + txt + '\n')

# the MapServer folder
mapServerFolder = sys.argv[3]

# set variables to select an MXD file
mxdFileFolder = sys.argv[1]
mxdFilePath = sys.argv[1] + sys.argv[2]
mxdFileName =  sys.argv[2]

# get local format for thousand separator
loc = locale.getlocale()

# get a reference to the Map Document
mxd = arcpy.mapping.MapDocument(mxdFilePath)

# create a map file with the same name of the MXD file, in the same folder
file = open(mxdFileFolder + os.path.splitext(mxdFileName)[0] + '.map', 'w')

# convert to MSD (Map Service Definition)
# TODO: !!!!!!!!!! we need to have the right data source path. if not, we need to repair the link !!!!!!!!!!
arcpy.mapping.ConvertToMSD(mxd, mxdFileFolder + os.path.splitext(mxdFileName)[0] + '.msd')
zz = zipfile.ZipFile(mxdFileFolder + os.path.splitext(mxdFileName)[0] + '.msd')


# get documentInfo
rootDocInfo = ET.parse(zz.open('DocumentInfo.xml')).getroot()
title = rootDocInfo.find('./DocumentTitle').text
abstract = rootDocInfo.find('./Subject').text
keywords = rootDocInfo.find('./Keywords').text.replace(' ', '')
dataFrame = os.path.basename(rootDocInfo.find('./ActiveMapRepositoryPath').text)

# get dataFrameInfo
# if data have the same name as the dataFrame, dataFrame will have a number suffix.
# We need to remove it from the path.
rootDataFrame = ET.parse(zz.open((dataFrame.split('.')[0].rstrip(string.digits)) + '/' + dataFrame)).getroot()

name = rootDataFrame.find('./Name').text.replace(' ', '_')
ext = [rootDataFrame.find('./DefaultExtent/XMin').text,
    rootDataFrame.find('./DefaultExtent/YMin').text,
    rootDataFrame.find('./DefaultExtent/XMax').text,
    rootDataFrame.find('./DefaultExtent/YMax').text]

layersNode = rootDataFrame.find('./Layers')
layers = []
for elem in layersNode.iter():
    if elem.text != None:
        layers.append(elem.text.split('=')[1])

log('MAP')

log('NAME            "{name}"'.format(name=name), 2)
log(sections.getMapCommon(), 2, False)
log(sections.getExtent(ext), 2, False)
log(sections.getSize(), 2, False)
log(sections.getUnits() + '\n', 2, False)

log(sections.getPng(), 2, False)
log(sections.getGif(), 2, False)
log(sections.getJpeg(), 2, False)

log(sections.getScale(), 2, False)
log(sections.getLegend(), 2, False)

epsg = EPSG.getCodeFromWKID(rootDataFrame.find('./DefaultExtent/SpatialReference/WKID').text)
log(sections.getProjection(epsg), 2, False)

log(sections.getWeb(title, abstract, keywords), 2, False)

log(sections.getSeparator(), 2, False)

for fileName in layers:
    tree = ET.parse(zz.open(fileName))
    root = tree.getroot()

    name = root.find('./Name').text.replace(' ', '_')
    data = root.find('./FeatureTable/DataConnection/Dataset').text
    minScale = root.find('./MinScale').text
    maxScale = root.find('./MaxScale').text
    connection = root.find('./FeatureTable/DataConnection/WorkspaceConnectionString').text.replace('DATABASE=', '')
    geomType = sections.getLayerGeometry(root.find('./FeatureTable/FieldDescriptions'))

    log('LAYER', 2)
    log('NAME    "' + name + '"', 4, False)
    log('DATA    "' + data + '"', 4, False)
    # log('MINSCALEDENOM   ' + minScale, 4)
    # log('MAXSCALEDENOM    ' + maxScale, 4)
    log('STATUS    ON', 4)
    log('CONNECTIONTYPE    OGR', 4)
    log('CONNECTION    "./data/' + mapServerFolder + '/' + os.path.basename(connection) + '"', 4, False)
    log('TYPE    ' + geomType, 4)
    log(sections.getLayerMetadata(name, epsg), 4, False)

    # symbology
    if geomType == 'Line':
        log(symbols.getSymbologyLine(root), 4, False)
    elif geomType == 'Polygon':
        log(symbols.getSymbologyPolygon(root), 4, False)
    else:
        log(symbols.getSymbologyPoint(root), 4, False)

    # if geomType == 'Point':
    #     # outline
    #     colorR = root.find('./Symbolizer/Symbol/Symbol/SymbolLayers/CIMSymbolLayer/OutlineColor/R').text
    #     colorG = root.find('./Symbolizer/Symbol/Symbol/SymbolLayers/CIMSymbolLayer/OutlineColor/G').text
    #     colorB = root.find('./Symbolizer/Symbol/Symbol/SymbolLayers/CIMSymbolLayer/OutlineColor/B').text
    #     width = root.find('./Symbolizer/Symbol/Symbol/SymbolLayers/CIMSymbolLayer/OutlineWidth').text

    #     # fill
    #     fillR = root.find('./Symbolizer/Symbol/Symbol/SymbolLayers/CIMSymbolLayer/FillColor/R').text
    #     fillG = root.find('./Symbolizer/Symbol/Symbol/SymbolLayers/CIMSymbolLayer/FillColor/G').text
    #     fillB = root.find('./Symbolizer/Symbol/Symbol/SymbolLayers/CIMSymbolLayer/FillColor/B').text

    #     # size
    #     size = root.find('./Symbolizer/Symbol/Symbol/SymbolLayers/CIMSymbolLayer/Size').text

    #     log(sections.getPointStyle(fillR + ' ' +fillG + ' ' + fillB, size), 4, False)

    log('END # layer', 2, False)

    log(sections.getSeparator(), 2, False)

log('END # map')
file.close()

del zz
del mxd

openNotepad = 'true'
if openNotepad == 'true':
    # open TXT file with Notepad or other program with which txt extension is associated with
    os.startfile(file.name)