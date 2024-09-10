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

SinvLineData = namedtuple(
    'SinvLineData',
    [
        'sat_id',
        'sat_id_name',
        'obs_count',
        'sat_inst_id',
        'sat_inst_desc',
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
HEADER_LINE = 'header_line'


def validate_args(args):
    return True

# def get_sat_id(line):
#     try:
#         raw_val = line[SAT_ID_START:SAT_ID_END]
#         sat_id = int(raw_val)
#     except Exception as e:
#         print(f'Error parsing sat_id: raw_val: {raw_val}, error: {e}')
#         sat_id = None
#     return sat_id


# def get_sat_id_name(line):
#     try:
#         sat_id_name = line[SAT_ID_NAME_START:SAT_ID_NAME_END]
#         sat_id_name = sat_id_name.strip()
#     except Exception as e:
#         print(f'Error parsing sat_id_name: {sat_id_name}, error: {e}')
#     return sat_id_name


# def get_obs_count(line):
#     try:
#         raw_val = line[OBS_COUNT_START:OBS_COUNT_END]
#         obs_count = int(raw_val)
#     except Exception as e:
#         print(f'Error parsing obs_count: raw_val: {raw_val}, error: {e}')
#         obs_count = None
#     return obs_count


# def get_sat_inst_id(line):
#     try:
#         raw_val = line[SAT_INST_ID_START:SAT_INST_ID_END]
#         sat_inst_id = int(raw_val)
#     except Exception as e:
#         print(f'Error parsing sat_inst_id: raw_val: {raw_val}, error: {e}')
#         sat_inst_id = None
#     return sat_inst_id


# def get_sat_inst_dsc(line):
#     try:
#         sat_inst_dsc = line[SAT_INST_DSC_START:SAT_INST_DSC_END]
#         sat_inst_dsc = sat_inst_dsc.strip()
#     except Exception as e:
#         print(f'Error parsing sat_inst_dsc: {sat_inst_dsc}, error: {e}')
#         sat_inst_dsc = None
#     return sat_inst_dsc


def get_line_type(line):
    if len(line) <=1:
        return FILLER_LINE
    try:
        header_keywords = ["id", "satellite", "subsets", "instrument"]
        if all(keyword.lower() in line.lower() for keyword in header_keywords):
            return HEADER_LINE
        if line.strip() == "":
            return FILLER_LINE
        
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
            line_data = parse_data_line(line)
            if line_data.obs_count is not None:
                obs_cnt_sum += line_data.obs_count
            try:
                line_meta = SinvMeta(
                    bufr_file.obs_id,
                    line_data.sat_id,
                    line_data.sat_id_name,
                    line_data.obs_count,
                    line_data.sat_inst_id,
                    line_data.sat_inst_desc,
                    bufr_file.obs_day,
                    bufr_file.filename,
                    bufr_file.file_size
                )
                lines_meta.append(line_meta)
            except Exception as e:
                print(f'Problem with sinv output parsing - error: {e}')
        elif line_type == OBS_COUNT_TOTAL_LINE:
            check_obs_cnt_sum = parse_total_obs_line(line)
            if check_obs_cnt_sum is not None and obs_cnt_sum != check_obs_cnt_sum:
                print(f'Output obs count sum: {check_obs_cnt_sum} ' \
                       f'does not match lines sum: {obs_cnt_sum}')

    return lines_meta

def parse_data_line(line):
    split_line = line.split(maxsplit=4) #know there's 5 columns

    #define variables to be assigned
    sat_id = None
    sat_id_name = None
    obs_count = None
    sat_inst_id = None
    sat_inst_desc = None

    try:
        raw_sat_id = split_line[0].strip()
        sat_id = int(raw_sat_id)
    except Exception as e:
        print(f'Error parsing sat_id: raw_val: {raw_sat_id}, error: {e}')
    
    try:
        sat_id_name = split_line[1].strip()
    except Exception as e:
        print(f'Error parsing sat_id_name: {sat_id_name}, error: {e}')
    
    try:
        raw_count_val = split_line[2].strip()
        obs_count = int(raw_count_val)
    except Exception as e:
        print(f'Error parsing obs_count: raw_val: {raw_count_val}, error: {e}')

    try:
        raw_inst_id_val = split_line[3].strip()
        sat_inst_id = int(raw_inst_id_val)
    except Exception as e:
        print(f'Error parsing sat_inst_id: raw_val: {raw_inst_id_val}, error: {e}')

    try:
        sat_inst_desc = split_line[4].strip()
    except Exception as e:
        print(f'Error parsing sat_inst_dsc: {sat_inst_desc}, error: {e}')

    return SinvLineData(
        sat_id,
        sat_id_name,
        obs_count,
        sat_inst_id,
        sat_inst_desc
    )

def parse_total_obs_line(line):
    total_obs_count = None
    try:
        clean_line = line.strip()
        total_obs_count = int(clean_line)
    except Exception as e:
        print(f'Error parsing total_obs_count from line: {clean_line}, error: {e}')
    return total_obs_count
    

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
