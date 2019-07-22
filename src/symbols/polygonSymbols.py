# needed to keep order before Python 3.7
from collections import OrderedDict

# import msd - map modules
import utils
import pointSymbols
import lineSymbols
from common import lookup
from common import sections

def manageSymbols(styles):
    """
    Create style for polygon layer

    Args:
        styles: The array of styles xml node

    Returns:
        styleString: The layer's style section
    """
    stylesString = ''
    styles.reverse()

    values = OrderedDict()
    for item in styles:
        styleType = item.attrib.itervalues().next()

        if 'CIMFilledStroke' in styleType:
            values['OUTLINECOLOR'] = utils.getColor(item.find('./Pattern/Color'))
            values['WIDTH'] = item.findtext('./Width')
            
            stylesString += utils.createStyle(values, ['OUTLINECOLOR', 'WIDTH'])
        elif 'CIMFill' in styleType:
            stylesString += getFill(item, values)

    return stylesString

def getFill(node, values):
    """
    Create fill pattern

    Args:
        node: The styles xml node
        values: The dictionnary of values to add (optional, default empty dictionnary)

    Returns:
        style: The layer's fill
    """
    # check fill pattern
    style = ''
    pattern = node.find('./Pattern').attrib.itervalues().next()

    if 'CIMSolidPattern' in pattern:
        values['COLOR'] = utils.getColor(node.find('./Pattern/Color'))
        style = utils.createStyle(values, ['COLOR'])

    elif 'CIMTiledPattern' in pattern:
        name = utils.createPictureSymbol(node.find('./Pattern'))
        values['SYMBOL'] = name
        style = utils.createStyle(values)   

    elif 'CIMMarkerPattern' in pattern:
        values['GAP'] = node.findtext('./Pattern/MarkerPlacement/StepX')
        style = pointSymbols.manageSymbols(node.findall('./Pattern/Symbol/SymbolLayers/CIMSymbolLayer'), values)

    elif 'CIMHatchPattern' in pattern:
        style = ''
        size = float(node.findtext('./Pattern/Separation'))
        
        # find symbol to use from rotation. For size, double value when not horizontal
        deg = round(float(node.findtext('./Pattern/Rotation')) / 45) * 45
        if deg in [0, 180]:
            name = 'hatch-0'
        elif deg in [90, 270]:
            name = 'hatch-90'
            size += size
        elif deg in [45, 225]:
            name = 'hatch-45'
            size += size
        elif deg in [135, 315]:
            name = 'hatch-135'
            size += size

        values['SYMBOL'] = name
        values['SIZE'] = size
        fields = ['SYMBOL', 'SIZE']
        style = lineSymbols.manageSymbols(node.findall('./Pattern/LineSymbol/SymbolLayers/CIMSymbolLayer'), values, fields)

    elif 'CIMGradientPattern' in pattern:
        print 'CIMGradientPattern not supported for polygon layer'

    else:
        print pattern + ' is not supported for polygon layer'

    return style