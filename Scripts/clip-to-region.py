import arcpy
import os
import shutil
from arcpy import env
from arcpy.sa import *


if arcpy.CheckExtension("Spatial") == "Available":
    arcpy.AddMessage("Checking out Spatial")
    arcpy.CheckOutExtension("Spatial")
else:
    arcpy.AddError("Unable to get spatial analyst extension")
    arcpy.AddMessage(arcpy.GetMessages(0))
    sys.exit(0)

# Climate Hub file geodatabase path
feature_dataset_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'ClimateHub.gdb', 'Regions'))
netcdf_layer_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'classified.gdb'))



# Make netcdf_clipped_layers folder to store clipped geotiff files if it does not exist
#netcdf_clipped_layers = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'clipped_netcdf_layers'))
#if os.path.exists(netcdf_clipped_layers):
#    pass
#else:
#    os.mkdir(netcdf_clipped_layers )

# Name of file geodatabase
file_geodatabase_name = "clipped.gdb"

# Path to tooldata folder
tooldata_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata'))

fgdb = os.path.abspath(os.path.join(tooldata_folder, file_geodatabase_name))

netcdf_clipped_layers = fgdb

if arcpy.Exists(fgdb):
	print "Exists... removing and making a new file geodatabase"
	shutil.rmtree(fgdb)
	# Make classified file geodatabase
	arcpy.CreateFileGDB_management(tooldata_folder, file_geodatabase_name)
else:
    # Make classified file geodatabase
    arcpy.CreateFileGDB_management(tooldata_folder, file_geodatabase_name)


arcpy.env.workspace = netcdf_layer_folder
netcdf_layers = arcpy.ListRasters()

#netcdf_layers = [x for x in os.listdir(netcdf_layer_folder) if x.endswith('.tif')]
#print netcdf_layers, len(netcdf_layers)

env.workspace = feature_dataset_path 
fcList = arcpy.ListFeatureClasses()

# Clip rasters to each fc (region in feature dataset)
for fc in fcList:
    print fc
    for netcdf in netcdf_layers:
        print fc, netcdf
        if fc == "PNW":
            raster_layer = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'classified.gdb', netcdf))
            rectExtract = arcpy.sa.ExtractByRectangle(raster_layer, "-124.792995 41.5 -109.5 49.415758", "INSIDE")
            rectExtract.save(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', netcdf_clipped_layers, fc + '_' + netcdf)))

        else:
            outExtractByMask = ExtractByMask(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'classified.gdb', netcdf)), fc)
            outExtractByMask.save(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', netcdf_clipped_layers, fc + '_' + netcdf))) 
    

arcpy.CheckInExtension("Spatial")
