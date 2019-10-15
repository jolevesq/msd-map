# needed to keep order before Python 3.7
from collections import OrderedDict

# import msd - map modules
import utils
from common import lookup
from common import sections
from common import trace

def manageSymbols(styles, values = OrderedDict([]), fields = []):
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
        # copy original values and get type
        oriValues = values.copy()
        oriFields = list(fields)
        styleType = item.attrib.itervalues().next()

        if 'CIMFilledStroke' in styleType:
            trace.log('Create line: CIMFilledStroke')

            oriFields.extend(['COLOR', 'WIDTH'])
            oriValues['COLOR'] = utils.getColor(item.find('./Pattern/Color'))
            oriValues['WIDTH'] = item.findtext('./Width')

            if item.find('./CapStyle') != None:
                oriValues['LINECAP'] = item.findtext('./CapStyle').lower()
                oriFields.append('LINECAP')
            if item.find('./JoinStyle') != None:
                oriValues['LINEJOIN'] = item.findtext('./JoinStyle').lower()
                oriFields.append('LINEJOIN')
            if item.find('./MiterLimit') != None:
                oriValues['LINEJOINMAXSIZE'] = item.findtext('./MiterLimit').lower()
                oriFields.append('LINEJOINMAXSIZE')

            # effects for cartographic line symbol
            effects = item.find('./Effects')
            pattern = ''
            if effects != None:
                pattern = createEffects(effects)
                oriValues['PATTERN'] = pattern
                oriFields.append('PATTERN')

            stylesString += utils.createStyle(oriValues, oriFields)
        elif 'CIMFill' in styleType:
            trace.log('Create line: CIMFill')

            values['COLOR'] = utils.getColor(item.find('./Pattern/Color'))
            stylesString += utils.createStyle(values, ['COLOR'])

        elif 'CIMPlacedPointSymbols' in styleType:
            # hash line symbol
            print 'CIMPlacedPointSymbols (hash) not supported for line layer'
            trace.log('Create line: CIMPlacedPointSymbols (hash) not supported for line layer')
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