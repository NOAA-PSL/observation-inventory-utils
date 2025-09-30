from collections import namedtuple

from obs_inv_utils import score_hv_cmds
from obs_inv_utils import inventory_table_factory as itf

OZONE_META_NETCDF = 'ozone_meta_netcdf'

ObsMetaOzoneData = namedtuple(
    'ObsMetaOzoneData',
    [
        'obs_id',
        'cmd_result_id',
        'cmd_str',
        'variable', #will always be ozone, but want for consistency with other tables
        'ozone_count',
        'levels',
        'profiles',
        'min_pressure',
        'max_pressure',
        'sensor',
        'filename',
        'min_data_date',
        'max_data_date',
        'obs_day',
    ]
)

def build_harvest_dict(command, args):
    filename = args.get('filename', None)
    if filename is None: 
        raise ValueError('required args "filename" not found. cannot build harvest dict')
    hv_dict =  {
        'harvester_name': command,
        'filename': filename
    }
    return hv_dict

def post_harvest_results(cmd_id, harvest_response, ozone_file):
    #go through response, if multiple variables insert each individually and then insert an agg value
    if not isinstance(harvest_response, list):
        print(f'Error posting harvest results as the response is not of type list but {type(harvest_response)}')
        return #can't parse if not a list of objects
    
    obs_meta_data_items = []
    
    #go through items in harvest response and build data insert 
    for item in harvest_response:
        new_item = ObsMetaOzoneData(
            ozone_file.obs_id, 
            cmd_id,
            score_hv_cmds.HV_OZONE_NC_META,
            'ozone',
            convert_to_int(item.ozone_count),
            convert_to_int(item.levels),
            convert_to_int(item.profiles), 
            convert_to_float(item.min_pressure),
            convert_to_float(item.max_pressure),
            item.sensor,
            item.filename,
            item.min_date_time,
            item.max_date_time,
            ozone_file.obs_day
        )

        obs_meta_data_items.append(new_item)

    #once all items have been translated to work with columns, insert to correct tables 
    itf.insert_obs_meta_hv_ozone_netcdf_item(obs_meta_data_items)

def convert_to_int(value):
    """Safely convert a value to an int."""
    if value is None:
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def convert_to_float(value):
    """Safely convert a value to a float."""
    if value is None:
        return None
    try:
        return float(value)
    except (ValueError, TypeError):
        return None