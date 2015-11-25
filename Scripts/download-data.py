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
        netcdf_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', filename))
        print "%s downloaded successfully" % layer_url
        # Write File to disk
        with open(netcdf_file, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)
        
    
# Will be updated later to download all datasets
#variable_list = ['pr', 'tasmin', 'pet', 'rhsmin', 'rsds', 'rhsmax', 'tasmax', 'was']
#variable_dictionary = {'huss':'specific_humidity', 'pr':'precipitation', 'tasmax':'air_temperature', 'rsds':'surface_downwelling_shortwave_flux_in_air', 'tasmin':'air_temperature', 'was':'wind_speed', 'SWE-monday1':'SWE','Evaporation-monsum':'Evaporation','TotalSoilMoist-monmean':'TotalSoilMoisture', 'C_ECOSYS':'C_ECOSYS',  'PART_BURN':'PART_BURN', 'pet':'pet', 'rhsmin':'relative_humidity', 'rhsmax':'relative_humidity'}
#variable_transform = variable_dictionary[variable]
# Enemble of all models for each time frame
#scenarios = ['rcp45', 'historical', 'rcp85']
#models = '20CMIP5ModelMean'
#month_ranges = ['ANN', 'DJF', 'MAM', 'JJA', 'SON']
#year_ranges = ['20102039', '20702099', '19712000', '20402069']

# Test URL
url = "http://thredds.northwestknowledge.net:8080/thredds/fileServer/NWCSC_INTEGRATED_SCENARIOS_ALL_CLIMATE/projections/macav2metdata/macav2metdata_pr_DJF_19712000_historical_20CMIP5ModelMean.nc"

download_summary_layer(url)
