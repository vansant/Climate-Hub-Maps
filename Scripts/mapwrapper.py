import arcpy
import os
# which mxd
# which .lyr
# name of pdf
# name of geotiff

import sys

print "loading"

mxd_name = sys.argv[1]
netcdf_layer_name = sys.argv[2]
lyr_file_name = sys.argv[3]

# Name used to save the pdf file
pdf_name = netcdf_layer_name[:-4] + ".pdf"


mxd = arcpy.mapping.MapDocument(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', mxd_name)))
df = arcpy.mapping.ListDataFrames(mxd, "*")[0]
updateLayer = arcpy.mapping.ListLayers(mxd, "*", df)[0]

# Path to clipped files
netcdf_clipped_layers = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'clipped_netcdf_layers'))

# Path to .lyr files
lyr_file_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'lyr'))

# Input strings
netcdf_layer = os.path.abspath(os.path.join(netcdf_clipped_layers, netcdf_layer_name))
lyr_file = os.path.abspath(os.path.join(lyr_file_path, lyr_file_name))

#addLayer = arcpy.mapping.Layer(r'%s' % netcdf_layer)  
#arcpy.mapping.AddLayer(df, addLayer, "TOP")
sourceLayer = arcpy.mapping.Layer(r"%s" % lyr_file )

arcpy.mapping.UpdateLayer(df, updateLayer, sourceLayer, True)
#mxd.saveACopy(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..','Doc', 'maps', 'IdahoTest.mxd')))
arcpy.RefreshTOC()
arcpy.RefreshActiveView()

#layers = arcpy.mapping.ListLayers(mxd, "*", df)

#layers[0].visible = False

#arcpy.RefreshTOC()
#arcpy.RefreshActiveView()

arcpy.mapping.ExportToPDF(mxd, os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Doc', 'maps', pdf_name)))

del mxd, sourceLayer
