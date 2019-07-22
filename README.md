# msd-map

Conversion of ESRI msd file to MapServer map file.

# How to use

Step 1: Copy locally the mxd file
Step 2: Copy the fgdb file on the mapServer server inside a folder under ./wms/data
Step 3: Run convertMXD.py with is 3 arguments
    * 1: Local mxd folder path
    * 2: Local mxd file name with extension
    * 3: The folder where is located the fgdb file (created at step 2)
Step 4: If your service contains picture symbol, images will be created inside the local folder.
    * Copy the images to the mapServer server (.wms/data/"step 2 folder"/img)
Step 4: Test the service


# known issues

The program may fail if he doesn't find a values from one of his lookup table (./common/lookup.py).
    * For EPSG:
        * Inside epsgDict dictionnary, only add the missing key/value (ESRI code/EPSG code)
    * For font:
        * Inside fontDict dictionnary, add the missing key/value (font name/font file name)
        * Copy the font file to mapServer server (./wms/etc/fonts/fonts)
        * Edit .wms/etc/fonts/fonts.list to add the missing font (font name        font file)