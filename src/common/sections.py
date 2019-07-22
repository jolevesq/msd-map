import os

# global variable for map file and project name
mapFile = None
projectName = ''

def createMapFile(path):
    """
    Create map file

    Args:
        path: Path for the map file
    """
    global mapFile
    mapFile = open(path, 'w')

def closeMapFile():
    """
    Close map file
    """
    global mapFile
    mapFile.close()

def log(txt, offset=0, upper=True):
    """
    Add to map file

    Args:
        txt: Text to add
        offset: Spaces to add (optional, default 0)
        upper: capitalize the text (optional, default true)
    """
    if upper:
        txt = txt.upper()
    
    mapFile.write(' ' * offset + txt + '\n')

def setProjectFolderName(name):
    """
    Set the project folder name

    Args:
        name: Project folder name
    """
    global projectName
    projectName = name

def getProjectFolderName():
    """
    Get project folder name

    Returns:
        projectName: The project folder name
    """
    global projectName

    return projectName

def getMapCommon():
    """
    Get common section for symbol set, font set and image type

    Returns:
        common: The section
    """
    common = """SYMBOLSET       "./etc/symbols.sym"
  FONTSET         "./etc/fonts/fonts.list"
  IMAGETYPE       "png"
  """

    return common

def getPng():
    """
    Get png output section

    Returns:
        output: The png section
    """
    output = """OUTPUTFORMAT
    NAME          "png"
    DRIVER        "AGG/PNG"
    MIMETYPE      "image/png"
    IMAGEMODE     RGB
    EXTENSION     "png"
  END\n"""

    return output

def getGif():
    """
    Get gif output section

    Returns:
        output: The gif section
    """
    output = """OUTPUTFORMAT
    NAME          "gif"
    DRIVER        "GD/GIF"
    MIMETYPE      "image/gif"
    IMAGEMODE     PC256
    EXTENSION     "gif"
  END\n"""

    return output

def getJpeg():
    """
    Get jpeg output section

    Returns:
        output: The jpeg section
    """
    output = """OUTPUTFORMAT
    NAME          "jpeg"
    DRIVER        "AGG/JPEG"
    MIMETYPE      "image/jpeg"
    IMAGEMODE     RGB
    EXTENSION     "jpg"
  END\n"""

    return output

def getScale():
    """
    Get scalebar section

    Returns:
        scale: The scalebar section
    """
    scale = """SCALEBAR
    STATUS        OFF
    UNITS         KILOMETERS
    INTERVALS     3
    TRANSPARENT   TRUE
    OUTLINECOLOR  0 0 0
  END\n"""

    return scale

def getLegend():
    """
    Get legend section

    Returns:
        legend: The legend section
    """
    legend = """LEGEND
    STATUS        ON
    LABEL
        COLOR       51 51 51
        FONT        verdana       # font needs to be inside fonts.list
        TYPE        TRUETYPE
        SIZE        8
    END
    KEYSIZE       24 16
  END\n"""

    return legend

def getSize(x = 2048, y = 2048):
    """
    Get size section

    Args:
        x: X value in pixel (optional, default 2048)
        y: Y value in pixel (optional, default 2048)

    Returns:
        size: The size section
    """
    size = 'SIZE            {x} {y}'.format(x=str(x), y=str(y))
    return size

def getUnits():
    """
    Get unit section

    Returns:
        units: The units section
    """
    units = 'UNITS            METERS'
    return units

def getExtent(ext):
    """
    Get extent section

    Args:
        ext: The extent as an object with { xmin, ymin, xmax, ymax }

    Returns:
        extent: The extent section
    """
    extent = 'EXTENT           {xmin} {ymin} {xmax} {ymax}'.format(xmin=ext[0], ymin=ext[1], xmax=ext[2], ymax=ext[3])
    return extent

def getProjection(epsg):
    """
    Get projection section

    Args:
        epsg: The EPSG code for the projection

    Returns:
        projection: The projection section
    """
    projection = """PROJECTION
    "init=epsg:{epsg}"
  END""".format(epsg=epsg)

    return projection

