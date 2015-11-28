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
        netcdf_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_files', filename))
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

# Build URL for files
for variable in variable_list:
    for scenario in scenarios:
        for month_range in month_ranges:
            for year_range in year_ranges:
                if year_range == "19712000" and not scenario == "historical":pass
                elif not year_range == "19712000" and scenario == "historical":pass
                else:
                    if variable in ['gdd0', 'coldestnight', 'freezefreeday']:
                        url = "http://thredds.northwestknowledge.net:8080/thredds/fileServer/NWCSC_INTEGRATED_SCENARIOS_ALL_CLIMATE/projections/macav2metdata/macav2metdata_%s_%s_%s_20CMIP5ModelMean.nc" % (variable, year_range, scenario)
                    else:
                        url = "http://thredds.northwestknowledge.net:8080/thredds/fileServer/NWCSC_INTEGRATED_SCENARIOS_ALL_CLIMATE/projections/macav2metdata/macav2metdata_%s_%s_%s_%s_20CMIP5ModelMean.nc" % (variable, month_range, year_range, scenario)
                    url_list.append(url)


# Make summary_layer folder to store NetCDF files if it does not exist
if os.path.exists(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_files'))):
    pass
else:
    os.mkdir(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_files')))


for url in url_list:
    download_summary_layer(url)
