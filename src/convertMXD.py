import os
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
    """
    Check if file is a layer or a group layers and add its name to array of layer

    Args:
        fileName: File name to read
    """
    print fileName
    tree = ET.parse(msdZip.open(fileName))
    root = tree.getroot()

    # first, check if it is a group layer ('typens:CIMDEGroupLayer')
    # if so, extract layer name. If not, iterate items in Layers node to extract layer name.
    # We can have groups in group so we always need to check.
    layersNode = root.find('./Layers')
    if layersNode == None:
        layers.setLayer(root)
    else:
        for elem in layersNode.iter():
            if elem.text != None:
                loopLayers(elem.text.split('=')[1])

# set the MapServer folder
sections.setProjectFolderName(sys.argv[3])

# set variables to select an MXD file
mxdFileFolder = sys.argv[1]
mxdFilePath = sys.argv[1] + sys.argv[2]
mxdFileName =  sys.argv[2]

# get a reference to the Map Document
mxd = arcpy.mapping.MapDocument(mxdFilePath)

# create a map file with the same name of the MXD file, in the same folder
sections.createMapFile(mxdFileFolder + os.path.splitext(mxdFileName)[0] + '.map')

# convert to MSD (Map Service Definition)
# TODO: we need to have the right data source path. if not, we need to repair the link!
arcpy.mapping.ConvertToMSD(mxd, mxdFileFolder + os.path.splitext(mxdFileName)[0] + '.msd')
msdZip = zipfile.ZipFile(mxdFileFolder + os.path.splitext(mxdFileName)[0] + '.msd')

# add map section
# if data have the same name as the dataFrame, dataFrame will have a number suffix. We need to remove it from the path
docInfo = sections.getDocumentInfo(ET.parse(msdZip.open('DocumentInfo.xml')).getroot())
rootDataFrame = ET.parse(msdZip.open((docInfo['dataFrame'].split('.')[0].rstrip(string.digits)) + '/' + docInfo['dataFrame'])).getroot()
dataFrameInfo = sections.getDataframeInfo(rootDataFrame)
epsg = lookup.getEPSGFromWKID(rootDataFrame.findtext('./DefaultExtent/SpatialReference/WKID'))
sections.log('MAP')
sections.getMap(docInfo, dataFrameInfo, epsg)

# add layers section
layers.initLayers(epsg, sections.getProjectFolderName())
layersNode = rootDataFrame.find('./Layers')
for elem in layersNode.iter():
    if elem.text != None:
        loopLayers(elem.text.split('=')[1])

# add symbols section
symbArr = sb.getSymbols()
for symbol in symbArr:
    sections.log(symbol, 2, False)

sections.log('END # map')
sections.closeMapFile()

# clean
del msdZip
del mxd