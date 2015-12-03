""" Script to download/update summary layers"""

import requests
import os

def download_summary_layer(layer_url, stream=True):
    """ Save NetCDF to file from HTTP URL"""

    #print("Downloading %s" % layer_url)
    r = requests.get(layer_url)

    if r.status_code == 200:
        # Get name of NetCDF File
        filename = layer_url.split("/")[-1]
        netcdf_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_files', filename))
        #print "%s downloaded successfully" % layer_url
        # Write File to disk
        with open(netcdf_file, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)
    else:
        print "Error %s" % r.status_code
        print "Was not able to download file %s" % layer_url
        
    
# URL Parameters
variable_list = ['pr', 'tasmin', 'tasmax', 'pet', 'gdd0', 'gdd3', 'gdd5','gdd10', 'coldestnight', 'freezefreeday', 'prpercent', 'rhsmax', 'rhsmin', 'rsds', 'was']
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
                    # Get urls for normal periods
                    if variable in ['gdd0', 'gdd3', 'gdd5','gdd10', 'coldestnight', 'freezefreeday']:
                        url = "http://thredds.northwestknowledge.net:8080/thredds/fileServer/NWCSC_INTEGRATED_SCENARIOS_ALL_CLIMATE/projections/macav2metdata/macav2metdata_%s_%s_%s_20CMIP5ModelMean.nc" % (variable, year_range, scenario)
                        url_list.append(url)
                    else:
                        # Get urls for normal periods
                        # prpercent does not have raw 30 year periods of data as it is a difference of future vs historical only
                        if variable == "prpercent":pass
                        else:
                            url = "http://thredds.northwestknowledge.net:8080/thredds/fileServer/NWCSC_INTEGRATED_SCENARIOS_ALL_CLIMATE/projections/macav2metdata/macav2metdata_%s_%s_%s_%s_20CMIP5ModelMean.nc" % (variable, month_range, year_range, scenario)
                            url_list.append(url)

                            # Historical is not vs historical so pass 
                        if scenario == "historical" or year_range == '19712000':pass

                        else:
                            # Get the difference from normal dataset urls
                            url_differece_from_normal = "http://thredds.northwestknowledge.net:8080/thredds/fileServer/NWCSC_INTEGRATED_SCENARIOS_ALL_CLIMATE/projections/macav2metdata/macav2metdata_%s_%s_%s_%s_vs_19712000_20CMIP5ModelMean.nc" % (variable, month_range, year_range, scenario)
                            url_list.append(url_differece_from_normal)


# Make summary_layer folder to store NetCDF files if it does not exist
if os.path.exists(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_files'))):
    pass
else:
    os.mkdir(os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_files')))


netcdf_files_folder = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'Tooldata', 'downloaded_netcdf_files'))

# See if exists, otherwise download
for url in url_list:
    #print url
    file_name = url.split('/')[-1]
    netcdf_file = os.path.abspath(os.path.join(netcdf_files_folder, file_name))
    #print netcdf_file
    if os.path.exists(netcdf_file):
        print "%s already exists" % netcdf_file
        pass
    else:
        print "Downloading %s" % netcdf_file
        download_summary_layer(url)

