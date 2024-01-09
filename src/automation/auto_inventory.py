import automation_utils as au
import atm_dicts
import yaml_generation as yg
import obs_inv_utils.obs_inv_cli as cli

import argparse
from joblib import Parallel, delayed
import os

from datetime import datetime as dt
from datetime import timedelta
from pandas import Timestamp

#argparse section
parser = argparse.ArgumentParser()
parser.add_argument("-cat", dest="category", help="Category of variables to inventory. Valid options: atmosphere", choices=['atmosphere'], default="atmosphere", type=str)
parser.add_argument("-end", dest="end_date", help="End date to use for run. Format expected %Y%m%dT%H%M%SZ. If not provided, uses the current time.", type=str)
parser.add_argument("-ago", dest="days_ago", help="Number of days ago to run the inventory for. If provided, must be positive integer. If not provided, it will run the full extent of the inventory.", default=0, type=int)
args = parser.parse_args()

#get category list
# more categories to be added as they are written as dictionaries 
# remember to add new categories to the argparser options and here
to_inventory = []
if args.category == 'atmosphere':
    to_inventory = atm_dicts.atm_infos 

#set end date time and put in 6H time 
# if len(args.end_date) > 0:
#     end_date = dt.strptime(args.end_date, au.DATESTR_FORMAT)
#     end = Timestamp(end_date).round(freq='6H')
# else:
#     end = Timestamp.now().round(freq='6H')
    
def get_start_end_time(inventory_info):
    if inventory_info.cycling_interval == au.CYCLING_6H:
        frequency = '6H'
    else: #default to round to closest hour as I think that's the lowest current unit 
        frequency = 'H'

    if args.end_date != None and len(args.end_date) > 0:
        end_date = dt.strptime(args.end_date, au.DATESTR_FORMAT)
        end = Timestamp(end_date).round(freq=frequency)
    else:
        end = Timestamp.now().round(freq=frequency)

    if args.days_ago > 0:
        end_time = end.strftime(au.DATESTR_FORMAT)
        start = end - timedelta(days=args.days_ago)
        start_time = start.strftime(au.DATESTR_FORMAT)
    else: #run the full period from start to now if no days ago
        start_time = inventory_info.start
        end_time = end.strftime(au.DATESTR_FORMAT)

    return start_time, end_time

#define functions to run in parallel 
def run_obs_inventory(inventory_info):
    #EXPAND THIS LATER TO HANDLE TWO DAY RUNS; probably specify end time as part fo the argument options above
    # if args.days_ago > 0:
    #     #end = Timestamp.now().round(freq='6H')
    #     #end = dt.now() # need to get in 0/6/12/18z most recent value 
    #     end_time = end.strftime(au.DATESTR_FORMAT)
    #     start = end - timedelta(days=args.days_ago)
    #     start_time = start.strftime(au.DATESTR_FORMAT)
    #     print(f'Start time: {start_time}, End time: {end_time}')
    # else: #run the full period from start to now
    #     start_time = inventory_info.start
    #     #end = dt.now() # need to get this in the 0 / 6 / 12 / 18z most recent value 
    #     #end = Timestamp.now().round(freq='6H')
    #     end_time = end.strftime(au.DATESTR_FORMAT)
    start_time, end_time = get_start_end_time(inventory_info)

    yaml_file = yg.generate_obs_inv_config(inventory_info, start_time, end_time)
    cli.get_obs_inventory_base(yaml_file)
    os.remove(yaml_file)

def run_nceplibs(inventory_info):
    # if args.days_ago > 0:
    #     #end = Timestamp.now().round(freq='6H')
    #     #end = dt.now() # need to get in 0/6/12/18z most recent value 
    #     end_time = end.strftime(au.DATESTR_FORMAT)
    #     start = end - timedelta(days=args.days_ago)
    #     start_time = start.strftime(au.DATESTR_FORMAT)
    #     print(f'Start time: {start_time}, End time: {end_time}')
    # else: #run the full period from start to now
    #     start_time = inventory_info.start
    #     #end = dt.now() # need to get this in the 0 / 6 / 12 / 18z most recent value 
    #     #end = Timestamp.now().round(freq='6H')
    #     end_time = end.strftime(au.DATESTR_FORMAT)

    start_time, end_time = get_start_end_time(inventory_info)
    
    #run correct command
    if inventory_info.nceplibs_cmd == au.NCEPLIBS_SINV:
        yaml_file = yg.generate_nceplibs_sinv_inventory_config(inventory_info, start_time, end_time)
        cli.get_obs_count_meta_sinv_base(yaml_file)
        os.remove(yaml_file)
    elif inventory_info.nceplibs_cmd == au.NCEPLIBS_CMPBQM:
        yaml_file = yg.generate_nceplibs_cmpbqm_inventory_config(inventory_info, start_time, end_time)
        cli.get_obs_count_meta_cmpbqm_base(yaml_file)
        os.remove(yaml_file)
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

#next step would be to trigger the plotting scripts again 
