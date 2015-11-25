# Climate-Hub-Maps
ArcGIS Map Automation for Climate Hub Mapping Project

# /Tooldata folder
tl_2015_us_state.shp - Vector state boundaries from 2015 US CENSUS TIGER LINES http://www2.census.gov/geo/tiger/TIGER2015/STATE/tl_2015_us_state.zip

Folder holds downloaded NetCDF Summary Layers

# /Scripts Folder
./requests folder
 Python HTTP Requests for Humans™ module from Kenneth Reitz
 https://github.com/kennethreitz/requests

download-data.py - downloads/updates NetCDF summary layer datasets

General workflow overview

1. Download or update NetCDF datasets to /Tooldata using download-data.py
  - Data is downloaded/updated using requests module
2. Data converted from NetCDF to Raster layers using MakeNetCDFRaster Layer tool
3. Raster layers clipped to regions Idaho, Oregon, Washington and Pacific Northwest. 
4. Clipped Raster layers exported to file geodatabase
5. Min and max values grabbed from all files after conversion from metric units
6. Create .rtf.xml for color ramp export by right clicking then exporting rtf xml file
7. Added layer to mxd file
8. Apply symbology
9. Save as a PDF