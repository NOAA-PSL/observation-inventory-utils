from collections import namedtuple

from obs_inv_utils import score_hv_cmds
from obs_inv_utils import inventory_table_factory as itf

WOD_INSITU_META_NETCDF = 'wod_insitu_meta_netcdf'

ObsMetaWodData = namedtuple(
    'ObsMetaWodData',
    [
        'obs_id',
        'cmd_result_id',
        'cmd_str',
        'variable',
        'var_count',
        'min_depth',
        'max_depth',
        'sensor',
        'casts',
        'filename',
        'min_data_date',
        'max_data_date',
        'obs_day',
    ]
)

ObsMetaWodAggData = namedtuple(
    'ObsMetaWodAggData',
    [
        'obs_id',
        'cmd_result_id',
        'cmd_str',
        'variable_names',
        'num_vars',
        'var_counts',
        'min_depth',
        'max_depth',
        'sensor',
        'casts',
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

def post_harvest_results(cmd_id, harvest_response, wod_file):
    #go through response, if multiple variables insert each individually and then insert an agg value
    if not isinstance(harvest_response, list):
        print(f'Error posting harvest results as the response is not of type list but {type(harvest_response)}')
        return #can't parse if not a list of objects
    
    obs_meta_data_items = []
    obs_meta_data_agg_item = [] #if this is only going to be data from one file, there will be at most one agg item (since agg is a full file)
    
    #go through items in harvest response and build data insert 
    for item in harvest_response:
        new_item = ObsMetaWodData(
            wod_file.obs_id, 
            cmd_id,
            score_hv_cmds.HV_WOD_NC_META,
            item.variable_name,
            convert_to_int(item.var_count), 
            convert_to_float(item.min_depth),
            convert_to_float(item.max_depth), 
            item.sensor,
            convert_to_int(item.casts),
            item.filename,
            item.min_date_time,
            item.max_date_time,
            wod_file.obs_day
        )

        obs_meta_data_items.append(new_item)

    #handle aggregation 
    if len(harvest_response) > 1:
        var_names = ", ".join(item.variable_name for item in harvest_response)
        total_var_count = sum(item.var_count for item in harvest_response)
        new_agg_item = ObsMetaWodAggData(
            wod_file.obs_id,
            cmd_id, 
            score_hv_cmds.HV_WOD_NC_META,
            var_names, 
            convert_to_int(harvest_response[0].num_vars),
            convert_to_int(total_var_count),
            convert_to_float(harvest_response[0].min_depth),
            convert_to_float(harvest_response[0].max_depth),
            harvest_response[0].sensor,
            convert_to_int(harvest_response[0].casts),
            harvest_response[0].filename,
            harvest_response[0].min_date_time,
            harvest_response[0].max_date_time,
            wod_file.obs_day
        )

        obs_meta_data_agg_item.append(new_agg_item)
    
    #once all items have been translated to work with columns, insert to correct tables 
    itf.insert_obs_meta_hv_wod_netcdf_item(obs_meta_data_items)
    itf.insert_obs_meta_hv_wod_netcdf_agg_item(obs_meta_data_agg_item)

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