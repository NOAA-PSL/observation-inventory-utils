import obs_inv_utils.obs_inv_cli
import datetime
import yaml
import os
import pathlib

PY_CURRENT_DIR = pathlib.Path(__file__).parent.resolve()


def generate_obs_inv_config(inventory_info, end_time):
    filename = inventory_info.obs_name + '_obs_inv_config.yaml'
    yaml_file_path = os.path.join(PY_CURRENT_DIR, filename)
    body = {
        'cycling_interval': inventory_info.cycling_interval,
        'date_range': {
            'datestr':'%Y%m%dT%H%M%SZ',
            'start':inventory_info.start,
            'end': end_time.strftime('%Y%m%dT%H%M%SZ')
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
    body = {
        's3_bucket': inventory_info.s3_bucket,
        's3_prefix': inventory_info.s3_prefix,
        'date_range': {
            'datestr':'%Y%m%dT%H%M%SZ',
            'start':inventory_info.start,
            'end': end_time.strftime('%Y%m%dT%H%M%SZ')
        },
        'bufr_files':[inventory_info.bufr_files],
        'work_dir': './',
        'scrub_files': 'True'
    }
    with(yaml_file_path, 'w') as outfile:
        yaml.dump(body, outfile)
    return yaml_file_path
