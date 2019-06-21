def getPointStyle(color, size):
    style = """CLASS
        STYLE
            SYMBOL       "point"
            COLOR       {color}
            SIZE       {size}
        END # style
    END # class""".format(color=color, size=size)

    return style