def getWeb(title, abstract, keywords):
    """
    Get web section

    Args:
        title: The dataset title
        abstract: The datataset abstract
        keywords: The dataset keywords 

    Returns:
        web: The web section
    """
    web = """WEB
    IMAGEPATH     "/tmp/"
    IMAGEURL      "/tmp/"
    METADATA
      "wms_title"                   "GOV Canada - {title}"
      "wms_abstract"                "{abstract}"
      "wms_server_version"          "1.1.1"
      "wms_enable_request"          "GetCapabilities GetMap GetFeatureInfo GetLegendGraphic"
      "wms_formatlist"              "image/png,image/gif,image/jpeg"
      "wms_format"                  "image/png"
      "wms_feature_info_mime_type"  "text/html"
      "wms_keywordlist"             "Canada,Map,Carte,NRCan,RNCan,Natural Resources Canada,Ressources naturelles Canada,{keywords}"
      INCLUDE                       "./etc/projections.inc"
      INCLUDE                       "./etc/service_metadata_en.inc"
    END # metadata
  END  # web""".format(title=title, abstract=abstract, keywords=keywords)

    return web

def getLayerMetadata(name, projection):
    """
    Get layer metadata section

    Args:
        name: The wms title
        projections: The datataset projection

    Returns:
        meta: The layer metadata section
    """
    meta = """METADATA
        "wms_title"             "{name}"
        "wms_srs"               "EPSG:{projection}"
        "wms_enable_request"         "GetCapabilities GetMap GetFeatureInfo GetLegendGraphic"
    END # metadata""".format(name=name, projection=projection)

    return meta

def getLayerGeometry(fieldsNode):
    """
    Get layer's geometry

    Args:
        fieldsNode: The xml FeatureTable/FieldDescriptions node

    Returns:
        geom: The geomatry type (Point, Line or Polygon)
    """
    poly = False
    line = False

    if fieldsNode != None:
        for elem in fieldsNode:
            fieldName = elem.find('./FieldName').text
            if 'SHAPE_LENGTH' == fieldName.upper():
                line = True
            elif 'SHAPE_AREA' == fieldName.upper():
                poly = True

    if poly:
        geom = 'Polygon'
    elif line:
        geom = 'Line'
    else:
        # if there is no field description we assume it is a point layer
        # TODO: validate the assumption
        geom = 'Point'

    return geom

def getMap(docInfo, dataFrameInfo, epsg):
    """
    Create the map section

    Args:
        docInfo: The document information
        dataFrameinfo: the data frame information
        espg: The EPSG code
    """
    log('  NAME            "' + dataFrameInfo['name'] + '"')
    log(getMapCommon(), 2, False)
    log(getExtent(dataFrameInfo['ext']), 2, False)
    log(getSize(), 2, False)
    log(getUnits() + '\n', 2, False)

    log(getPng(), 2, False)
    log(getGif(), 2, False)
    log(getJpeg(), 2, False)

    log(getScale(), 2, False)
    log(getLegend(), 2, False)

    log(getProjection(epsg), 2, False)

    log(getWeb(docInfo['title'], docInfo['abstract'], ['docInfo.keywords']), 2, False)

    log(getSeparator(), 2, False)

def getDocumentInfo(root):
    """
    Get document info

    Args:
        root: The xml root node

    Returns:
        values: The needed values (title, abstract, keywords and data frame name)
    """
    values = {}
    values['title'] = root.findtext('./DocumentTitle')
    values['abstract'] = root.findtext('./Subject')
    values['keywords'] = root.findtext('./Keywords').replace(' ', '')
    values['dataFrame'] = os.path.basename(root.findtext('./ActiveMapRepositoryPath'))

    return values

def getDataframeInfo(root):
    """
    Get data frame info

    Args:
        root: The xml root node

    Returns:
        values: The needed values (name and epsg code)
    """
    values = {}
    values['name'] = root.findtext('./Name').replace(' ', '_')
    values['ext'] = [root.findtext('./DefaultExtent/XMin'),
        root.findtext('./DefaultExtent/YMin'),
        root.findtext('./DefaultExtent/XMax'),
        root.findtext('./DefaultExtent/YMax')]

    return values

def getSeparator():
    """
    Get separator between sections

    Returns:
        The separator
    """
    return '# --------------------------------------------------------------'