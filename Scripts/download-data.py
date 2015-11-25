""" Script to download/update summary layers"""

import requests
import os

def download_summary_layer(layer_url, stream=True):
    """ Save NetCDF to file from HTTP URL"""

    print("Downloading %s" % layer_url)
    r = requests.get(layer_url)

    if r.status_code == 200:
        # Get name of NetCDF File
        filename = layer_url.split("/")[-1]
        netcdf_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'summary_layers', filename))
        print "%s downloaded successfully" % layer_url
        # Write File to disk
        with open(netcdf_file, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)
    else:
        print "Error %s" % r.status_code
        print "Was not able to download file %s" % layer_url
        
    
# URL Parameters
variable_list = ['pr', 'tasmin', 'tasmax', 'pet', 'gdd0', 'coldestnight', 'freezefreeday']
scenarios = ['rcp45', 'historical', 'rcp85']
month_ranges = ['ANN', 'DJF', 'MAM', 'JJA', 'SON']
year_ranges = ['20102039', '20702099', '19712000', '20402069']

# Hold all possible URLs
url_list = []

for variable in variable_list:
    for scenario in scenarios:
        for month_range in month_ranges:
            for year_range in year_ranges:
                url = "http://thredds.northwestknowledge.net:8080/thredds/fileServer/NWCSC_INTEGRATED_SCENARIOS_ALL_CLIMATE/projections/macav2metdata/macav2metdata_%s_%s_%s_%s_20CMIP5ModelMean.nc" % (variable, month_range, year_range, scenario)
                url_list.append(url)


for url in url_list:
    download_summary_layer(url)
