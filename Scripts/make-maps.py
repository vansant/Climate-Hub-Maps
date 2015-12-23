""" Script that styles geotiff layers, and then saves a map document to a pdf"""
import os
import arcpy
from arcpy import env

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

# Main project folder of the / top level folder for the project
project_root = os.path.abspath(os.path.join(os.path.dirname( __file__ )))

# List files in project root folder
project_root_files = os.listdir(project_root)

# Establish absolute folder paths
style_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Tooldata', 'style'))


# List of all map document files in project root
#mxd_list = [x for x in project_root_files if x.endswith(".mxd")]
#print "Found the following mxd files: %s" % mxd_list

# Path to clipped files
netcdf_clipped_layers = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Tooldata', 'clipped.gdb'))

# List of all variables
#variables = ['pr', 'tasmin', 'tasmax', 'pet', 'gdd0', 'coldestnight', 'freezefreeday']

# Get path to all clipped raster layers
#all_clipped_layers = [x for x in os.listdir(netcdf_clipped_layers) if x.endswith('.tif')]

arcpy.env.workspace = netcdf_clipped_layers
raster_list = arcpy.ListRasters()
all_clipped_layers = raster_list
#print raster_list

# Get feature class names from feature Regions dataset
#feature_dataset_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Tooldata', 'ClimateHub.gdb', 'Regions'))
#env.workspace = feature_dataset_path 
#fcList = arcpy.ListFeatureClasses()
#regions = [fc for fc in fcList]

mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
for layer in raster_list:
    
    if 'gdd10' in layer and 'PNW' in layer:
	    netcdf_layer = os.path.abspath(os.path.join(netcdf_clipped_layers, layer))
	    #print "loading in %s layer" % layer
	    #layer_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Tooldata', 'clipped.gdb', layer))
	    #addLayer = arcpy.mapping.Layer(r'%s' % netcdf_layer)
	    #arcpy.mapping.AddLayer(df, addLayer, "TOP")
	    clr_name = clr_lookup(os.path.abspath(os.path.join(netcdf_clipped_layers, layer)))
	    clr_file = os.path.abspath(os.path.join(style_folder, clr_name))
	    print clr_file
	    if os.path.isfile(clr_file):
	        classified_raster_file =  os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'Tooldata', 'clipped.gdb', layer))
	        # Apply .clr symbology
	        arcpy.AddColormap_management(classified_raster_file, '', clr_file)
	    else:
	        print "Missing .clr for %s" % layer
	    
# Path to .lyr files
#lyr_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'lyr'))

# Set environment to project root
#env.workspace = project_root

# Loop through all regions
#for region in regions:
#
#    # Loop through all variables
#    for variable in variables:
#        print "Processing: %s-%s" % (region, variable)
#
#        # Build .lyr name to match those in lyr fodler
#        lyr_file = '%s_%s.lyr' % (region, variable)
#        print "Will use %s for styling" % lyr_file
#
#        # Group of region and variable
#        layer_group = []
#        for layer in all_clipped_layers:
#            if layer.startswith("%s_macav2metdata_%s" % (region, variable)):
#                layer_group.append(layer)            
#
#        # Process each Layer group
#        for layer_name in layer_group:
#            
#            # Set mxd name
#            mxd = "%s.mxd" % region
#            print "opening %s" % mxd
#        
#            # get name of clipped NetCDF raster file
#            netcdf_layer = os.path.abspath(os.path.join(netcdf_clipped_layers, layer_name))
#            print "loading in %s layer" % netcdf_layer
#
#            # Name of pdf output
#            pdf_name = layer_name[:-4] + ".pdf"
#
#            # Full path to .lyr file
#            lyr_file = os.path.abspath(os.path.join(lyr_folder , lyr_file))
#            print "loading %s for .lyr styling" % lyr_file
#
#            # Setup map document
#            mxd = arcpy.mapping.MapDocument(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', mxd)))
#            df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
#
#            # Add the clipped raster layer, apply symbology, and save as pdf file
#            addLayer = arcpy.mapping.Layer(r'%s' % netcdf_layer)  
#            arcpy.mapping.AddLayer(df, addLayer, "TOP")
#            sourceLayer = arcpy.mapping.Layer(r"%s" % lyr_file )
#            updateLayer = arcpy.mapping.ListLayers(mxd, "*", df)[0]
#            print "applying %s style to %s" % (lyr_file, netcdf_layer)
#            arcpy.ApplySymbologyFromLayer_management(updateLayer ,sourceLayer)
#            arcpy.RefreshTOC()
#            arcpy.RefreshActiveView()
#            arcpy.mapping.ExportToPDF(mxd, os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Doc', 'maps', pdf_name)))
#            print "Exported map %s to /Doc/maps folder" % pdf_name
#            del mxd, sourceLayer
