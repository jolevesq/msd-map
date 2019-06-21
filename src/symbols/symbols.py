# CIMSimpleMarker

import pointSymbols as pt
import lineSymbols as ln
import polygonSymbols as pl

import colorsys

def getSymbologyPoint(root):
    symbType = root.find('./Symbolizer').attrib.itervalues().next()

    if 'CIMSimpleSymbolizer' in symbType:
        stylesString = 'CLASS\n'

        # get array of symbols
        styles = root.findall('./Symbolizer/Symbol/Symbol/SymbolLayers/CIMSymbolLayer')
        styles.reverse()

        for style in styles:
            styleType = style.attrib.itervalues().next()

            if 'CIMSimpleMarker' in styleType:
                color = getColor(style.find('./OutlineColor'))
                width = style.find('./OutlineWidth').text
                fill = getColor(style.find('./FillColor'))
                size = style.find('./Size').text

                stylesString += getSimpleMarker(color, width, fill, size)

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
            stylesString += '        EXPRESSION   /' + value + '/\n'
            
            # get array of symbols
            styles = elem.findall('./Symbol/Symbol/SymbolLayers/CIMSymbolLayer')
            styles.reverse()

            for style in styles:
                styleType = style.attrib.itervalues().next()

                if 'CIMFilledStroke' in styleType:
                    stylesString += getFilledStroke(style) + '\n'
            
            stylesString += '    END # class ' + value + '\n'

    return stylesString

def getSymbologyLine(root):

    symbType = root.find('./Symbolizer').attrib.itervalues().next()

    if 'CIMSimpleSymbolizer' in symbType:
        stylesString = 'CLASS\n'

        # get array of symbols
        styles = root.findall('./Symbolizer/Symbol/Symbol/SymbolLayers/CIMSymbolLayer')
        styles.reverse()

        for style in styles:
            styleType = style.attrib.itervalues().next()

            if 'CIMFilledStroke' in styleType:
                stylesString += getFilledStroke(style) + '\n'
            elif 'CIMFill' in styleType:
                stylesString += getFill(style) + '\n'

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
            stylesString += '        EXPRESSION   /' + value + '/\n'
            
            # get array of symbols
            styles = elem.findall('./Symbol/Symbol/SymbolLayers/CIMSymbolLayer')
            styles.reverse()

            for style in styles:
                styleType = style.attrib.itervalues().next()

                if 'CIMFilledStroke' in styleType:
                    stylesString += getFilledStroke(style) + '\n'
            
            stylesString += '    END # class ' + value + '\n'

    return stylesString

def getSymbologyPolygon(root):

    symbType = root.find('./Symbolizer').attrib.itervalues().next()

    if 'CIMSimpleSymbolizer' in symbType:
        stylesString = 'CLASS\n'

        # get array of symbols
        styles = root.findall('./Symbolizer/Symbol/Symbol/SymbolLayers/CIMSymbolLayer')
        styles.reverse()

        for style in styles:
            styleType = style.attrib.itervalues().next()

            if 'CIMFilledStroke' in styleType:
                color = getColor(style.find('./Pattern/Color'))
                width = style.find('./Width').text
            elif 'CIMFill' in styleType:
                fill = getColor(style.find('./Pattern/Color'))

        # if fill is not define, it means there no color fill. Set it as white
        if 'fill' not in locals():
            fill = '255 255 255'

        stylesString += getFill(color, width, fill)

    elif 'CIMUniqueValueSymbolizer' in symbType:
        # get the field to render from
        stylesString = 'CLASSITEM          "' + root.find('./Symbolizer/Fields/String').text + '"\n'

        # get array of symbol class
        classes = root.findall('./Symbolizer/Groups/CIMUniqueValueGroup/Classes/CIMUniqueValueClass')

        for elem in classes:
            # get the expression for the class
            value = elem.find('./Values/CIMUniqueValue/FieldValues/String').text
            stylesString += '    CLASS\n'
            stylesString += '        EXPRESSION   /' + value + '/\n'
            
            # get array of symbols
            styles = elem.findall('./Symbol/Symbol/SymbolLayers/CIMSymbolLayer')
            styles.reverse()

            for style in styles:
                styleType = style.attrib.itervalues().next()

                if 'CIMFilledStroke' in styleType:
                    color = getColor(style.find('./Pattern/Color'))
                    width = style.find('./Width').text
                elif 'CIMFill' in styleType:
                    fill = '255 255 255' #getColor(style.find('./Pattern/Color'))

            # if fill is not define, it means there no color fill. Set it as white
            if 'fill' not in locals():
                fill = '255 255 255'

            stylesString += getFill(color, width, fill)

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
            styles.reverse()

            for style in styles:
                styleType = style.attrib.itervalues().next()

                if 'CIMFilledStroke' in styleType:
                    color = getColor(style.find('./Pattern/Color'))
                    width = style.find('./Width').text
                elif 'CIMFill' in styleType:
                    fill = getColor(style.find('./Pattern/Color'))
                
            stylesString += getFill(color, width, fill) + '\n'

    return stylesString

def getColor(node):
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


    return str(R) + ' ' + str(G) + ' ' + str(B)

def getFilledStroke(node):

    # get color and width
    color = getColor(node.find('./Pattern/Color'))
    width = node.find('./Width').text

    style = """        STYLE
            COLOR       {color}
            WIDTH       {width}
        END # style""".format(color=color, width=width)

    return style

def getFill(color, width, fill):
    style = """         STYLE
            COLOR           {fill}
            OUTLINECOLOR    {color}
            WIDTH           {width}
        END # style
    END # class""".format(color=color, width=width, fill=fill)

    return style

def getSimpleMarker(color, width, fill, size):
    style = """CLASS
        STYLE
            SYMBOL       "point"
            COLOR       {color}
            SIZE       {size}
        END # style
    END # class""".format(color=color, size=size)

    return style