from collections import namedtuple
from datetime import datetime
import re

from obs_inv_utils import nceplibs_cmds
from obs_inv_utils import inventory_table_factory as itf

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
    