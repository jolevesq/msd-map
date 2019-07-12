# Symbol
* Features
    * Simple Symbol (draw with symbol level in advance mode)
* Categories
    * Unique Value
    * Unique Value, Many fields
* Quantity
    * Graduated Colors
    * Graduated Symbols
    * Proportional Symbols
    * Dot density (Polygon)
* Chart
    * Pie
    * Bar
    * Stacked
* Multiple Attributes
    * Quantity by Category

# Marker - Symbols Type
* Simple Marker Symbol
    * Simple Marker
        * Style (Circle - CIMSimpleMarker, CIMVectorMarker: Square, Cross X, Diamond)
    * Mask (Polygon fill symbol)
* Picture Marker Symbol
    * Picture Marker
    * Mask (Polygon fill symbol)
* Character Marker Symbol
    * Character Marker
    * Mask Polygon Fill
* Arrow Marker Symbol
    * Arrow Marker
    * Mask (Polygon fill symbol)

# Line - Symbols Type
* Simple Line Symbol
    * Simple Line
* Cartographic Line Symbol
    * Cartographic Line (Color, Width, Line Cap, Line Join)
    * Template (Pattern)
    * Line Properties (Arrow and Offset)
* Marker Line Symbol
    * Marker Line (Point Symbol!!)
    * Cartographic Line (Color, Width, Line Cap, Line Join)
    * Template (Pattern)
    * Line Properties (Arrow and Offset)
* Hash Line Symbol
    * Hash Line (Simple Line Symbol)
    * Cartographic Line (Color, Width, Line Cap, Line Join)
    * Template (Pattern)
    * Line Properties (Arrow and Offset)

# Polygon - Symbols Type
* Simple Fill Symbol
    * Simple Fill
        * Outline (Line symbol)
* Gradient Fill Symbol
    * Gradient Fill
        * Outline (Line symbol)
* Line Fill Symbol
    * Line Fill
        * Line (Line symnbol)
        * Outline (Line symbol)
* Marker Fill Symbol
    * Marker Fill
        * Marker (Point symbol)
        * Outline (Line symbol)
    * Fill Properties
* Picture Fill Symbol
    * Picture Fill
    * Fill Properties

# Not supported

There is no support for picture element like

* 3D Marker Symbol
* 3D SimpleMarker Symbol
* 3D Character Marker Symbol

* Picture Line Symbol (Picture Line)
* 3D Texture Line Symbol
* 3D Simple Line Symbol

* 3D Texture Fill Symbol


# How to work with symbols
We can add symbols to a symbols.sym file with a symbolset inside. We can define each symbol inside the map file at the map level.
e.g.:
 SYMBOL
    NAME "test_png"
    TYPE PIXMAP
    IMAGE "./data/Influenza/img/int.png"
  END

This will be the best way so we keep images at the same place as data. in our case it will be automatique so there is not a lot of reuse available.
We can have both inside a map file.

# ESRI Hierarchy

* CIMFilledStroke
    * CIMSolidPattern
    * COLOR: CIMRGBColor or CIMHSVColor
    
* CIMFill
    * CIMSolidPattern
    * COLOR: CIMRGBColor or CIMHSVColor

* CIMFill
    * CIMTiledPattern (need URL)
    * COLOR: There is color but is it needed?


# Values from styles

* CIMSolidPattern
    * Color
    * Width

* CIMFIll
    * Color