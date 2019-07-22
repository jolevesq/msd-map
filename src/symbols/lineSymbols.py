# needed to keep order before Python 3.7
from collections import OrderedDict

# import msd - map modules
import utils
from common import lookup
from common import sections

def manageSymbols(styles, values = OrderedDict(), fields = []):
    """
    Create style for line layer

    Args:
        styles: The array of styles xml node
        values: The dictionnary of values to add (optional, default empty dictionnary)
        fields: The array of values to add from the dictionnary keys (optional, default empty. If empty, use all values)

    Returns:
        styleString: The layer's style section
    """
    stylesString = ''
    styles.reverse()

    for item in styles:
        styleType = item.attrib.itervalues().next()

        if 'CIMFilledStroke' in styleType:
            fields.extend(['COLOR', 'WIDTH'])
            values['COLOR'] = utils.getColor(item.find('./Pattern/Color'))
            values['WIDTH'] = item.findtext('./Width')

            # efffects for cartographic line symbol
            effects = item.find('./Effects')
            pattern = ''
            if effects != None:
                pattern = createEffects(effects)
                values['PATTERN'] = pattern
                fields.append('PATTERN')

            stylesString += utils.createStyle(values, fields)
        elif 'CIMFill' in styleType:
            values['COLOR'] = utils.getColor(item.find('./Pattern/Color'))
            stylesString += utils.createStyle(values, ['COLOR'])

        elif 'CIMPlacedPointSymbols' in styleType:
            # hash line symbol
            print 'CIMPlacedPointSymbols (hash) not supported for line layer'
        else:
            print styleType + ' not supported for line layer'


    return stylesString

def createEffects(node):
    """
    Create line effect

    Args:
        node: The xml effect node

    Returns:
        pattern: The line effect
    """
    effectType = node.attrib.itervalues().next()

    pattern = ''
    if 'ArrayOfCIMGeometricEffect' in effectType:
        effects = node.findall('./CIMGeometricEffect')

        for effect in effects:
            dashes = effect.find('./DashTemplate').findall('./Double')

            for dash in dashes:
                pattern += dash.text + ' '

        pattern += ' END'

    return pattern