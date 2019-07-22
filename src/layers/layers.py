import os

# import msd - map modules
from symbols import symbols
from common import sections

epsg = None
msFolder = None

def initLayers(epsgCode, mapServerFolder):
    """
    Initialize the global variables for layers creation 

    Args:
        epsgCode: EOSG code
        mapServerFolder: MapServer folder to use for this layer
    """
    global epsg
    epsg = epsgCode
    global msFolder
    msFolder = mapServerFolder

def setLayer(root):
    """
    Write layer section

    Args:
        root: Root xml node for the layer file
    """

    # main section
    name = root.findtext('./Name').replace(' ', '_')
    data = root.findtext('./FeatureTable/DataConnection/Dataset')
    minScale = root.findtext('./MinScale')
    maxScale = root.findtext('./MaxScale')
    connection = root.findtext('./FeatureTable/DataConnection/WorkspaceConnectionString').replace('DATABASE=', '')
    geomType = sections.getLayerGeometry(root.find('./FeatureTable/FieldDescriptions'))
    sections.log('LAYER', 2)
    sections.log('NAME    "' + name + '"', 4, False)
    sections.log('DATA    "' + data + '"', 4, False)
    sections.log('MINSCALEDENOM   ' + minScale, 4)
    sections.log('MAXSCALEDENOM    ' + maxScale, 4)
    sections.log('STATUS    ON', 4)
    sections.log('CONNECTIONTYPE    OGR', 4)
    sections.log('CONNECTION    "./data/' + msFolder + '/' + os.path.basename(connection) + '"', 4, False)
    sections.log('TYPE    ' + geomType, 4)
    sections.log(sections.getLayerMetadata(name, epsg), 4, False)

    # symbology
    sections.log(symbols.getSymbology(root, geomType), 4, False)
    sections.log('END # layer', 2, False)
    sections.log(sections.getSeparator(), 2, False)