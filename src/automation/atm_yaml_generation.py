import obs_inv_utils.obs_inv_cli
import datetime
import yaml
import os
import pathlib

PY_CURRENT_DIR = pathlib.Path(__file__).parent.resolve()

airs_airsev_dict = {
    'obs_name':'airs_airsev',
    'key':'observations/reanalysis/airs/airsev/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.airsev.tm00.bufr_d',
    'start':'20070201T000000Z',
    'platform':'aws_s3_clean',
    's3_bucket':'noaa-reanalyses-pds',
    's3_prefix':'observations/reanalysis/airs/airsev/%Y/%m/bufr/',
    'bufr_files':'gdas.%z.airsev.tm00.bufr_d',
}

def generate_obs_inv_config(dict, end_time):
    filename = dict['obs_name'] + '_obs_inv_config.yaml'
    yaml_file_path = os.path.join(PY_CURRENT_DIR, filename)
    body = {
        'cycling_interval':'21600',
        'date_range': {
            'datestr':'%Y%m%dT%H%M%SZ',
            'start':dict['start'],
            'end': end_time.strftime('%Y%m%dT%H%M%SZ')
        },
        'search_info':{
            'platform':dict['platform'],
            'key':dict['key']
        }
    }
    with(yaml_file_path, 'w') as outfile:
        yaml.dump(body, outfile)
    return yaml_file_path

