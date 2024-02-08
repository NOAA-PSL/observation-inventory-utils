'''
Script for automated running of inventory in the AWS S3 bucket
Allows for configuration of categories of data to run (currently referencing atm_dicts), an end date, and number of days ago
If nothing is specified in the configuration, it runs the full period of time for all atmosphere variables. 
Runs in parallel on given number of CPUs. 
'''
import automation_utils as au
import atm_dicts
import yaml_generation as yg

import argparse
from joblib import Parallel, delayed
import os

from datetime import datetime as dt
from datetime import timedelta
from pandas import Timestamp

#argparse section
parser = argparse.ArgumentParser()
parser.add_argument("-cat", dest="category", help="Category of variables to inventory. Valid options: atmosphere", choices=['atmosphere', 'list'], default="atmosphere", type=str)
parser.add_argument("-end", dest="end_date", help=f"End date to use for run. Format expected {au.ESCAPED_DATESTR_FORMAT}. If not provided, uses the current time.", type=str)
parser.add_argument("-ago", dest="days_ago", help="Number of days before today or a given end_date (defined by the -end argument) over which to run the inventory. If provided, must be positive integer. If not provided, it will run the full extent of the inventory.", default=0, type=int)
parser.add_argument("-n_jobs", dest="n_jobs", help="Number of parallel jobs to run.", default=18, type=int)
parser.add_argument("--list", dest="var_list", help="List of the variables to inventory with spaces between each, will only be used if -cat is list", type=str, nargs='+')
args = parser.parse_args()

#check that input variables are valid 
if args.end_date != None and len(args.end_date) > 0:
    try:
        end_date = dt.strptime(args.end_date, au.DATESTR_FORMAT)
    except ValueError:
        print(f'Argument -end value {args.end_date} is not a string in the valid format of {au.DATESTR_FORMAT}. Please give a valid end date.')
        quit()
else:
    end_date = None

if args.days_ago < 0:
    print(f'Argument -ago value {args.days_ago} is not a positive value, please give a valid positive integer to use the -ago argument.')
    quit()

#get category list
# more categories to be added as they are written as dictionaries 
# remember to add new categories to the argparser options and here
to_inventory = []
if args.category == 'atmosphere':
    to_inventory = atm_dicts.atm_infos
if args.category == 'list':
    try:
        to_inventory = [x for x in atm_dicts.atm_infos if any(x.obs_name == i for i in args.var_list)]
    except Exception as ex:
        print("An error occurred getting list values to inventory")
        print(ex)
        quit()
    if to_inventory is None:
        print("The provided list did not match available variables.")
        quit()
    if to_inventory.count() != args.var_list.count():
        print("Some of the items in the list were not available variables.")
        print("The following items were valid: ")
        for i in to_inventory: print(i.obs_name)
        quit()


#Import CLI here so that we only connect to the database if the arguments were valid 
import obs_inv_utils.obs_inv_cli as cli

#function to determine the start and end time for inventory calls based on given info  
def get_start_end_time(inventory_info):
    #additional cycling options will need to be added as functionality expands 
    if inventory_info.cycling_interval == au.CYCLING_6H:
        frequency = '6H'
    else: #default to round to closest hour
        frequency = 'H'

    if end_date != None:
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
#call get obs inventory cli 
def run_obs_inventory(inventory_info):
    start_time, end_time = get_start_end_time(inventory_info)

    yaml_file = yg.generate_obs_inv_config(inventory_info, start_time, end_time)
    cli.get_obs_inventory_base(yaml_file)
    os.remove(yaml_file)

#call appropriate nceplibs cli command 
def run_nceplibs(inventory_info):
    start_time, end_time = get_start_end_time(inventory_info)
    
    #run correct command as given in dict 
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

#function to use for parallel call for each variable 
def run_full_inventory(inventory_info):
    print('Beginning inventory for ' + inventory_info.obs_name)
    run_obs_inventory(inventory_info)
    print('Obs inventory complete, now running nceplibs for ' + inventory_info.obs_name)
    run_nceplibs(inventory_info)
    print('NCEPlibs call complete for ' + inventory_info.obs_name)

#for each item in the category list run parallel
#call the run obs inventory and run nceplibs from above
Parallel(n_jobs=args.n_jobs)(delayed(run_full_inventory)(info) for info in to_inventory)

print('Auto inventory script completed for ')
for i in to_inventory: print(i.obs_name)
