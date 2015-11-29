import arcpy
import os
from arcpy import env


def get_min_max(raster_file):
	
    # Read in raster properties
    minimum = arcpy.GetRasterProperties_management(raster_file, "MINIMUM")
    # Get the minimum value from geoprocessing result object
    minimum_result = minimum.getOutput(0)

    # Read in raster properties
    maximum = arcpy.GetRasterProperties_management(raster_file, "MAXIMUM")
    # Get the minimum value from geoprocessing result object
    maximum_result = maximum.getOutput(0)

    return minimum_result, maximum_result



# Get feature class names from feature Regions dataset
feature_dataset_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'ClimateHub.gdb', 'Regions'))
env.workspace = feature_dataset_path 
fcList = arcpy.ListFeatureClasses()
regions = [fc for fc in fcList]

# Path to clipped files
netcdf_clipped_layers = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'clipped_netcdf_layers'))

# Hold min,max value for each region/variable
master_list = []

# List of all variables
variables = ['pr', 'tasmin', 'tasmax', 'pet', 'gdd0', 'coldestnight', 'freezefreeday']

# Get path to all clipped raster layers
all_clipped_layers = [x for x in os.listdir(netcdf_clipped_layers) if x.endswith('.tif')]
#print all_clipped_layers

for region in regions:
    print region
    for variable in variables:
        print region, variable
        # Group of region and variable
        layer_group = []
        for layer in all_clipped_layers:
            if layer.startswith("%s_macav2metdata_%s" % (region, variable)):
                #print layer
                min_max = get_min_max( os.path.abspath(os.path.join(netcdf_clipped_layers, layer)))
                #print min_max
                layer_group.append(min_max)
        overall_min = min([float(x[0]) for x in layer_group])
        overall_max = max([float(x[1]) for x in layer_group])
        data = [region, variable, overall_min, overall_max]
        master_list.append(data)

#print master_list

# Convert all items to string
region_to_string = [str(x[0]) for x in master_list]
variable_to_string = [str(x[1]) for x in master_list]
min_to_string = [str(x[2]) for x in master_list]
max_to_string = [str(x[3]) for x in master_list]
min_max_file_path = feature_dataset_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Doc','regional-min-max.txt'))

# Write to /Doc/regional-min-max.txt
f = open(min_max_file_path, 'w+')
f.write("region,variable,min,max\n")
for i in range(len(region_to_string)):
    f.write('%s,%s,%s,%s\n' % (region_to_string[i], variable_to_string[i], min_to_string[i], max_to_string[i]))
f.close()




