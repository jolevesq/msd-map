def getMapCommon():
    common = """SYMBOLSET       "./etc/symbols.sym"
  FONTSET         "./etc/fonts/fonts.list"
  IMAGETYPE       "png"
  """

    return common

def getPng():
    output = """OUTPUTFORMAT
    NAME          "png"
    DRIVER        "AGG/PNG"
    MIMETYPE      "image/png"
    IMAGEMODE     RGB
    EXTENSION     "png"
  END\n"""

    return output

def getGif():
    output = """OUTPUTFORMAT
    NAME          "gif"
    DRIVER        "GD/GIF"
    MIMETYPE      "image/gif"
    IMAGEMODE     PC256
    EXTENSION     "gif"
  END\n"""

    return output

def getJpeg():
    output = """OUTPUTFORMAT
    NAME          "jpeg"
    DRIVER        "AGG/JPEG"
    MIMETYPE      "image/jpeg"
    IMAGEMODE     RGB
    EXTENSION     "jpg"
  END\n"""

    return output

def getScale():
    scale = """SCALEBAR
    STATUS        OFF
    UNITS         KILOMETERS
    INTERVALS     3
    TRANSPARENT   TRUE
    OUTLINECOLOR  0 0 0
  END\n"""

    return scale

def getLegend():
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
    size = 'SIZE            {x} {y}'.format(x=str(x), y=str(y))
    return size

def getUnits():
    units = 'UNITS            METERS'
    return units

def getExtent(ext):
    extent = 'EXTENT           {xmin} {ymin} {xmax} {ymax}'.format(xmin=ext[0], ymin=ext[1], xmax=ext[2], ymax=ext[3])
    return extent

def getProjection(epsg):
    projection = """PROJECTION
    "init=epsg:{epsg}"
  END""".format(epsg=epsg)

    return projection

def getWeb(title, abstract, keywords):
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
    meta = """METADATA
        "wms_title"             "{name}"
        "wms_srs"               "EPSG:{projection}"
        "wms_enable_request"         "GetCapabilities GetMap GetFeatureInfo GetLegendGraphic"
    END # metadata""".format(name=name, projection=projection)

    return meta

def getLayerGeometry(fieldsNode):
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

def getSeparator():
    return '# --------------------------------------------------------------'