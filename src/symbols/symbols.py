# import msd - map modules
from common import lookup
import pointSymbols as pt
import lineSymbols as ln
import polygonSymbols as pl
from common import trace

def getSymbology(root, geom):
    """
    Get layer's style section. We support 3 type of symbolizer for now
        - Simple
        - Unique value
        - Class break

    Args:
        root: The xml symbology root node
        geom: The datataset geometry (Point, Line or Polygon)

    Returns:
        styleStrings: The styles for the layer
    """
    symbType = root.find('./Symbolizer').attrib.itervalues().next()

    if 'CIMSimpleSymbolizer' in symbType:
        trace.log('Add CIMSimpleSymbolizer')
        stylesString = 'CLASS\n'

        # get array of symbols
        styles = root.findall('./Symbolizer/Symbol/Symbol/SymbolLayers/CIMSymbolLayer')
        stylesString += getStyle(styles, geom)

        stylesString += '    END # class\n'

    elif 'CIMUniqueValueSymbolizer' in symbType:
        trace.log('Add CIMUniqueValueSymbolizer')

        # get the field to render from
        stylesString = 'CLASSITEM          "' + root.findtext('./Symbolizer/Fields/String') + '"\n'

        # get array of symbol class
        classes = root.findall('./Symbolizer/Groups/CIMUniqueValueGroup/Classes/CIMUniqueValueClass')

        for elem in classes:
            # get the expression for the class
            value = elem.findtext('./Values/CIMUniqueValue/FieldValues/String')
            stylesString += '    CLASS\n'
            stylesString += '        EXPRESSION   "' + value + '"\n'
            
            # get array of symbols
            styles = elem.findall('./Symbol/Symbol/SymbolLayers/CIMSymbolLayer')
            stylesString += getStyle(styles, geom)
            
            stylesString += '    END # class ' + value + '\n'

    elif 'CIMClassBreaksSymbolizer' in symbType:
        trace.log('Add CIMClassBreaksSymbolizer')

        # get the field to render from
        field = root.findtext('./Symbolizer/Field')
        stylesString = 'CLASSITEM          "' + field + '"\n'
        minimumBreak = root.findtext('./Symbolizer/MinimumBreak')

        # get array of symbol class
        classes = root.findall('./Symbolizer/Breaks/CIMClassBreak')

        for elem in classes:
            # get the expression for the class
            value = elem.findtext('./UpperBound')
            stylesString += '    CLASS\n'
            stylesString += '        EXPRESSION   ([' + field + ']>=' + minimumBreak + ' AND [' + field + ']<' + value + ')\n'
            
            minimumBreak = value
            
            # get array of symbols
            styles = elem.findall('./Symbol/Symbol/SymbolLayers/CIMSymbolLayer')
            stylesString += getStyle(styles, geom)

            stylesString += '    END # class ' + value + '\n'

     # remove last carriage return
    return stylesString.rstrip()

def getStyle(styles, geom):
    """
    Get Get the styles in function of the geometry

    Args:
        styles: The xml styles nodes
        geom: The datataset geometry (Point, Line or Polygon)

    Returns:
        styleStrings: The styles for the layer
    """
    if geom == 'Point':
        stylesString = pt.manageSymbols(styles)
    elif geom == 'Line':
        stylesString = ln.manageSymbols(styles)
    elif geom == 'Polygon':
        stylesString = pl.manageSymbols(styles)

    return stylesString