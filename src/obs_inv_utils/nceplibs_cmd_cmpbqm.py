from collections import namedtuple
from datetime import datetime
import re

from obs_inv_utils import nceplibs_cmds
from obs_inv_utils import inventory_table_factory as itf
 
ObsMetaNceplibsPrepbufrData = namedtuple(
    'ObsMetaNceplibsPrepbufrData',
    [
        'obs_id',
        'cmd_result_id',
        'cmd_str',
        'variable',
        'typ',
        'tot',
        'qm0thru3',
        'qm4thru7',
        'qm8',
        'qm9',
        'qm10',
        'qm11',
        'qm12',
        'qm13',
        'qm14',
        'qm15',
        'cka',
        'ckb',
        'filename',
        'file_size',
        'obs_day',
    ]
)

ObsMetaNceplibsPrepbufrAggregateData = namedtuple(
    'ObsMetaNceplibsPrepbufrAggregateData',
    [
        'obs_id',
        'cmd_result_id',
        'cmd_str',
        'variable',
        'tot',
        'qm0thru3',
        'qm4thru7',
        'qm8',
        'qm9',
        'qm10',
        'qm11',
        'qm12',
        'qm13',
        'qm14',
        'qm15',
        'cka',
        'ckb',
        'filename',
        'file_size',
        'obs_day',
    ]
)

def validate_args(args):
    return True


def parse_output():
    #call score hv
    return "to be added"

def post_obs_meta_data(cmd_id, lines_meta, prepbufr_file):
    #prep obs meta for insert to table

    #this will be based on the new name for these items
    #iterate over lines meta for each object to save
    # this will probably handle the variations of table inputs we want to calculate
    # calculate the aggregates --- probably using list(filter(lambda)) or all(x with name) like Linq
    #since we have to loop anyway is it better to just map as looping?? 
    # call itf.insert_... make a new call for inserting to our new table

    obs_meta_data_items = []
    obs_meta_data_agg_items = []
    for line_meta in lines_meta:
        obs_meta_item = ObsMetaNceplibsPrepbufrData(
            prepbufr_file.obs_id, 
            cmd_id,
            nceplibs_cmds.NCEPLIBS_CMPBQM,
            line_meta.variable,
            line_meta.typ,
            line_meta.tot,
            line_meta.qm0thru3,
            line_meta.qm4thu7,
            line_meta.qm8,
            line_meta.qm9,
            line_meta.qm10,
            line_meta.qm11,
            line_meta.qm12,
            line_meta.qm13,
            line_meta.qm14,
            line_meta.qm15,
            line_meta.cka,
            line_meta.ckb,
            prepbufr_file.filename,
            prepbufr_file.file_size,
            prepbufr_file.obs_day
        )

        obs_meta_data_items.append(obs_meta_item)
    
    #CALCULATE THE AGG SomEWHERE before this 
    itf.insert_obs_meta_nceplibs_prepbufr_item(obs_meta_data_items)
    itf.insert_obs_meta_nceplibs_prepbufr_agg_item(obs_meta_data_agg_items)