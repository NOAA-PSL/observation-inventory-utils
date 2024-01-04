import yaml
import os
import pathlib
from datetime import datetime as dt
import automation_utils as au

PY_CURRENT_DIR = pathlib.Path(__file__).parent.resolve()

def generate_obs_inv_config(inventory_info, end_time):
    filename = inventory_info.obs_name + '_obs_inv_config.yaml'
    yaml_file_path = os.path.join(PY_CURRENT_DIR, filename)
    if end_time is dt:
        end = end_time.strftime(au.DATESTR_FORMAT)
    else:
        end = end_time
    body = {
        'cycling_interval': inventory_info.cycling_interval,
        'date_range': {
            'datestr':au.DATESTR_FORMAT,
            'start':inventory_info.start,
            'end': end
        },
        'search_info':{
            'platform':inventory_info.platform,
            'key':inventory_info.key
        }
    }
    with(yaml_file_path, 'w') as outfile:
        yaml.dump(body, outfile)
    return yaml_file_path

def generate_nceplibs_inventory_config(inventory_info, end_time):
    filename = inventory_info.obs_name + '_obs_meta_nceplibs.yaml'
    yaml_file_path = os.path.join(PY_CURRENT_DIR, filename)
    if end_time is dt:
        end = end_time.strftime(au.DATESTR_FORMAT)
    else:
        end = end_time
    body = {
        's3_bucket': inventory_info.s3_bucket,
        's3_prefix': inventory_info.s3_prefix,
        'date_range': {
            'datestr':au.DATESTR_FORMAT,
            'start':inventory_info.start,
            'end': end
        },
        'bufr_files':[inventory_info.bufr_files],
        'work_dir': './',
        'scrub_files': 'True'
    }
    with(yaml_file_path, 'w') as outfile:
        yaml.dump(body, outfile)
    return yaml_file_path
