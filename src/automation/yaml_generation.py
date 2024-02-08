'''
Generation of yaml configurations needed to pass to the CLI
'''
import yaml
import os
import pathlib
from datetime import datetime as dt
import automation_utils as au

PY_CURRENT_DIR = pathlib.Path(__file__).parent.resolve()

# produces the yaml in required format to pass to get_obs_inventory cli command
def generate_obs_inv_config(inventory_info, start_time, end_time):
    filename = inventory_info.obs_name + '_obs_inv_config.yaml'
    yaml_file_path = os.path.join(PY_CURRENT_DIR, filename)
    if start_time is dt:
        start = start_time.strftime(au.DATESTR_FORMAT)
    else:
        start = start_time
    if end_time is dt:
        end = end_time.strftime(au.DATESTR_FORMAT)
    else:
        end = end_time
    body = {
        'cycling_interval': inventory_info.cycling_interval,
        'date_range': {
            'datestr':au.DATESTR_FORMAT,
            'start': start,
            'end': end
        },
        'search_info':[{
            'platform':inventory_info.platform,
            'key':inventory_info.key 
            }
        ],
    }
    outfile = open(yaml_file_path, 'w')
    yaml.dump(body, outfile)
    outfile.close()
    return yaml_file_path

# produces the yaml in required format to pass to get_obs_count_meta_sinv cli command
def generate_nceplibs_sinv_inventory_config(inventory_info, start_time, end_time, work_dir):
    filename = inventory_info.obs_name + '_obs_meta_sinv.yaml'
    yaml_file_path = os.path.join(PY_CURRENT_DIR, filename)
    if start_time is dt:
        start = start_time.strftime(au.DATESTR_FORMAT)
    else:
        start = start_time
    if end_time is dt:
        end = end_time.strftime(au.DATESTR_FORMAT)
    else:
        end = end_time
    body = {
        's3_bucket': inventory_info.s3_bucket,
        's3_prefix': inventory_info.s3_prefix,
        'date_range': {
            'datestr':au.DATESTR_FORMAT,
            'start': start,
            'end': end
        },
        'bufr_files':[inventory_info.bufr_files],
        'work_dir': work_dir,
        'scrub_files': True
    }
    outfile = open(yaml_file_path, 'w')
    yaml.dump(body, outfile)
    outfile.close()
    return yaml_file_path

# produces the yaml in required format to pass to get_obs_count_meta_cmpbqm cli command
def generate_nceplibs_cmpbqm_inventory_config(inventory_info, start_time, end_time, work_dir):
    filename = inventory_info.obs_name + '_obs_meta_cmpbqm.yaml'
    yaml_file_path = os.path.join(PY_CURRENT_DIR, filename)
    if start_time is dt:
        start = start_time.strftime(au.DATESTR_FORMAT)
    else:
        start = start_time
    if end_time is dt:
        end = end_time.strftime(au.DATESTR_FORMAT)
    else:
        end = end_time
    body = {
        's3_bucket': inventory_info.s3_bucket,
        's3_prefix': inventory_info.s3_prefix,
        'date_range': {
            'datestr':au.DATESTR_FORMAT,
            'start': start,
            'end': end
        },
        'prepbufr_files':[inventory_info.bufr_files],
        'work_dir': work_dir,
        'scrub_files': True
    }
    outfile = open(yaml_file_path, 'w')
    yaml.dump(body, outfile)
    outfile.close()
    return yaml_file_path
