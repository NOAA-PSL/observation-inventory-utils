from collections import namedtuple
from datetime import datetime
import re

from obs_inv_utils import nceplibs_cmds
from obs_inv_utils import inventory_table_factory as itf

SinvMeta = namedtuple(
    'SinvMeta',
    [
        'obs_inv_id',
        'sat_id',
        'sat_id_name',
        'obs_count',
        'sat_inst_id',
        'sat_inst_desc',
        'obs_day',
        'source_filename',
        'source_file_size'
    ]
)

ObsMetaNceplibsBufrData = namedtuple(
    'ObsMetaNceplibsBufrData',
    [
        'obs_id',
        'cmd_result_id',
        'cmd_str',
        'sat_id',
        'sat_id_name',
        'obs_count',
        'sat_inst_id',
        'sat_inst_desc',
        'filename',
        'file_size',
        'obs_day',
    ]
)

SPACE_SEPARATOR_LEN = 2
SAT_ID_START = 0
SAT_ID_END = SAT_ID_START + 3
SAT_ID_NAME_START = SAT_ID_END + SPACE_SEPARATOR_LEN
SAT_ID_NAME_END = SAT_ID_NAME_START + 16
OBS_COUNT_START = SAT_ID_NAME_END + SPACE_SEPARATOR_LEN
OBS_COUNT_END = OBS_COUNT_START + 10
SAT_INST_ID_START = OBS_COUNT_END + SPACE_SEPARATOR_LEN
SAT_INST_ID_END = SAT_INST_ID_START + 3
SAT_INST_DSC_START = SAT_INST_ID_END + SPACE_SEPARATOR_LEN
SAT_INST_DSC_END = SAT_INST_DSC_START + 80

OBS_DATA_LINE = 'obs_data_line'
OBS_COUNT_TOTAL_LINE = 'obs_count_total_line'
FILLER_LINE = 'filler_line'



def validate_args(args):
    return True

def get_sat_id(line):
    try:
        raw_val = line[SAT_ID_START:SAT_ID_END]
        sat_id = int(raw_val)
    except Exception as e:
        print(f'Error parsing sat_id: raw_val: {raw_val}, error: {e}')
        sat_id = None
    return sat_id


def get_sat_id_name(line):
    try:
        sat_id_name = line[SAT_ID_NAME_START:SAT_ID_NAME_END]
        sat_id_name = sat_id_name.strip()
    except Exception as e:
        print(f'Error parsing sat_id_name: {sat_id_name}, error: {e}')
    return sat_id_name


def get_obs_count(line):
    try:
        raw_val = line[OBS_COUNT_START:OBS_COUNT_END]
        obs_count = int(raw_val)
    except Exception as e:
        print(f'Error parsing obs_count: raw_val: {raw_val}, error: {e}')
        obs_count = None
    return obs_count


def get_sat_inst_id(line):
    try:
        raw_val = line[SAT_INST_ID_START:SAT_INST_ID_END]
        sat_inst_id = int(raw_val)
    except Exception as e:
        print(f'Error parsing sat_inst_id: raw_val: {raw_val}, error: {e}')
        sat_inst_id = None
    return sat_inst_id


def get_sat_inst_dsc(line):
    try:
        sat_inst_dsc = line[SAT_INST_DSC_START:SAT_INST_DSC_END]
        sat_inst_dsc = sat_inst_dsc.strip()
    except Exception as e:
        print(f'Error parsing sat_inst_dsc: {sat_inst_dsc}, error: {e}')
        sat_inst_dsc = None
    return sat_inst_dsc


def get_line_type(line):
    if len(line) <=1:
        return FILLER_LINE
    try:
        obs_count = get_obs_count(line)
        if obs_count is not None:
            if line[0] != ' ':
                return OBS_DATA_LINE
            else:
                return OBS_COUNT_TOTAL_LINE
    except Exception as e:
        print(f'could not parse obs_total, must be filler line')

    return FILLER_LINE

def parse_output(output, bufr_file):
    print(f"output: {output}")
    # split the output into an array of lines
    output_lines = output.split('\n')
    print(f'output_lines: {output_lines}')
    lines_meta = []
    obs_cnt_sum = 0
    for line in output_lines:
        line_type = get_line_type(line)
        if line_type == OBS_DATA_LINE:
            sat_id = get_sat_id(line)
            sat_id_name = get_sat_id_name(line)
            obs_count = get_obs_count(line)
            obs_cnt_sum += obs_count
            sat_inst_id = get_sat_inst_id(line)
            sat_inst_dsc = get_sat_inst_dsc(line)
            try:
                line_meta = SinvMeta(
                    bufr_file.obs_id,
                    sat_id,
                    sat_id_name,
                    obs_count,
                    sat_inst_id,
                    sat_inst_dsc,
                    bufr_file.obs_day,
                    bufr_file.filename,
                    bufr_file.file_size
                )
                lines_meta.append(line_meta)
            except Exception as e:
                print(f'Problem with sinv output parsing - error: {e}')
        elif line_type == OBS_COUNT_TOTAL_LINE:
            check_obs_cnt_sum = get_obs_count(line)
            if obs_cnt_sum != check_obs_cnt_sum:
                print(f'Output obs count sum: {check_obs_cnt_sum} ' \
                       f'does not match lines sum: {obs_cnt_sum}')

    return lines_meta

def post_obs_meta_data(cmd_id, lines_meta, bufr_file):
    # package obs meta for file insert
    obs_meta_data_items = []
    for line_meta in lines_meta:
        obs_meta_item = ObsMetaNceplibsBufrData(
            bufr_file.obs_id,
            cmd_id,
            nceplibs_cmds.NCEPLIBS_SINV,
            line_meta.sat_id,
            line_meta.sat_id_name,
            line_meta.obs_count,
            line_meta.sat_inst_id,
            line_meta.sat_inst_desc,
            bufr_file.filename,
            bufr_file.file_size,
            bufr_file.obs_day
        )

        obs_meta_data_items.append(obs_meta_item)

    itf.insert_obs_meta_nceplibs_bufr_item(obs_meta_data_items) 
