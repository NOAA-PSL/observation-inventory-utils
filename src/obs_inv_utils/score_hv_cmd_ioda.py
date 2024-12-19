from collections import namedtuple

from obs_inv_utils import score_hv_cmds
from obs_inv_utils import inventory_table_factory as itf

IODA_META_NETCDF = 'ioda_meta_netcdf'

ObsMetaIodaData = namedtuple(
    'ObsMetaIodaData',
    [
        'obs_id',
        'cmd_result_id',
        'cmd_str',
        'variable',
        'num_locs',
        'min_depth',
        'max_depth',
        'hasPreQC',
        'hasObsError',
        'sensor',
        'platform',
        'ioda_layout',
        'processing_level',
        'thinning',
        'ioda_version',
        'filename',
        'file_date',
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
        'num_locs',
        'min_depth',
        'max_depth',
        'hasPreQC',
        'hasObsError',
        'sensor',
        'platform',
        'ioda_layout',
        'processing_level',
        'thinning',
        'ioda_version',
        'filename',
        'file_date',
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


#Harvester should return data in the following tuple format:
# HarvestedData = namedtuple(
#     'HarvestedData',
#     [
#         'filename',
#         'obs_day',
#         'file_date_time',
#         'min_date_time',
#         'max_date_time',
#         'num_locs',
#         'min_depth',
#         'max_depth',
#         'num_vars',
#         'variable_name',
#         'var_count',
#         'has_PreQC',
#         'has_ObsError',
#         'sensor',
#         'platform',
#         'ioda_layout',
#         'processing_level',
#         'thinning',
#         'ioda_version',
#     ]
# )
def post_harvest_results(cmd_id, harvest_response, ioda_file):
    #go through response, if multiple variables insert each individually and then insert an agg value
    if not isinstance(harvest_response, list):
        print(f'Error posting harvest results as the response is not of type list but {type(harvest_response)}')
        return #can't parse if not a list of objects
    
    obs_meta_data_items = []
    obs_meta_data_agg_item = [] #if this is only going to be data from one file, there will be at most one agg item (since agg is a full file)
    
    #for item in harvest_response need to make a new insert item
    for item in harvest_response:
        new_item = ObsMetaIodaData(
            ioda_file.obs_id,
            cmd_id, 
            score_hv_cmds.HV_IODA_META,
            item.variable_name, 
            item.var_count,
            item.min_depth,
            item.max_depth,
            item.has_PreQC,
            item.has_ObsError,
            item.sensor,
            item.platform,
            item.ioda_layout,
            item.processing_level,
            item.thinning,
            item.ioda_version,
            item.filename,
            item.file_date_time,
            item.min_date_time,
            item.max_date_time, 
            ioda_file.obs_day
        )

        obs_meta_data_items.append(new_item)

    if len(harvest_response) > 1:
        var_names = ", ".join(item.variable_name for item in harvest_response)
        min_data_date = min(harvest_response, key=lambda item: item.min_date_time)
        max_data_date = max(harvest_response, key=lambda item: item.max_date_time)
        min_depth_response = min(harvest_response, key=lambda item: item.min_depth)
        max_depth_response = max(harvest_response, key=lambda item: item.max_depth)
        new_agg_item = ObsMetaIodaAggData(
            ioda_file.obs_id,
            cmd_id,
            score_hv_cmds.HV_IODA_META,
            var_names,
            harvest_response[0].num_vars,
            harvest_response[0].num_locs,
            min_depth_response.min_depth,
            max_depth_response.max_depth,
            harvest_response[0].has_PreQC,
            harvest_response[0].has_ObsError,
            harvest_response[0].sensor,
            harvest_response[0].platform,
            harvest_response[0].ioda_layout,
            harvest_response[0].processing_level,
            harvest_response[0].thinning,
            harvest_response[0].ioda_version,
            harvest_response[0].filename,
            harvest_response[0].file_date_time,
            min_data_date,
            max_data_date,
            ioda_file.obs_day
        )

        obs_meta_data_agg_item.append(new_agg_item)
    
    print('submitting items for insert')
    #once all items have been translated to work with columns, insert to correct tables 
    itf.insert_obs_meta_hv_ioda_netcdf_item(obs_meta_data_items)
    itf.insert_obs_meta_hv_ioda_netcdf_agg_item(obs_meta_data_agg_item)
