# Climate-Hub-Maps
ArcGIS Map Automation for Climate Hub Mapping Project

# /Tooldata folder
./ClimateHub.gdb contains a feature dataset called Regions in WGS 84 (same as NetCDF Raster Layers). The Vector state boundaries are from the 2015 US CENSUS TIGER LINES http://www2.census.gov/geo/tiger/TIGER2015/STATE/tl_2015_us_state.zip

downloaded_netcdf_files/ 
Folder holds downloaded 30 year averaged NetCDF Summary Layers downloaded from NKN Northwest Knowledge Network via HTTP protocol

# /Scripts Folder
./requests 
 Python HTTP Requests for Humans™ module from Kenneth Reitz
 https://github.com/kennethreitz/requests

./download-data.py - downloads/updates NetCDF summary layer datasets into downloaded_netcdf_files folder

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