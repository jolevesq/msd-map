# import msd - map modules
import utils
import polygonSymbols
from common import lookup
from common import sections

def manageSymbols(styles):
    stylesString = ''
    styles.reverse()

    for style in styles:
        styleType = style.attrib.itervalues().next()

        # circle
        if 'CIMSimpleMarker' in styleType:
            color = utils.getColor(style.find('./OutlineColor'))
            width = style.find('./OutlineWidth').text
            fill = utils.getColor(style.find('./FillColor'))
            size = style.find('./Size').text

            stylesString += getSimpleMarker('circle', color, width, fill, size)

        elif 'CIMCharacterMarker' in styleType:
            stylesString += manageCharacterMarkerSymbol(style)

        # square, cross, x, diamond
        elif 'CIMVectorMarker' in styleType:
            stylesString += manageVectorMarker(style)


    return stylesString

def getSimpleMarker(marker, color, width, fill, size):
    style = """        STYLE
            SYMBOL       "{marker}"
            COLOR       {fill}
            OUTLINECOLOR {color}
            WIDTH       {width}
            SIZE       {size}
        END # style\n""".format(marker=marker, color=color, width=width, fill=fill, size=size)

    return style

def getSimpleMarkerLight(marker, color, size):
    style = """        STYLE
            SYMBOL       "{marker}"
            COLOR       {color}
            SIZE       {size}
        END # style\n""".format(marker=marker, color=color, size=size)

    return style

def manageCharacterMarkerSymbol(root):
    # get marker symbol
    name = utils.incrementName('marker')
    font = lookup.getFontfromESRI(root.find('./FontFamilyName').text)

    # escape "
    code = int(root.find('./CharacterIndex').text)
    if code == 34:
        char = '\\"'
    else:
        char = chr(code) # get character from ASCII
 
    # add symbols to array of symbols
    utils.addSymbol(getCharacterMarkerSymbol(name, font, char))

    # marker size to use in style
    size = root.find('./Size').text

    # only support one level deep
    # TODO: check if we need to support more...
    styleNode = root.find('./Symbol/SymbolLayers/CIMSymbolLayer')

    if 'CIMFill' in styleNode.attrib.itervalues().next():
        style = getFillMarkerStyle(styleNode, name, size)
    else:
        print 'NOT SUPPORTED'

    return style

    
def getCharacterMarkerSymbol(name, font, char):
    symbol = """SYMBOL
    NAME        "{name}"
    TYPE        truetype
    FONT        "{font}"
    CHARACTER   "{char}"
  END # symbol {name}""".format(name=name, font=font, char=char)

    return symbol

def getFillMarkerStyle(root, name, size):
    color = utils.getColor(root.find('./Pattern/Color')) 
    style = """        STYLE
            SYMBOL "{name}"
            COLOR {color}
            SIZE {size}
        END # style {name}\n""".format(name=name, color=color, size=size)

    return style

def manageVectorMarker(node):
    # there is 3 kind of vector marker.... for the moment
    # square doesn't have path node, only envelope
    # cross and x have PathArray node
    # diamond have RingArray node
    size = node.find('./Size').text
    styles = node.findall('./MarkerGraphics/CIMMarkerGraphic/Symbol/SymbolLayers/CIMSymbolLayer')

    styles.reverse()
    if node.find('./MarkerGraphics/CIMMarkerGraphic/Geometry/PathArray') != None:

        name = utils.getPathSymbol(node.findall('./MarkerGraphics/CIMMarkerGraphic/Geometry/PathArray/Path'))

        # there is only CIMFilledStroke symbol. If we need outline, fill will have a width of -1
        # if no outline, there is only one CIMFilledStroke with width -1
        # TODO: Validate
        styleString = ''
        for item in styles:
            if item.find('./Width').text == '-1':
                fill = utils.getColor(item.find('./Pattern/Color'))
                styleString += getSimpleMarkerLight(name, fill, size)
            else:
                color = utils.getColor(item.find('./Pattern/Color'))
                width = item.find('./Width').text
                styleString += getSimpleMarkerLight(name, color, float(size) + float(width))

    elif node.find('./MarkerGraphics/CIMMarkerGraphic/Geometry/RingArray') != None:
        
        name = utils.getRingSymbol(node.findall('./MarkerGraphics/CIMMarkerGraphic/Geometry/RingArray/Ring/PointArray/Point'))
        
        # Put back styles in first order. Seems to be the right one for ringArray
        styles.reverse()

        # TODO: same as aother path... manage all path the same way except square and circle... !!! ring array no width not real
        # CIMFill no width
        
        styleString = ''
        for item in styles:
            styleType = item.attrib.itervalues().next()

            if 'CIMFilledStroke' in styleType:
                color = utils.getColor(item.find('./Pattern/Color'))
                width = item.find('./Width').text
                styleString += getSimpleMarkerLight(name, color, float(size) + float(width))
            elif 'CIMFill' in styleType:
                fill = utils.getColor(item.find('./Pattern/Color'))
                styleString += getSimpleMarkerLight(name, fill, size)

    else:
        for item in styles:
            styleType = item.attrib.itervalues().next()
            
            if 'CIMFilledStroke' in styleType:
                color = utils.getColor(item.find('./Pattern/Color'))
                width = item.find('./Width').text
            #: TODO: CIMFill has no width. works the same as point, line polygon
            elif 'CIMFill' in styleType:
                fill = utils.getColor(item.find('./Pattern/Color'))

        styleString = getSimpleMarker('square', color, width, fill, size)

    return styleString



