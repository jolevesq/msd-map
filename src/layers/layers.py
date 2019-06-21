import os

# import msd - map modules
from symbols import symbols
from common import sections

epsg = None
msFolder = None

def initLayers(epsgCode, mapServerFolder):
    global epsg
    epsg = epsgCode
    global msFolder
    msFolder = mapServerFolder

def setLayer(root):
    name = root.find('./Name').text.replace(' ', '_')
    data = root.find('./FeatureTable/DataConnection/Dataset')

    data = data.text
    minScale = root.find('./MinScale').text
    maxScale = root.find('./MaxScale').text
    connection = root.find('./FeatureTable/DataConnection/WorkspaceConnectionString').text.replace('DATABASE=', '')
    geomType = sections.getLayerGeometry(root.find('./FeatureTable/FieldDescriptions'))
    sections.log('LAYER', 2)
    sections.log('NAME    "' + name + '"', 4, False)
    sections.log('DATA    "' + data + '"', 4, False)
    # log('MINSCALEDENOM   ' + minScale, 4)
    # log('MAXSCALEDENOM    ' + maxScale, 4)
    sections.log('STATUS    ON', 4)
    sections.log('CONNECTIONTYPE    OGR', 4)
    sections.log('CONNECTION    "./data/' + msFolder + '/' + os.path.basename(connection) + '"', 4, False)
    sections.log('TYPE    ' + geomType, 4)
    sections.log(sections.getLayerMetadata(name, epsg), 4, False)

    # symbology
    #if geomType == 'Line':
     #   sections.log(symbols.getSymbologyLine(root), 4, False)
    #elif geomType == 'Polygon':
    #    sections.log(symbols.getSymbologyPolygon(root), 4, False)
    #else:
    sections.log(symbols.getSymbology(root, geomType), 4, False)
    sections.log('END # layer', 2, False)
    sections.log(sections.getSeparator(), 2, False)