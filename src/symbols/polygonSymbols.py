def getPolygonStyle(color, width, fill):
    style = """CLASS
        STYLE
            COLOR           {fill}
            OUTLINECOLOR    {color}
            WIDTH           {width}
        END # style
    END # class""".format(color=color, width=width, fill=fill)

    return style