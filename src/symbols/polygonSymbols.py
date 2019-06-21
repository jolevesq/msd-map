# import msd - map modules
import utils
from common import lookup
from common import sections

def manageSymbols(styles):
    stylesString = ''
    styles.reverse()

    for style in styles:
        styleType = style.attrib.itervalues().next()

        if 'CIMFilledStroke' in styleType:
            stylesString += getFilledStroke(style) + '\n'
        elif 'CIMFill' in styleType:
            stylesString += getFill(style) + '\n'

    return stylesString

def getFilledStroke(node):

    # get info
    color = utils.getColor(node.find('./Pattern/Color'))
    width = node.find('./Width').text

    style = """        STYLE
            OUTLINECOLOR       {color}
            WIDTH       {width}
        END # style""".format(color=color, width=width)

    return style

def getFill(node):

    # check fill pattern
    pattern = node.find('./Pattern').attrib.itervalues().next()

    if 'CIMSolidPattern' in pattern:
        # get info
        fill = utils.getColor(node.find('./Pattern/Color'))

        # if fill is not define, it means there no color fill. Set it as white
        if 'fill' not in locals():
            fill = '255 255 255'

        style = """        STYLE
                COLOR       {fill}
            END # style""".format(fill=fill)

    elif 'CIMTiledPattern' in pattern:
        name = utils.incrementName('picture')
        # add symbols to array of symbols
        utils.addSymbol(getFillPictureSymbol(name))
        utils.convertBase64(node, name)

        style = """        STYLE
            SYMBOL       "{name}"
        END # style""".format(name=name)

    elif 'CIMMarkerPattern' in pattern:
        style = ''

    elif 'CIMHatchPattern' in pattern:
        style = ''

    elif  'CIMGradientPattern' in pattern:
        style = ''

    else: 
        style = pattern

    return style

def getFillPictureSymbol(name):
    folder = sections.getProjectFolderName()

    symbol = """SYMBOL
    NAME        "{name}"
    TYPE        pixmap
    IMAGE       "data/{folder}/img/{name}.png"
  END # symbol {name}""".format(name=name, folder=folder)

    return symbol