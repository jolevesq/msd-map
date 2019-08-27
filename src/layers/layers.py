import os

# import msd - map modules
from symbols import symbols
from common import sections
from common import trace

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

def setLayer(root, displayArray):
    """
    Write layer section

    Args:
        root: Root xml node for the layer file
        displayArray: Information abour how to display the layer (visibility and transparency)

    Returns:
        name: Name of added layer if found empty string otherwise
    """
    subs = { ' ': '_', ',': '_', '/': '_', '(': '_', ')': '_', '\\': '_', '[': '_', ']': '_' }
    name = sections.replace(root.findtext('./Name'), subs)

    # check if we have a match between array of layers and the one who should be displayed
    found = [a for a in displayArray if a['layer'].capitalize() == name.capitalize()]

    if len(found) == 1:
        print name

        # main section
        data = root.findtext('./FeatureTable/DataConnection/Dataset')
        minScale = root.findtext('./MinScale')
        maxScale = root.findtext('./MaxScale')
        connection = root.findtext('./FeatureTable/DataConnection/WorkspaceConnectionString').replace('DATABASE=', '')
        geomType = sections.getLayerGeometry(root.find('./FeatureTable/FieldDescriptions'))
        sections.log('LAYER', 2)
        sections.log('NAME    "' + name + '"', 4, False)
        sections.log('DATA    "' + data + '"', 4, False)
        sections.log('MINSCALEDENOM   ' + maxScale, 4) # reverse from mxd
        sections.log('MAXSCALEDENOM    ' + minScale, 4) # reverse from mxd
        sections.log('OPACITY    ' + str(100 - int(found[0]['transparency'])), 4)
        sections.log('STATUS    ON', 4)
        sections.log('CONNECTIONTYPE    OGR', 4)
        sections.log('CONNECTION    "./data/' + msFolder + '/' + os.path.basename(connection) + '"', 4, False)
        sections.log('TYPE    ' + geomType, 4)
        sections.log(sections.getLayerMetadata(name, epsg), 4, False)

        trace.log('\n***---------------------***\nAdd layer *** ' + name + ' *** to map file')
        trace.log('Geometry type: ' + geomType)

        # symbology
        sections.log(symbols.getSymbology(root, geomType), 4, False)
        sections.log('END # layer', 2, False)
        sections.log(sections.getSeparator(), 2, False)

        trace.log('***---------------------***')
    else:
        trace.log('***---------------------***\nLayer not visible in mxd *** ' + name + ' ***\n***---------------------***')
        name = ''

    return name