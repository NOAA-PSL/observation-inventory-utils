import automation_utils as au
import atm_dicts
import yaml_generation as yg
import obs_inv_utils.obs_inv_cli as cli

import argparse
import subprocess
from joblib import Parallel, delayed

from datetime import datetime as dt
from datetime import timedelta
from pandas import Timestamp

#argparse section
parser = argparse.ArgumentParser()
parser.add_argument("-cat", dest="category", help="Category of variables to inventory. Valid options: atmosphere", choices=['atmosphere'], default="atmosphere", type=str)
#parser.add_argument("-p", dest="platform", help="Platform the script is being run on. Valid options: pw, hera", choices=['pw', 'hera'], default="pw", type=str)
parser.add_argument("-ago", dest="days_ago", help="Number of days ago to run the inventory for. If provided, must be positive integer. If not provided, it will run the full extent of the inventory.", default=0, type=int)
args = parser.parse_args()

#get category list
# more categories to be added as they are written as dictionaries 
# remember to add new categories to the argparser options and here
to_inventory = []
if args.category is 'atmosphere':
    to_inventory = atm_dicts.atm_infos 

#need to run correct sh for platform 
# assume this is gonna be done before running the script because I had to do it to run initally
# and don't want to give permission to run these files from this script 
# if args.platform is 'pw':
#     subprocess.run(['./../../obs_inv_utils_pw_cloud.sh'])
# elif args.platform is 'hera':
#     subprocess.run(['./../../obs_inv_utils_hera.sh'])


#define functions to run in parallel 
def run_obs_inventory(inventory_info):
    #EXPAND THIS LATER TO HANDLE TWO DAY RUNS; probably specify end time as part fo the argument options above
    if args.days_ago > 0:
        end = Timestamp.now().round(freq='6H')
        #end = dt.now() # need to get in 0/6/12/18z most recent value 
        end_time = end.strftime(au.DATESTR_FORMAT)
        start = end - timedelta(days=args.days_ago)
        start_time = start.strftime(au.DATESTR_FORMAT)
        print(f'Start time: {start_time}, End time: {end_time}')
    else: #run the full period from start to now
        start_time = inventory_info.start
        #end = dt.now() # need to get this in the 0 / 6 / 12 / 18z most recent value 
        end = Timestamp.now().round(freq='6H')
        end_time = end.strftime(au.DATESTR_FORMAT)

    yaml_file = yg.generate_obs_inv_config(inventory_info, start_time, end_time)
    cli.get_obs_inventory_base(yaml_file)

def run_nceplibs(inventory_info):
    #ADD TWO DAY EXPANSION HERE AS WELL
    if args.days_ago > 0:
        end = Timestamp.now().round(freq='6H')
        #end = dt.now() # need to get in 0/6/12/18z most recent value 
        end_time = end.strftime(au.DATESTR_FORMAT)
        start = end - timedelta(days=args.days_ago)
        start_time = start.strftime(au.DATESTR_FORMAT)
        print(f'Start time: {start_time}, End time: {end_time}')
    else: #run the full period from start to now
        start_time = inventory_info.start
        #end = dt.now() # need to get this in the 0 / 6 / 12 / 18z most recent value 
        end = Timestamp.now().round(freq='6H')
        end_time = end.strftime(au.DATESTR_FORMAT)
    
    #run correct command
    if inventory_info.nceplibs_cmd == au.NCEPLIBS_SINV:
        yaml_file = yg.generate_nceplibs_sinv_inventory_config(inventory_info, start_time, end_time)
        cli.get_obs_count_meta_sinv_base(yaml_file)
    elif inventory_info.nceplibs_cmd == au.NCEPLIBS_CMPBQM:
        yaml_file = yg.generate_nceplibs_cmpbqm_inventory_config(inventory_info, start_time, end_time)
        cli.get_obs_count_meta_cmpbqm_base(yaml_file)
    else:
        print(f'No valid commmand found for nceplibs_cmd in {inventory_info.obs_name} inventory info with value: ' + inventory_info.nceplibs_cmd)

def run_full_inventory(inventory_info):
    print('Beginning inventory for ' + inventory_info.obs_name)
    run_obs_inventory(inventory_info)
    print('Obs inventory complete, now running nceplibs for ' + inventory_info.obs_name)
    run_nceplibs(inventory_info)
    print('NCEPlibs call complete for ' + inventory_info.obs_name)

#for each item in the category list run parallel
#call the run obs inventory and run nceplibs from above
Parallel(n_jobs=10)(delayed(run_full_inventory)(info) for info in to_inventory)

print('Auto inventory script completed for ')
for i in to_inventory: print(i.obs_name)

#NEED TO ADD A CLEAN UP OF THE YAML FILES SOMEWHERE IN HERE 

#next step would be to trigger the plotting scripts again 
