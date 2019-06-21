
def getLineStyle(color, width):
    style = """CLASS
        STYLE
            COLOR       {color}
            WIDTH       {width}
        END # style
    END # class""".format(color=color, width=width)

    return style