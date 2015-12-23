import os
import shutil
import arcpy
from arcpy import env

from values import classify_dictionary

def index_lookup(raster_name):
    ''' Builds string (key) to index value from classify_dictionary'''
    variable_list = ['pr', 'tasmin', 'tasmax', 'pet', 'gdd0', 'gdd3', 'gdd5','gdd10', 'coldestnight', 'freezefreeday', 'prpercent', 'rhsmax', 'rhsmin', 'rsds', 'was']
    #scenarios = ['rcp45', 'historical', 'rcp85']
    month_ranges = ['ANN', 'DJF', 'MAM', 'JJA', 'SON']
    #year_ranges = ['20102039', '20702099', '19712000', '20402069']

    index_string = ''
    print raster_name
    for variable in variable_list:
    	if variable in raster_name.lower().split('_'):
    	    index_string += variable.lower() + "_"
    for month_range in month_ranges:
        if month_range.lower() in raster_name.lower():
            index_string += month_range.lower() + "_"
    for v in ['gdd0', 'gdd3', 'gdd5','gdd10', 'coldestnight', 'freezefreeday']:
            if v in raster_name.lower():
                    index_string += 'ann_'

    if 'vs' in raster_name.lower():
        index_string += 'dif'
    else:
        index_string += 'raw'


    return index_string

    


# Name of file geodatabase
file_geodatabase_name = "classified.gdb"

# Path to tooldata folder
tooldata_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata'))

fgdb = os.path.abspath(os.path.join(tooldata_folder, file_geodatabase_name))

if arcpy.Exists(fgdb):
	print "Exists... removing and making a new file geodatabase"
	shutil.rmtree(fgdb)
	# Make classified file geodatabase
	arcpy.CreateFileGDB_management(tooldata_folder, file_geodatabase_name)
else:
    # Make classified file geodatabase
    arcpy.CreateFileGDB_management(tooldata_folder, file_geodatabase_name)

print classify_dictionary


# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")

# Set folder absolute paths
input_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'conversion_layers'))
output_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'classified.gdb'))
unconverted_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_layers'))
arcpy.env.workspace = input_folder
raster_list = arcpy.ListRasters()

#print raster_list

for layer in raster_list:
        # Local variables:
        unconverted_list = ['freezefreeday', 'prpercent', 'rhsmin', 'rhsmax', 'rsds']

        input_raster = os.path.abspath(os.path.join(input_folder, layer))
        for unconverted in unconverted_list:
            if unconverted in layer:
                input_raster = os.path.abspath(os.path.join(unconverted_folder, layer))

        esri_grid_name = layer[:-4]
        output_raster = os.path.abspath(os.path.join(output_folder, esri_grid_name))
        index_string = index_lookup(esri_grid_name)
        print input_raster
        print index_string
        print classify_dictionary[index_string]
        # Classify and save raster
        classified_raster = arcpy.sa.Reclassify(input_raster, "Value", classify_dictionary[index_string], "NODATA")
        classified_raster.save(output_raster)





