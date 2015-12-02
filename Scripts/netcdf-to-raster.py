""" Script to convert netcdf files in a folder to raster (geotiff)"""

import os
import arcpy
import sys

netcdf_layers_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_layers'))
netcdf_files_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_files'))

# Make layers folder to store NetCDF files if it does not exist
if os.path.exists(netcdf_layers_folder):
    pass
else:
    os.mkdir(netcdf_layers_folder )

# List of netcdf files
netcdf_files = [netcdf_file for netcdf_file in os.listdir(netcdf_files_folder)]

# Variable names in filename and the variable name in the NetCDF files are different so a mapping is used
variable_list =  ['pr', 'tasmin', 'tasmax', 'pet', 'gdd0', 'gdd3', 'gdd5','gdd10', 'coldestnight', 'freezefreeday', 'prpercent', 'rhsmax', 'rhsmin', 'rsds', 'was']
variable_mapping = {'pr':'precipitation', 'tasmin':'air_temperature', 'tasmax':'air_temperature', 'pet':'pet', 'gdd0':'growing_degree_days', 'gdd3':'growing_degree_days', 'gdd5':'growing_degree_days', 'gdd10':'growing_degree_days', 'coldestnight':'air_temperature', 'freezefreeday':'freeze_free_days', 'prpercent':'pon', 'rhsmax': 'relative_humidity', 'rhsmin':'relative_humidity', 'rsds':'surface_downwelling_shortwave_flux_in_air','was':'wind_speed'}

for netcdf in netcdf_files:
    # Set local variables
    inNetCDFFile = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_files', netcdf))

    # Set correct variable name
    for v in variable_list:
        if v in netcdf.split("_"):
            variable = variable_mapping[v]
    XDimension = "lon"
    YDimension = "lat"
    outRasterLayer = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_layers', netcdf[:-3]))
    bandDimmension = ""
    dimensionValues = ""
    valueSelectionMethod = ""

    print inNetCDFFile
    #print outRasterLayer

    try:
        # Execute MakeNetCDFRasterLayer
        #arcpy.MakeNetCDFRasterLayer_md(inNetCDFFile, variable, XDimension, YDimension, outRasterLayer, bandDimmension, dimensionValues,valueSelectionMethod)
        #arcpy.CopyRaster_management(outRasterLayer, outRasterLayer+'.tif')

        python_path = sys.executable
        script_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'mywrapper.py'))

        if os.path.isfile(outRasterLayer+'.tif'):
            print "%s exists" % outRasterLayer
        else:
            os.system("%s %s %s %s %s" %(python_path, script_path, inNetCDFFile, variable, outRasterLayer))

    except:
        print "could not make layer"
        print arcpy.GetMessages()
        break
        
