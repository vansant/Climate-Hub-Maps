""" Scripts used to bypass arcgis memopy leaks - calls this script from a loop to clear memory"""



import sys

import arcpy
script_name = sys.argv[0]

# Set local variables
inNetCDFFile = sys.argv[1]
variable = sys.argv[2]
outRasterLayer = sys.argv[3]

print sys.argv[1]
print sys.argv[2]
print sys.argv[3]
XDimension = "lon"
YDimension = "lat"
bandDimmension = ""
dimensionValues = ""
valueSelectionMethod = ""

arcpy.MakeNetCDFRasterLayer_md(inNetCDFFile, variable, XDimension, YDimension, outRasterLayer, bandDimmension, dimensionValues,valueSelectionMethod)
arcpy.CopyRaster_management(outRasterLayer, outRasterLayer+'.tif')