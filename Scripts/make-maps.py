
import os

import arcpy
from arcpy import env

# Main project folder of the / top level folder for the project
project_root = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))

# List files in project root folder
project_root_files = os.listdir(project_root)

# List of all map document files in project root
mxd_list = [x for x in project_root_files if x.endswith(".mxd")]
print mxd_list


# Path to clipped files
netcdf_clipped_layers = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'clipped_netcdf_layers'))

# Hold min,max value for each region/variable
master_list = []

# List of all variables
variables = ['pr', 'tasmin', 'tasmax', 'pet', 'gdd0', 'coldestnight', 'freezefreeday']

# Get path to all clipped raster layers
all_clipped_layers = [x for x in os.listdir(netcdf_clipped_layers) if x.endswith('.tif')]
#print all_clipped_layers

# Get feature class names from feature Regions dataset
feature_dataset_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'ClimateHub.gdb', 'Regions'))
env.workspace = feature_dataset_path 
fcList = arcpy.ListFeatureClasses()
regions = [fc for fc in fcList]

# Path to .lyr files
lyr_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'lyr'))


# Set environment to project root
env.workspace = project_root

for region in regions:
    print region

    # Assign correct mxd
    for mxd in mxd_list:
        if mxd.startswith(region):
            #print mxd
            #mxd = 
            mxd_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', mxd))
    # Loop through variables
    for variable in variables:
        print region, variable
        lyr_file = os.path.abspath(os.path.join( lyr_folder, '%s-%s.lyr' % (region, variable)))
        print lyr_file

        # Group of region and variable
        layer_group = []
        for layer in all_clipped_layers:
            if layer.startswith("%s_macav2metdata_%s" % (region, variable)):
                layer_group.append(layer)
        print layer_group
        #
        # Add raster layer to map
        # Update text datafields
        # Save map as pdf
        for layer_name in layer_group:
            mxd = arcpy.mapping.MapDocument(mxd_path)
            arcpy.mapping.ExportToPDF(mxd, os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Doc', 'maps', '%s.pdf' % layer_name)))

