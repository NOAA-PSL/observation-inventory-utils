from collections import namedtuple
from datetime import datetime

from obs_inv_utils import nceplibs_cmds
from obs_inv_utils import inventory_table_factory as itf

CmpbqmMeta = namedtuple(
    'CmpbqmMeta',
    [
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
    ]
)

#data stored in the table per line item, includes type
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

#data stored in aggreagate table for variable aggregate totals 
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


def parse_output(output, prepbufr_file):
    try:
        output_lines = output.split('\n')
        lines_meta = []
        current_variable = ""
        for line in output_lines:
            print(line)
            # skip any lines which are all whitespace
            if line.isspace():
                continue

            cleaned_line = line.strip() # strip to remove whitespace so calls can be to first character of line
            #file is done when line starts with * 
            if '*' in cleaned_line:
                break

            # skip lines which are all ----
            if cleaned_line[0] is '-':
                continue

            #skip lines with 'DATA' in it since this is just a header
            if cleaned_line.find('DATA') != -1:
                continue

            # either on a heading row for the variable or reached the next variable in the list
            # save new variable name for harvested lines below
            if cleaned_line[0].isalpha():
                if cleaned_line[0:3] == 'typ':
                    continue
                else:
                    current_variable = cleaned_line.upper()
                    #fix potential humidity spelling issue coming from cmpbqm output
                    current_variable = current_variable.replace('HUMIDTY', 'HUMIDITY')
                    continue
                

                
            # harvest line of data and save to list
            if line[0].isdigit():
                cleaned_line = cleaned_line.replace('|', ' ')
                #check in case typ and total run into each other to split it properly
                if cleaned_line[3].isdigit():
                        cleaned_line = cleaned_line[0:3] + ' ' + cleaned_line[3:]
                #check in case typ includes R to add space at right place
                if cleaned_line[3].isalpha():
                        cleaned_line = cleaned_line[0:4] + ' ' + cleaned_line[4:]
                split = cleaned_line.split()
                print(f'split line: {split}')
                typ = split[0]
                tot = split[1]
                qm0thru3 = split[2]
                qm4thru7 = split[3]
                qm8 = split[4]
                qm9 = split[5]
                qm10 = split[6]
                qm11 = split[7]
                qm12 = split[8]
                qm13 = split[9]
                qm14 = split[10]
                qm15 = split[11]
                cka = split[12]
                ckb = split[13]
                item = CmpbqmMeta(
                    current_variable,
                    typ,
                    tot,
                    qm0thru3,
                    qm4thru7,
                    qm8,
                    qm9,
                    qm10,
                    qm11,
                    qm12,
                    qm13,
                    qm14,
                    qm15,
                    cka,
                    ckb
                )
                lines_meta.append(item)
    except Exception as e:
        print(f'Error parsing output for prepbufr_file: {prepbufr_file}, error: {e}')
    print("data file output parsed")
    return lines_meta

def post_obs_meta_data(cmd_id, lines_meta, prepbufr_file):
    obs_meta_data_items = []
    obs_meta_data_agg_items = []
    aggregate_dict = {}
    for line_meta in lines_meta:
        #handle aggregate table information
        existing_agg_item = aggregate_dict.get(line_meta.variable)
        if existing_agg_item != None:
            #key exists, combine items 
            new_agg_item = ObsMetaNceplibsPrepbufrAggregateData(
                existing_agg_item.obs_id,
                existing_agg_item.cmd_result_id,
                existing_agg_item.cmd_str,
                existing_agg_item.variable,
                int(existing_agg_item.tot) + int(line_meta.tot),
                int(existing_agg_item.qm0thru3) + int(line_meta.qm0thru3),
                int(existing_agg_item.qm4thru7) + int(line_meta.qm4thru7),
                int(existing_agg_item.qm8) + int(line_meta.qm8),
                int(existing_agg_item.qm9) + int(line_meta.qm9),
                int(existing_agg_item.qm10) + int(line_meta.qm10),
                int(existing_agg_item.qm11) + int(line_meta.qm11),
                int(existing_agg_item.qm12) + int(line_meta.qm12),
                int(existing_agg_item.qm13) + int(line_meta.qm13),
                int(existing_agg_item.qm14) + int(line_meta.qm14),
                int(existing_agg_item.qm15) + int(line_meta.qm15),
                int(existing_agg_item.cka) + int(line_meta.cka),
                int(existing_agg_item.ckb) + int(line_meta.ckb),
                existing_agg_item.filename,
                existing_agg_item.file_size,
                existing_agg_item.obs_day
            )
            aggregate_dict[line_meta.variable] = new_agg_item

        else:
            #key doesn't exist, create agg data item
            obs_agg_item = ObsMetaNceplibsPrepbufrAggregateData(
                prepbufr_file.obs_id, 
                cmd_id,
                nceplibs_cmds.NCEPLIBS_CMPBQM,
                line_meta.variable,
                line_meta.tot,
                line_meta.qm0thru3,
                line_meta.qm4thru7,
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
            aggregate_dict[line_meta.variable] = obs_agg_item

        #create individual item for single entry table
        obs_meta_item = ObsMetaNceplibsPrepbufrData(
            prepbufr_file.obs_id, 
            cmd_id,
            nceplibs_cmds.NCEPLIBS_CMPBQM,
            line_meta.variable,
            line_meta.typ,
            line_meta.tot,
            line_meta.qm0thru3,
            line_meta.qm4thru7,
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
    
    #make an aggregate list to pass to insert
    obs_meta_data_agg_items = list(aggregate_dict.values())

    #insert items into appropriate tables
    itf.insert_obs_meta_nceplibs_prepbufr_item(obs_meta_data_items)
    itf.insert_obs_meta_nceplibs_prepbufr_agg_item(obs_meta_data_agg_items)
    print("data file items inserted to database")