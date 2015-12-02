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

# Climate Hub file geodatabase path
feature_dataset_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'ClimateHub.gdb', 'Regions'))
netcdf_layer_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_layers'))
env.workspace = feature_dataset_path 
fcList = arcpy.ListFeatureClasses()


# Make netcdf_clipped_layers folder to store clipped geotiff files if it does not exist
netcdf_clipped_layers = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'clipped_netcdf_layers'))
if os.path.exists(netcdf_clipped_layers):
    pass
else:
    os.mkdir(netcdf_clipped_layers )

netcdf_layers = [x for x in os.listdir(netcdf_layer_folder) if x.endswith('.tif')]
print netcdf_layers, len(netcdf_layers)



# Clip rasters to each fc (region in feature dataset)
for fc in fcList:
    print fc
    for netcdf in netcdf_layers:
        print fc, netcdf
        if fc == "PNW":
            #rectExtract = arcpy.sa.ExtractByRectangle(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_layers', netcdf)), "-124.792995 41.5 -109.5 49.415758", "INSIDE")
            #print rectExtract
            #rectExtract.save(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', netcdf_clipped_layers, fc + '_' + netcdf[:-4] + '.tif')))
            #arcpy.sa.RasterCalculator("\"%%s%\" * 0.0393701" % rectExtract , os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', netcdf_clipped_layers, fc + '_' + netcdf[:-4] + '.tif')))
            raster_layer = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_layers', netcdf))
            rectExtract = arcpy.sa.ExtractByRectangle(conversion, "-124.792995 41.5 -109.5 49.415758", "INSIDE")
            rectExtract.save(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', netcdf_clipped_layers, fc + '_' + netcdf[:-4] + '.tif')))
            

        else:
            outExtractByMask = ExtractByMask(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_layers', netcdf)), fc)
            outExtractByMask.save(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', netcdf_clipped_layers, fc + '_' + netcdf[:-4] + '.tif'))) 
    

arcpy.CheckInExtension("Spatial")
