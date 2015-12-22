import os
import arcpy

def clr_lookup(raster_name):
    ''' Builds string to point to correct .clr file for each varibale'''
    variable_list = ['pr', 'tasmin', 'tasmax', 'pet', 'gdd0', 'gdd3', 'gdd5','gdd10', 'coldestnight', 'freezefreeday', 'prpercent', 'rhsmax', 'rhsmin', 'rsds', 'was']
    month_ranges = ['ANN', 'DJF', 'MAM', 'JJA', 'SON']
  
    index_string = ''
    #print raster_name
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

    index_string+=".clr"
    return index_string

# Name of file geodatabase
file_geodatabase_name = "clipped.gdb"

# Path to tooldata folder
tooldata_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata'))

fgdb = os.path.abspath(os.path.join(tooldata_folder, file_geodatabase_name))


arcpy.env.workspace = fgdb
raster_list = arcpy.ListRasters()

#print raster_list

# Establish absolute folder paths
style_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'style'))


for layer in raster_list:
    # Path to .clr file
    print layer
    clr_name = clr_lookup(os.path.abspath(os.path.join(fgdb, layer)))
    clr_file = os.path.abspath(os.path.join(style_folder, clr_name))
    if os.path.isfile(clr_file):
        classified_raster_file =  os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'clipped.gdb', layer))
        # Apply .clr symbology
        arcpy.AddColormap_management(classified_raster_file, '', clr_file)
    else:
        print "Missing .clr for %s" % layer







