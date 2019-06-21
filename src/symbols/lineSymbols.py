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
            COLOR       {color}
            WIDTH       {width}
        END # style""".format(color=color, width=width)

    return style

def getFill(node):

    # get info
    fill = utils.getColor(node.find('./Pattern/Color'))

    # if fill is not define, it means there no color fill. Set it as white
    if 'fill' not in locals():
        fill = '255 255 255'

    style = """        STYLE
            COLOR       {fill}
        END # style""".format(fill=fill)

    return style