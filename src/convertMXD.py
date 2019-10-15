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
from common import trace

print 'Argument List:', str(sys.argv)
def loopLayers(fileName,  layersArray):
    """
    Check if file is a layer or a group layers and add its name to array of layer

    Args:
        fileName: File name to read
        layersArray: Arrays of layers object

    Returns:
        layersArray: Layers array .(will reverse to have the right order in the map file)
    """
    tree = ET.parse(msdZip.open(fileName))
    root = tree.getroot()

    # first, check if it is a group layer ('typens:CIMDEGroupLayer')
    # if so, extract layer name. If not, iterate items in Layers node to extract layer name.
    # We can have groups in group so we always need to check.
    layersNode = root.find('./Layers')
    if layersNode == None:
        layersArray.append(root)
    else:
        for elem in layersNode.iter():
            if elem.text != None:
                loopLayers(elem.text.split('=')[1], layersArray)

    return layersArray

# set the MapServer folder
sections.setProjectFolderName(sys.argv[3])

# set variables to select an MXD file
mxdFileFolder = sys.argv[1]
mxdFilePath = sys.argv[1] + sys.argv[2]
mxdFileName =  sys.argv[2]
mxdName = os.path.splitext(mxdFileName)[0]

try:
    # create trace file
    trace.create(mxdFileFolder + mxdName + '_trace.txt')

    # get a reference to the Map Document
    mxd = arcpy.mapping.MapDocument(mxdFilePath)

    # shorten layer names over 56 characters and uncompress FGDB data
    layersMXD = arcpy.mapping.ListLayers(mxd)
    for lyr in layersMXD:
        if lyr.supports('workspacePath'):
            sourcedata = lyr.workspacePath

        if len(lyr.name) > 56:
            truncName = lyr.name
            lyr.name = lyr.name[:56]
            trace.log('WARNING: The name of the layer \"' + truncName + '\" is too long and has been truncated to \"' + lyr.name + '\"')
    arcpy.RefreshTOC()
    if sourcedata[-4:] == '.gdb':
        arcpy.UncompressFileGeodatabaseData_management(sourcedata)

    # create a map file with the same name of the MXD file, in the same folder
    sections.createMapFile(mxdFileFolder + mxdName + '.map')

    # convert to MSD (Map Service Definition)
    # TODO: we need to have the right data source path. if not, we need to repair the link
    arcpy.mapping.ConvertToMSD(mxd, mxdFileFolder + mxdName + '.msd')
    msdZip = zipfile.ZipFile(mxdFileFolder + mxdName + '.msd')

    # add map section
    # if data have the same name as the dataFrame, dataFrame will have a number suffix. We need to remove it from the path
    docInfo = sections.getDocumentInfo(ET.parse(msdZip.open('DocumentInfo.xml')).getroot())
    rootDataFrame = ET.parse(msdZip.open((docInfo['dataFrame'].split('.')[0].rstrip(string.digits)) + '/' + docInfo['dataFrame'])).getroot()
    dataFrameInfo = sections.getDataframeInfo(rootDataFrame)
    epsg = lookup.getEPSGFromWKID(rootDataFrame.findtext('./DefaultExtent/SpatialReference/WKID'))
    sections.log('MAP')
    sections.getMap(docInfo, dataFrameInfo, epsg)

    # create array of layers. We need to create an array then reverse it because the map file is the opposite order then the mxd
    layers.initLayers(epsg, sections.getProjectFolderName())
    layersNode = rootDataFrame.find('./Layers')
    layersArray = []
    for elem in layersNode.iter():
        if elem.text != None:
            layersArray += loopLayers(elem.text.split('=')[1], [])

    # get array of visible layers with their opacity value (use dataframe to know visibility and opacity)
    display = dataFrameInfo['display']
    display = [a for a in display if a['visibility'] == 'true']

     # add layers section
    layersArray.reverse()
    layersName = []
    for item in layersArray:
        layersName.append(layers.setLayer(item, display))

    # add symbols section
    symbArr = sb.getSymbols()
    for symbol in symbArr:
        sections.log(symbol, 2, False)

    sections.log('END # map')

    # add url to use for testing to track
    trace.setSampleUrl(mxdName + '.map', ','.join([a for a in layersName if a != '']))

except Exception as e:
    message = 'Failed to create map file: ' + str(e)
    print message
    trace.log(message)

finally:
    sections.closeMapFile()
    trace.close()
    print 'End of Map file creation'

    # clean
    del msdZip
    del mxd