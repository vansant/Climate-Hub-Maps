# Climate-Hub-Maps
ArcGIS Map Automation for Climate Hub Mapping Project
Project Description: This joint venture between the University of Idaho (UI) and the PNW Regional Climate Hub will create a web-based, digital resource that provides downscaled, simple, current and projected climate maps of the PNW region. 

Static, downloadable maps will feature 6 climate metrics of interest to land managers. These metrics include: temperature, precipitation, freeze-free days, cold hardiness zones, accumulated growing degree days, and reference evapotranspiration. Climatic variables will be presented based on current conditions and under RCP 4.5 and will average findings across climate models for each metric. If time and resources permit, maps will also be generated based on the RCP 8.5. Users will have access to maps that feature information about the climatic metrics for the entire PNW region and each state in the region (e.g., ID, WA and OR) for four time periods (1981-2010, 2011-2040, 2041-2070 and 2070-2099). Specifically we will produce maps of:
(1)	Mean maximum and minimum temperature for annual, Dec-Feb, Mar-May, Jun-Aug, Sep-Nov
(2)	Accumulated precipitation for annual, Dec-Feb, Mar-May, Jun-Aug, Sep-Nov
(3)	Reference ET for annual, Dec-Feb, Mar-May, Jun-Aug, Sep-Nov
(4)	Freeze-free days 
(5)	Cold Hardiness Zones
(6)	Growing degree days (base 0C)

Maps generated will be viewable on computers, tablets or mobile phones. Use of these resources will help PNW farmers, land managers, and advisors visualize and understand climatic variability within the region, under current conditions and as projected based on climate models and emission scenarios.

Development of these user-focused maps will support transitioning to a larger, regional focus and enhance utility of current and future climate change and agriculture related projects and the Climate Hub.


# /Tooldata folder
./ClimateHub.gdb contains a feature dataset called Regions in WGS 84 (same as NetCDF Raster Layers). The Vector state boundaries are from the 2015 US CENSUS TIGER LINES http://www2.census.gov/geo/tiger/TIGER2015/STATE/tl_2015_us_state.zip

downloaded_netcdf_files/ 
Folder holds downloaded 30 year averaged NetCDF Summary Layers downloaded from NKN Northwest Knowledge Network via HTTP protocol

downloaded_netcdf_layers/ 
Folder than contains all geotiff (raster) layers for the downloaded NetCDF Files

# /Scripts Folder
./requests 
 Python HTTP Requests for Humans™ module from Kenneth Reitz
 https://github.com/kennethreitz/requests

./download-data.py - downloads/updates NetCDF summary layer datasets into downloaded_netcdf_files folder
./download-data.py - converts netcdf files to raster (geotiff layers) as stores them in /Tooldata/downloaded_netcdf_layers/ 

General workflow overview

1. Download or update NetCDF datasets to /Tooldata using download-data.py
  - Data is downloaded/updated using requests module into Tooldata/downloaded_netcdf_files/
2. Data converted from NetCDF to Raster layers using netcdf-to-raster.py
  - Data gets converted using the make netcdf raster layer tool and stored in Tooldata/downloaded_netcdf_files/
  - mywrapper.py - used beacause ArcGIS was whining about running out of memory and it would not look through all files at the same time. A little hacky/slow but works perfectly.
3. Raster layers clipped to regions Idaho, Oregon, Washington and Pacific Northwest. 
4. Clipped Raster layers exported to file geodatabase
5. Min and max values grabbed from all files after conversion from metric units
6. Create .rtf.xml for color ramp export by right clicking then exporting rtf xml file
7. Added layer to mxd file
8. Apply symbology
9. Save as a PDF