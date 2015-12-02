# -*- coding: cp1252 -*-
import arcpy
import os
from arcpy import env
from arcpy.sa import *


if arcpy.CheckExtension("Spatial") == "Available":
    arcpy.AddMessage("Checking out Spatial")
    arcpy.CheckOutExtension("Spatial")
else:
    arcpy.AddError("Unable to get spatial analyst extension")
    arcpy.AddMessage(arcpy.GetMessages(0))
    sys.exit(0)

# Path to raw raster layer files
raster_layer_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_layers'))

# Make conversion_layers folder to store unit conversion geotiff files if it does not exist
conversion_layers_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'conversion_layers'))
if os.path.exists(conversion_layers_path):
    pass
else:
    os.mkdir(conversion_layers_path)

# Get all raw netcdf raster layers
netcdf_layers = [x for x in os.listdir(raster_layer_folder) if x.endswith('.tif')]
print netcdf_layers, len(netcdf_layers)

# List of layers that do not need unit conversions and will be copied into conversion folder
copy_list = []

# Process each layer and perform a unit conversion if necessary
for netcdf in netcdf_layers:
    raw_raster_layer = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_layers', netcdf))
    conversion_layer = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'conversion_layers', netcdf))


    try:
        if 'pr' in netcdf.split('_'):
            print "you got pr"
            conversion = arcpy.sa.Raster(raw_raster_layer) * 0.0393701
        if 'tasmin' in netcdf.split('_'):
            print "you got tasmin"
            conversion = arcpy.sa.Raster(raw_raster_layer) * 9/5. - 459.67
        if 'tasmax' in netcdf.split('_'):
            print "you got tasmax"
            conversion = arcpy.sa.Raster(raw_raster_layer) * 9/5. - 459.67
        if 'pet' in netcdf.split('_'):
            print "you got pet"
            conversion = arcpy.sa.Raster(raw_raster_layer) * 0.0393701
        if 'gdd0' in netcdf.split('_'):
            print "you got gdd0"
            conversion = arcpy.sa.Raster(raw_raster_layer) * 9/5 + 32
        if 'gdd3' in netcdf.split('_'):
            print "you got gdd3"
            conversion = arcpy.sa.Raster(raw_raster_layer) * 9/5 + 32
        if 'gdd5' in netcdf.split('_'):
            print "you got gdd5"
            conversion = arcpy.sa.Raster(raw_raster_layer) * 9/5 + 32
        if 'gdd10' in netcdf.split('_'):
            print "you got gdd10"
            conversion = arcpy.sa.Raster(raw_raster_layer) * 9/5 + 32   
        if 'coldestnight' in netcdf.split('_'):
            print "you got coldestnight"
            conversion = arcpy.sa.Raster(raw_raster_layer) * 9/5. - 459.67
        if 'was' in netcdf.split('_'):
            print "you got was"
            conversion = arcpy.sa.Raster(raw_raster_layer) * 2.237

    
    #conversion = arcpy.sa.Raster(raw_raster_layer) * 0.0393701
        conversion.save(conversion_layer)
    except:
        if 'freezefreeday' in netcdf.split('_'):
            copy_list.append(netcdf)
        if 'prpercent' in netcdf.split('_'):
            copy_list.append(netcdf)
        if 'rhsmin' in netcdf.split('_'):
            copy_list.append(netcdf)
        if 'rhsmax' in netcdf.split('_'):
            copy_list.append(netcdf)
        if 'rsds' in netcdf.split('_'):
            copy_list.append(netcdf)
        
    

arcpy.CheckInExtension("Spatial")

# Copy over layers that did not need a unit converion
for copy_file in copy_list:
    #print copy_file
    arcpy.CopyRaster_management(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_layers', copy_file)), os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'conversion_layers', copy_file)))

