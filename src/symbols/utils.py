import colorsys

# basse64 to png
# need to install pillow (pip install pillow). Make sure PYTHONPATH and other python variable are on ArcGIS python path
import base64
from PIL import Image
from io import BytesIO

# array to hold all symbols to add to map file
symbols = []

# varaible to increment name to avoid collision
incName = 0

def getSymbols():
    return symbols

# TODO: create a dictionnay of symbols ad check if the symbol exist, if so, reference it instead of creating it
def addSymbol(symbol):
    symbols.append(symbol)

def incrementName(name):
    global incName
    incName += 1

    return "{name}-{incName}".format(name=name, incName=incName)

def getColor(node):
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
        # case where image is use as fill. Not supported in map file
        R = 255
        G = 255
        B = 255

    return str(R) + ' ' + str(G) + ' ' + str(B)

def convertBase64(node, name):
    data = node.find('./Pattern/URL').text.split('base64,')[1]
    im = Image.open(BytesIO(base64.b64decode(data)))
    im.save(name + '.png', 'PNG')

def createSymbol(nameType, geom):
    # there seems to be a limit of points in MapServer for a symbol
    if ((len(geom.split(' ')) / 2) < 10):
        name = incrementName(nameType)

        symbol = """SYMBOL
            NAME "{name}"
            TYPE vector
            POINTS {geom} END
            FILLED true
    END # symbol {name}""".format(name=name, geom=geom)

        # add symbols to array of symbols
        addSymbol(symbol)

    else:
        name = 'circle'

    return name

def getRingSymbol(points):
    geom = addPointGeom(points)

    return createSymbol('ring', geom)

def getPathSymbol(paths):
    geom = ''
    for path in paths:
        points = path.findall('./PointArray/Point')

        geom += addPointGeom(points)

        # change path, add -99 -99
        geom += '-99 -99 '

    return createSymbol('path', geom)

def addPointGeom(points):

    xOld = ''
    yOld = ''
    geom = ''
    for point in points:
        x = str(round(float(point.findtext('./X')), 2))
        y = str(round(float(point.findtext('./Y')), 2))
            
        if (x != xOld or y != yOld):
            geom += x + ' ' + y + ' '

        # do not use duplicate values. MapServer seems to have a limit
        xOld = x
        yOld = y

    return geom