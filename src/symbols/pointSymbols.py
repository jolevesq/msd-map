# needed to keep order before Python 3.7
from collections import OrderedDict

# import msd - map modules
import utils
from common import lookup
from common import sections
from common import trace

def manageSymbols(styles, values = OrderedDict()):
    """
    Create style for point layer

    Args:
        styles: The array of styles xml node
        values: The dictionnary of values to add (optional, default empty dictionnary)

    Returns:
        styleString: The layer's style section
    """
    stylesString = ''
    styles.reverse()

    for style in styles:
        styleType = style.attrib.itervalues().next()

        # get rotation, offset and size. There for all CIMSymbolLayer
        values['SYMBOL'] = 'tmp'
        values['ANGLE'] = style.findtext('./Rotation')
        values['OFFSET'] = style.findtext('./OffsetX') + ' ' + style.findtext('./OffsetY')
        values['SIZE'] = style.findtext('./Size')

        # circle
        if 'CIMSimpleMarker' in styleType:
            trace.log('Create point: CIMSimpleMarker')

            values['OUTLINECOLOR'] = utils.getColor(style.find('./OutlineColor'))
            values['WIDTH'] = style.findtext('./OutlineWidth')
            values['COLOR'] = utils.getColor(style.find('./FillColor'))
            values['SIZE'] = style.findtext('./Size')
            values['SYMBOL'] = 'circle'
            stylesString += utils.createStyle(values)

        elif 'CIMCharacterMarker' in styleType:
            trace.log('Create point: CIMCharacterMarker')
            stylesString += manageCharacterMarkerSymbol(style, values)

        # square, cross, x, diamond
        elif 'CIMVectorMarker' in styleType:
            trace.log('Create point: CIMVectorMarker')
            stylesString += manageVectorMarker(style, values)

        elif 'CIMPictureMarker' in styleType:
            trace.log('Create point: CIMPictureMarker')
            name = utils.createPictureSymbol(style)
            values['SYMBOL'] = name
            stylesString += utils.createStyle(values)

    return stylesString

def manageCharacterMarkerSymbol(root, values):
    """
    Create character marker style for point layer

    Args:
        root: The styles xml node
        values: The dictionnary of values to add (optional, default empty dictionnary)

    Returns:
        style: The layer's style section
    """
    # get marker symbol
    values['SYMBOL'] = utils.incrementName('marker')
    font = lookup.getFontfromESRI(root.find('./FontFamilyName').text)

    # escape "
    code = int(root.find('./CharacterIndex').text)
    if code == 34:
        char = '\\"'
    else:
        char = chr(code) # get character from ASCII
 
    # add symbols to array of symbols
    utils.addSymbol(getCharacterMarkerSymbol(values['SYMBOL'], font, char))

    # only support one level deep
    # TODO: check if we need to support more...
    styleNode = root.find('./Symbol/SymbolLayers/CIMSymbolLayer')
    styleType = styleNode.attrib.itervalues().next()
    if 'CIMFill' in styleType:
        values['COLOR'] = utils.getColor(styleNode.find('./Pattern/Color'))
        style = utils.createStyle(values)
    else:
        print styleType + ' is not supported for point layer'

    return style

    
def getCharacterMarkerSymbol(name, font, char):
    """
    Create character marker symbol

    Args:
        name: The symbol name
        font: The symbol font
        char: the character to use

    Returns:
        symbol: The character marker symbol
    """
    symbol = """SYMBOL
    NAME        "{name}"
    TYPE        truetype
    FONT        "{font}"
    CHARACTER   "{char}"
  END # symbol {name}""".format(name=name, font=font, char=char)

    return symbol

def manageVectorMarker(node, values):
    """
    Create vector marker style for point layer

    Args:
        node: The style xml node
        values: The dictionnary of values to add (optional, default empty dictionnary)

    Returns:
        styleString: The vector marker symbol
    """
    # there is 3 kind of vector marker.... for the moment
    # square doesn't have path node, only envelope
    # cross and x have PathArray node
    # diamond have RingArray node
    styles = node.findall('./MarkerGraphics/CIMMarkerGraphic/Symbol/SymbolLayers/CIMSymbolLayer')

    styles.reverse()
    if node.find('./MarkerGraphics/CIMMarkerGraphic/Geometry/PathArray') != None:

        values['SYMBOL'] = utils.getPathSymbol(node.findall('./MarkerGraphics/CIMMarkerGraphic/Geometry/PathArray/Path'))

        # there is only CIMFilledStroke symbol. If we need outline, fill will have a width of -1
        # if no outline, there is only one CIMFilledStroke with width -1
        # TODO: Validate
        styleString = ''
        for item in styles:
            if item.find('./Width').text == '-1':
                values['COLOR'] = utils.getColor(item.find('./Pattern/Color'))
                styleString += utils.createStyle(values, ['SYMBOL', 'COLOR', 'SIZE', 'ANGLE'])
            else:
                values['OUTLINECOLOR'] = utils.getColor(item.find('./Pattern/Color'))
                values['SIZE'] = float(item.findtext('./Width')) + float(values['SIZE'])
                styleString += utils.createStyle(values, ['SYMBOL', 'OUTLINECOLOR', 'SIZE'])

    elif node.find('./MarkerGraphics/CIMMarkerGraphic/Geometry/RingArray') != None:
        
        values['SYMBOL'] = utils.getRingSymbol(node.findall('./MarkerGraphics/CIMMarkerGraphic/Geometry/RingArray/Ring/PointArray/Point'))
        
        # Put back styles in first order. Seems to be the right one for ringArray
        styles.reverse()

        # TODO: same as aother path... manage all path the same way except square and circle... !!! ring array no width not real
        # CIMFill no width
        
        styleString = ''
        for item in styles:
            styleType = item.attrib.itervalues().next()

            if 'CIMFilledStroke' in styleType:
                values['OUTLINECOLOR'] = utils.getColor(item.find('./Pattern/Color'))
                values['SIZE'] = float(item.findtext('./Width')) + float(values['SIZE'])
                styleString += utils.createStyle(values, ['SYMBOL', 'OUTLINECOLOR', 'SIZE'])
            elif 'CIMFill' in styleType:
                values['COLOR'] = utils.getColor(item.find('./Pattern/Color'))
                styleString += utils.createStyle(values, ['SYMBOL', 'COLOR', 'SIZE', 'ANGLE'])

    else:
        for item in styles:
            styleType = item.attrib.itervalues().next()

            if 'CIMFilledStroke' in styleType:
                values['OUTLINECOLOR'] = utils.getColor(item.find('./Pattern/Color'))
                values['WIDTH'] = item.findtext('./Width')
            #: TODO: CIMFill has no width. works the same as point, line polygon
            elif 'CIMFill' in styleType:
                values['COLOR'] = utils.getColor(item.find('./Pattern/Color'))

        values['SYMBOL'] = 'square'
        styleString = utils.createStyle(values)

    return styleString



