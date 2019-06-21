# import msd - map modules
from common import lookup
import pointSymbols as pt
import lineSymbols as ln
import polygonSymbols as pl

def getSymbology(root, geom):
    symbType = root.find('./Symbolizer').attrib.itervalues().next()

    if 'CIMSimpleSymbolizer' in symbType:
        stylesString = 'CLASS\n'

        # get array of symbols
        styles = root.findall('./Symbolizer/Symbol/Symbol/SymbolLayers/CIMSymbolLayer')
        stylesString += getStyle(styles, geom)

        stylesString += '    END # class\n'

    elif 'CIMUniqueValueSymbolizer' in symbType:
        # get the field to render from
        stylesString = 'CLASSITEM          "' + root.find('./Symbolizer/Fields/String').text + '"\n'

        # get array of symbol class
        classes = root.findall('./Symbolizer/Groups/CIMUniqueValueGroup/Classes/CIMUniqueValueClass')

        for elem in classes:
            # get the expression for the class
            value = elem.find('./Values/CIMUniqueValue/FieldValues/String').text
            stylesString += '    CLASS\n'
            stylesString += '        EXPRESSION   "' + value + '"\n'
            
            # get array of symbols
            styles = elem.findall('./Symbol/Symbol/SymbolLayers/CIMSymbolLayer')
            stylesString += getStyle(styles, geom)
            
            stylesString += '    END # class ' + value + '\n'

    elif 'CIMClassBreaksSymbolizer' in symbType:
        # get the field to render from
        field = root.find('./Symbolizer/Field').text
        stylesString = 'CLASSITEM          "' + field + '"\n'
        minimumBreak = root.find('./Symbolizer/MinimumBreak').text

        # get array of symbol class
        classes = root.findall('./Symbolizer/Breaks/CIMClassBreak')

        for elem in classes:
            # get the expression for the class
            value = elem.find('./UpperBound').text
            stylesString += '    CLASS\n'
            stylesString += '        EXPRESSION   ([' + field + ']>=' + minimumBreak + ' AND [' + field + ']<' + value + ')\n'
            
            minimumBreak = value
            
            # get array of symbols
            styles = elem.findall('./Symbol/Symbol/SymbolLayers/CIMSymbolLayer')
            stylesString += getStyle(styles, geom)

            stylesString += '    END # class ' + value + '\n'

    return stylesString

def getStyle(styles, geom):
    if geom == 'Point':
        stylesString = pt.manageSymbols(styles)
    elif geom == 'Line':
        stylesString = ln.manageSymbols(styles)
    elif geom == 'Polygon':
        stylesString = pl.manageSymbols(styles)

    return stylesString