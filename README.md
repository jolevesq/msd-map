# msd-map

Conversion of ESRI msd file to MapServer map file.


# How to use

Step 1: Copy locally the mxd file<br>
Step 2: Copy the fgdb file on the mapServer server inside a folder under ./wms/data<br>
  * File needs to have the same name as the mxd
 
Step 3: Run convertMXD.py with is 3 arguments<br>
* 1: Local mxd folder path (e.g. C:/Users/me/Documents/mxd/900A/)<br>
* 2: Local mxd file name with extension (e.g. 900A.mxd)<br>
* 3: The folder where is located the fgdb file (created at step 2, e.g. 900A)<br>

Step 4: If your service contains picture symbol, images will be created inside the local folder.<br>
* Copy the images to the mapServer server (.wms/data/"step 2 folder"/img)<br>

Step 5: Copy the file to (./wms) and test the service<br>


# known issues

The program may fail if he doesn't find a values from one of his lookup table (./common/lookup.py).<br>
* For EPSG:<br>
   * Inside epsgDict dictionnary, only add the missing key/value (ESRI code/EPSG code)<br>
* For font:<br>
   * Go to: Control Panel\All Control Panel Items\Fonts (copy this path to a file explorer)
      * Find the proper font file
      * Right click and copy the font file to mapServer server (./wms/etc/fonts/fonts)<br>
   * Edit .wms/etc/fonts/fonts.list to add the missing font (font name        font file)<br>
   * Inside fontDict dictionnary, add the missing key/value (font name/font file name)<br>
