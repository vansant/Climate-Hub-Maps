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

clipped_netcdf_layers/ 
Folder than contains all clipped geotiff (raster) layers for each feature class region in the Region feature dataset in ClimateHub.gdb


# /Scripts Folder
./requests 
 Python HTTP Requests for Humans™ module from Kenneth Reitz
 https://github.com/kennethreitz/requests

 - ./download-data.py - downloads/updates NetCDF summary layer datasets into downloaded_netcdf_files folder

 - ./netcdf-to-raster.py - converts netcdf files to raster (geotiff layers) as stores them in /Tooldata/downloaded_netcdf_layers/ 

 - ./mywrapper.py - runs a new process for each command

 - ./clip-to-region.py - clips each raster layer to each region (Idaho, Washington, Oregon, Pacfic Northwest PNW).

 - ./get-clipped-min-and-max.py - get the min and max values for each region for each variable. Usefully in providing consistent color ramp across space and time for each region/variable. Values stored in /Doc/regional-min-max.txt as comma separated values region,variable,min,max

General workflow overview

This tool requires the spatial analysis extension and was written to work with ArcGIS 10.3

1. Download or update NetCDF datasets to /Tooldata using download-data.py
  - Data is downloaded/updated using requests module into Tooldata/downloaded_netcdf_files/
2. Data converted from NetCDF to Raster layers using netcdf-to-raster.py
  - Data gets converted using the make netcdf raster layer tool and stored in Tooldata/downloaded_netcdf_files/
  - mywrapper.py - used beacause ArcGIS was whining about running out of memory and it would not look through all files at the same time. A little hacky/slow but works perfectly.
3. Raster layers clipped to regions Idaho, Oregon, Washington and Pacific Northwest. 
  - Done using clip-to-region.py which uses the extract by mask (requires spatial analyist extension) analysis tool for each each raster layer and for each region in the Feature Dataset (Regions) in ClimateHub.gdb.
  - Each new clipped layer begines with the name of the feature class and then the name of the raster layer file follows.
4. Min and max values grabbed from all clipped layers to aid with setting up .lyr files for each spatial/temporal visual anlysis
5. Create .lry color ramp by right clicking then exporting .lyr file for each raster layer group. Region,
  - Min and max for each region and variable via get-clipped-min-and-max.py - used as simple guid for color ramp and could actaully anything the user wants.
  - Setup color ramp in ArcMap gui GUI and export region_variable.lyr file to /lyr folder
  - Layers for each region can be updated in the future to remake the maps
6. Create mxd for each region with layout view elements set up for a map
  - Layout of elements can be updated for mxd and maps can be regenerated
7. Add layer to regional mxd file
8. Apply symbology from .lyr file
9. Save as a PDF
10. Loop through all layers and generate pdf maps