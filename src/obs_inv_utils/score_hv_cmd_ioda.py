from collections import namedtuple
from datetime import datetime
import re

from obs_inv_utils import score_hv_cmds
from obs_inv_utils import inventory_table_factory as itf


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

def build_harvest_dict():
    dict =  {}
    return dict


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
    if harvest_response is not list:
        return #can't parse if not a list of objects
    
    obs_meta_data_items = []
    obs_meta_data_agg_item = [] #if this is only going to be data from one file, there will be at most one agg item (since agg is a full file)
    aggregate_dict = {}
    
    #for item in harvest_response need to make a new insert item
