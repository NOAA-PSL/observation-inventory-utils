from collections import namedtuple

from obs_inv_utils import score_hv_cmds
from obs_inv_utils import inventory_table_factory as itf

WOD_INSITU_META_NETCDF = 'wod_insitu_meta_netcdf'

ObsMetaWODData = namedtuple(
    'ObsMetaWODData',
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

ObsMetaIodaAggData = namedtuple(
    'ObsMetaIodaAggData',
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
    #handle aggregation


    #insert to itf - single items, agg items 


    