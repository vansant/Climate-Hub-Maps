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
ClimateHub.gdb contains a feature dataset called Regions in WGS 84 (same as NetCDF Raster Layers). The Vector state boundaries are from the 2015 US CENSUS TIGER LINES http://www2.census.gov/geo/tiger/TIGER2015/STATE/tl_2015_us_state.zip

downloaded_netcdf_files/ 
Folder holds downloaded 30 year averaged NetCDF Summary Layers downloaded from NKN Northwest Knowledge Network via HTTP protocol

downloaded_netcdf_layers/ 
Folder than contains all geotiff (raster) layers for the downloaded NetCDF Files

clipped_netcdf_layers/ 
Folder than contains all clipped geotiff (raster) layers for each feature class region in the Region feature dataset in ClimateHub.gdb

/lyr
Folder that contains the .lyr styles for each region-variable combination. For example Idaho-pr.lyr is the .lyr file containg the symbology to be applied to all precipitation layers which were clipped to the Idaho region.

# /Scripts Folder
/requests 
 Python HTTP Requests for Humans™ module from Kenneth Reitz
 https://github.com/kennethreitz/requests

 - ./download-data.py - downloads/updates NetCDF summary layer datasets into downloaded_netcdf_files folder

 - ./netcdf-to-raster.py - converts netcdf files to raster (geotiff layers) as stores them in /Tooldata/downloaded_netcdf_layers/ 

 - ./mywrapper.py - runs a new process for each command

 - ./unit-conversion.py -  script that applies unit conversion to raw raster layers and stores them in /Tooldata/conversion_layers

 - ./clip-to-region.py - clips each raster layer to each region (Idaho, Washington, Oregon, Pacfic Northwest PNW). If Region is PNW the clip is to a spatial extent of -124.792995 41.5 -109.5 49.415758 (WGS 84). The other clip methods are extract by mask using the feature class layers in ClimateHub.gdb/Regions

 - ./classify-rasters.py - classifies rasters based strings contained in a Python dictionary in /ToolData/style/classifieddata.txt

 - ./get-clipped-statistics.py - get the min, max, mean, and standard devation (std) values for each region for each variable. Usefully in providing consistent color ramp across space and time for each region/variable. Values stored in /Doc/regional-statistics.txt as comma separated values region,variable,min,max, mean, std

- ./make-maps.py - script that loops over each regional map document (Idaho, Washington, Oregon, PNW) and over all clipped raster layers (all variables and time periods). Each layer is added to the map document, a style is applied from a .lyr file, and then the map is exported as a pdf to /Doc/maps. There are over 600 maps procuded



General workflow overview

This tool requires the spatial analysis extension and was written to work with ArcGIS 10.3

1. Download or update NetCDF datasets to /Tooldata using download-data.py
  - Data is downloaded/updated using requests module into Tooldata/downloaded_netcdf_files/
2. Data converted from NetCDF to Raster layers using netcdf-to-raster.py
  - Data gets converted using the make netcdf raster layer tool and stored in Tooldata/downloaded_netcdf_layers/
  - mywrapper.py - used beacause ArcGIS was complaining about running out of memory (not an issue in 10.2 using same methods) and it would not loop through all files at the same time. A little hacky/slow but works perfectly.
3. Layers get unit conversions applied
  - variable units and unit conversions
    pr - from millimeters to inches
      inch = mm * 0.0393701 
    tasmin and tasmax - from kelvin to fahrenheit
      °F = (°K * 9/5.) - 459.67
    pet - from millimeters to inches
      inch = mm * 0.0393701 
    gdd0, gdd3, gdd5, gdd10 - from celcius to fahrenheit
      °F = 9/5 × (°C) + 32
    coldestnight - from kelvin to fahrenheit
      °F = (°K * 9/5.) - 459.67
    freezefreeday - no change units in days
    prpercent - no change units in percent departure from 1971-2000 normal
    rhsmin and rhsmax - no change units in percent
    rsds - no change units in W/m2
    was - m/s (meters per second) to mph (miles per hour)
      mph = m/s * 2.237

    If a summary layer is vs the normal period and also temperature the conversion is
    to multiple the original nummbers by 1.8

4. Raster layers clipped to regions Idaho, Oregon, Washington and Pacific Northwest. 
  - Done using clip-to-region.py which uses the extract by mask (requires spatial analyist extension) analysis tool for each each raster layer and for each region in the Feature Dataset (Regions) in ClimateHub.gdb. If Region is PNW the clip is to a spatial extent of -124.792995 41.5 -109.5 49.415758 (WGS 84).
  - Each new clipped layer begins with the name of the feature class and then the name of the raster layer file follows.

5. Classify rasters with classify-rasters.py

6. Create .clr color ramp for each variable using style.txt and generate-clr.py

7. Create mxd for each region with layout view elements set up for a each MXD
  - Layout of elements can be updated for mxd and maps can be regenerated
  - Create Idaho.mxd, Oregon.mxd, Washington.mxd, PNW.mxd 
8. Run make-maps.py which processes all clipped raster layer
  - Adds layer to regional mxd file
  - Applies symbology from region-variable.lyr file
  - Save as a PDF into /Doc/maps