import os, locale
import sys
import string
import zipfile

# import xml tree navigation module
import xml.etree.ElementTree as ET

# import arcPy (ESRI) module
import arcpy

# import msd - map modules
from symbols import symbols
from symbols import utils as sb
from layers import layers 
from common import lookup
from common import sections

print 'Argument List:', str(sys.argv)

def loopLayers(fileName):
    print fileName
    tree = ET.parse(zz.open(fileName))
    root = tree.getroot()

    # first, check if it is a group layer ('typens:CIMDEGroupLayer')
    # If so, extract layer name. We can have groups in group so we always need to check.
    layersNode = root.find('./Layers')
    if layersNode == None:
        layers.setLayer(root)
    else:
        for elem in layersNode.iter():
            if elem.text != None:
                loopLayers(elem.text.split('=')[1])

# the MapServer folder
sections.setProjectFolderName(sys.argv[3])

# set variables to select an MXD file
mxdFileFolder = sys.argv[1]
mxdFilePath = sys.argv[1] + sys.argv[2]
mxdFileName =  sys.argv[2]

# get local format for thousand separator
loc = locale.getlocale()

# get a reference to the Map Document
mxd = arcpy.mapping.MapDocument(mxdFilePath)

# create a map file with the same name of the MXD file, in the same folder
sections.createLog(mxdFileFolder + os.path.splitext(mxdFileName)[0] + '.map')

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

sections.log('MAP')

sections.log('NAME            "{name}"'.format(name=name), 2)
sections.log(sections.getMapCommon(), 2, False)
sections.log(sections.getExtent(ext), 2, False)
sections.log(sections.getSize(), 2, False)
sections.log(sections.getUnits() + '\n', 2, False)

sections.log(sections.getPng(), 2, False)
sections.log(sections.getGif(), 2, False)
sections.log(sections.getJpeg(), 2, False)

sections.log(sections.getScale(), 2, False)
sections.log(sections.getLegend(), 2, False)

epsg = lookup.getEPSGFromWKID(rootDataFrame.find('./DefaultExtent/SpatialReference/WKID').text)
sections.log(sections.getProjection(epsg), 2, False)

sections.log(sections.getWeb(title, abstract, keywords), 2, False)

sections.log(sections.getSeparator(), 2, False)

# add layers
layers.initLayers(epsg, sections.getProjectFolderName())
layersNode = rootDataFrame.find('./Layers')
for elem in layersNode.iter():
    if elem.text != None:
        loopLayers(elem.text.split('=')[1])

# add symbols
symbArr = sb.getSymbols()
for symbol in symbArr:
    sections.log(symbol, 2, False)

sections.log('END # map')
sections.closeLog()

# clean
del zz
del mxd