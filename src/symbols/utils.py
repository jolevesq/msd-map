import colorsys

# basse64 to png
# need to install pillow (pip install pillow). Make sure PYTHONPATH and other python variable are on ArcGIS python path
import base64
from PIL import Image
from io import BytesIO

# import msd - map modules
from common import sections
from common import trace

# array to hold all symbols to add to map file
symbols = []

# varaible to increment name to avoid collision
incName = 0

def getSymbols():
    """
    Get array of symbols

    Returns:
        symbols: The array of symbols
    """
    return symbols

# TODO: create a dictionnay of symbols and check if the symbol exist, if so, reference it instead of creating it
def addSymbol(symbol):
    """
    Add a symbol to the array of symbols

    Args:
        symbol: The symbol to add
    """
    symbols.append(symbol)

def incrementName(name):
    """
    Increment and return a unique symbol name

    Args:
        name: The symbol name from symbol type (e.g. path, hatch, ring, ...)

    Returns:
        The unique name
    """
    global incName
    incName += 1

    return "{name}-{incName}".format(name=name, incName=incName)

def getColor(node):
    """
    Get RGB color from color node

    Args:
        node: The xml color node

    Returns:
        color: The RGB color
    """
    if node != None:
        colorType = node.attrib.itervalues().next()

        if 'RGBColor' in colorType:
            R = node.find('./R').text
            G = node.find('./G').text
            B = node.find('./B').text

        elif 'HSVColor' in colorType:
            h = float(node.find('./H').text) / 360
            s = float(node.find('./S').text) / 100
            v = float(node.find('./V').text) / 100

            color = colorsys.hsv_to_rgb(h, s, v)
            R = int(color[0] * 255)
            G = int(color[1] * 255)
            B = int(color[2] * 255)

        elif 'CIMCMYKColor' in colorType:
            c = int(node.find('./C').text)
            m = int(node.find('./M').text)
            y = int(node.find('./Y').text)
            k = int(node.find('./K').text)
    
            R = int(255 * (100 - (c + k)) / 100)
            G = int(255 * (100 - (m + k)) / 100)
            B = int(255 * (100 - (y + k)) / 100)

    else:
        trace.log('No color provided')
        # case where image is use as fill. Not supported in map file
        R = 'null'
        G = 'null'
        B = 'null'

    return str(R) + ' ' + str(G) + ' ' + str(B)

def convertBase64(node, name):
    """
    Convert a base64 image to a png

    Args:
        node: The xml url node
        name: The name of the output file
    """
    data = node.findtext('./URL').split('base64,')[1]
    im = Image.open(BytesIO(base64.b64decode(data)))
    im.save(name + '.png', 'PNG')

def createStyle(values, fields = []):
    """
    Create the style section from dictionnary of values/keys

    Args:
        values: Dictionnary of values
        fields: The array of values to add from the dictionnary keys (optional, default empty. If empty, use all values)

    Returns:
        style: The style section
    """
    # iterate over key pair
    keys = ''
    for key, value in values.items():

        # if an array of keys to add is provided, check if the key is part of it
        if len(fields) == 0 or key in fields:
            if key == 'SYMBOL':
                value = '"' + value + '"'

            keys += '            ' + key + '         ' + str(value) + '\n'

    # remove last carriage return
    keys = keys.rstrip()

    style = """        STYLE
{keys}
        END # style\n""".format(keys=keys)

    return style

def createPictureSymbol(node):
    """
    Create picture symbol

    Args:
        node: The xml symbol node

    Returns:
        name: The name to use in the symbol value of style section
    """
    folder = sections.getProjectFolderName()
    name = incrementName('picture')

    # convert to png
    convertBase64(node, name)

    symbol = """SYMBOL
    NAME        "{name}"
    TYPE        pixmap
    IMAGE       "data/{folder}/img/{name}.png"
  END # symbol {name}""".format(name=name, folder=folder)

    # add symbols to array of symbols
    addSymbol(symbol)

    return name

def createVectorSymbol(nameType, geom, filled):
    """
    Create vector symbol

    Args:
        nameType: The name type to increment to get the unique symbol value
        geom: The vector geometry as a list of coordinates
        filled: The filled value for the symbol (true or false)

    Returns:
        name: The name to use in the symbol value of style section
    """
    # there seems to be a limit of points in MapServer for a symbol
    # if values exceed the limit, use a circle symbol instead
    if ((len(geom.split(' ')) / 2) < 20):
        name = incrementName(nameType)

        symbol = """SYMBOL
    NAME        "{name}"
    TYPE        vector
    POINTS      {geom} END
    FILLED      {filled}
  END # symbol {name}""".format(name=name, geom=geom, filled=filled)

        # add symbols to array of symbols
        addSymbol(symbol)

    else:
        name = 'circle'

    return name

def getRingSymbol(points):
    """
    Create vector symbol of type ring

    Args:
        points: The list of coordinates

    Returns:
        name: The name to use in the symbol value of style section
    """
    geom = addPointGeom(points)

    return createVectorSymbol('ring', geom, 'true')

def getPathSymbol(paths):
    """
    Create vector symbol of type path

    Args:
        paths: The list of paths who contains coordinates

    Returns:
        name: The name to use in the symbol value of style section
    """
    geom = ''
    for path in paths:
        points = path.findall('./PointArray/Point')

        geom += addPointGeom(points)

        # change path, add -99 -99
        geom += '-99 -99 '

    return createVectorSymbol('path', geom, 'false')

def addPointGeom(points):
    """
    Create the list of points of a path or ring symbol

    Args:
        points: The list of coordinates

    Returns:
        geom: The symbol geometry as a list of points
    """
    xOld = ''
    yOld = ''
    geom = ''
    for point in points:
        x = str(round(float(point.findtext('./X')), 2))
        y = str(round(float(point.findtext('./Y')), 2))
        
        # if value is not identical as a old point, add it
        if (x != xOld or y != yOld):
            geom += x + ' ' + y + ' '

        # do not use duplicate values. MapServer seems to have a limit
        xOld = x
        yOld = y

    return geom