from typing import Optional
from dataclasses import dataclass, field
from datetime import datetime
import json
import os
from pathlib import Path
import shutil
import uuid

import pandas as pd
from pandas import DataFrame
import pathlib
import numpy as np

from config_handlers.obs_meta_sinv import ObsMetaSinvConfig
from config_handlers.obs_meta_cmpbqm import ObsMetaCMPBQMConfig
from obs_inv_utils import obs_inv_queries as oiq
from obs_inv_utils import aws_s3_interface as s3
from obs_inv_utils import time_utils
from obs_inv_utils.time_utils import DateRange
from obs_inv_utils import inventory_table_factory as itf
from obs_inv_utils import subprocess_cmd_handler as sch
from obs_inv_utils.subprocess_cmd_handler import SubprocessCmd
from obs_inv_utils import nceplibs_cmds as nc_cmds

import yaml

CALLING_DIR = pathlib.Path(__file__).parent.resolve()
TMP_OBS_DATA_DIR = 'tmp_obs_data'

def post_aws_s3_cmd_result(raw_response, obs_cycle_time):
    if not isinstance(raw_response, s3.AwsS3CommandRawResponse):
        msg = 'raw_response must be of type AwsS3CommandRawResponse. It is'\
              f' actually of type: {type(raw_response)}'
        raise TypeError(msg)

    output_str = json.dumps(
        raw_response.output,
        default=time_utils.default_datetime_converter
    )

    cmd_result_data = itf.CmdResultData(
        raw_response.command,
        raw_response.args_0,
        output_str,
        '',
        raw_response.return_code,
        obs_cycle_time,
        raw_response.submitted_at,
        raw_response.latency,
        datetime.utcnow()
    )

    itf.insert_cmd_result(cmd_result_data)


def download_bufr_file_from_s3(work_dir, bufr_file):
    object_key = bufr_file['full_path']

    obs_day = datetime.strftime(bufr_file['obs_day'], '%Y%m%d')

    dest_path = os.path.join(
        work_dir, obs_day, bufr_file['filename'])

    try:
        Path(dest_path).mkdir(parents=True, exist_ok=True)
    except Exception as err:
        msg = f'\'work_dir\' is not a directory - err: {err}'
        raise ValueError(msg) from err

    dest_filename = os.path.join(dest_path, bufr_file['filename'])
    
    print(f'dest_filename: {dest_filename}')

    # setup command arguments, [file s3 key, destination location,
    # and expected filesize
    args = [object_key, dest_filename, bufr_file['file_size']]

    cmd = s3.AwsS3CommandHandler(s3.CMD_DOWNLOAD_S3_OBJ, args)
    print(f'cmd: {cmd}')

    saved_filename = None
    if cmd.send():
        saved_filename = dest_filename

    # post result from command success or failure
    raw_resp = cmd.get_raw_response()
    print(f'raw_resp')

    print('posting command results for aws s3')
    post_aws_s3_cmd_result(
        raw_resp,
        bufr_file['obs_day']
    )

    return saved_filename



@dataclass
class ObsBufrFileMetaHandler(object):
    meta_config: ObsMetaSinvConfig
    bufr_files: list = field(default_factory=list, init=False)
    date_range: DateRange = field(init=False)
    #config_yaml: str
    config_data: dict = field(default_factory=str, init=False)
    s3_bucket: str = field(default_factory=str, init=False)
    s3_prefix: str = field(default_factory=str, init=False)


    def __post_init__(self):
        self.date_range = self.meta_config.get_date_range()
        self.bufr_files = self.meta_config.get_bufr_file_list()
        self.config_data = self.meta_config.load()

        #self.yaml.safe_load()
        print(f' -----0------- self: {self} ---')
        print(f' ')
        print(f' ')
        print(f' -----1------- self.config_data: {self.config_data} ---')
        print(f' ') 
        print(f' ')
        print(f' -----2------- self.config_data: {self.config_data} ---')
        #print(f' -----1------- meta_configconfig_data: {meta_config.config_data} -------------------------------------')
        #print(f' ------------ self.meta_config.s3_bucket: {self.s3_bucket} ------------------')
        #print(f' ------------ self.s3_bucket: {self.s3_bucket} ------------------')
        #print(f'self.meta_config.platform: {self.platform}')


    def __repr__(self):
        """
        string representation of ObsBufrFileMetaHandler globals
        """
        return f'meta_config: {self.meta_config}, ' \
            f'bufr_files: {self.bufr_files}, ' \
            f'date_range: {self.date_range}'

    def get_bufr_file_meta(self, cmd_type):

        inventory_bufr_files = oiq.get_bufr_files_data(
            self.bufr_files,
            self.date_range.start,
            self.date_range.end
        )
        
        #temp_uuid = str(uuid.uuid4())

        #work_dir = os.path.join(self.meta_config.work_dir, temp_uuid)
        bucket = self.meta_config.s3_bucket
        prefix = self.meta_config.s3_prefix
        print(f' ------------ bucket: {bucket} ------------------')
        print(f' ------------ prefix: {prefix} ------------------')
        print(f' ------------ bucket: {self.meta_config.s3_bucket} ------------------')
        print(bucket is self.meta_config.s3_bucket)
        print()
        ####### 1. NOAA S3 Clean Bucket
        #if self.s3_bucket == 'noaa-reanalyses-pds' or self.s3_bucket == 'aws_s3':
        if bucket == 'noaa-reanalyses-pds': #or bucket == 'aws_s3':
            #print(f'!!!! {self.s3_bucket}')
            print(f'  ------ {self.s3_bucket} -----------------------------------------------------------------')
            print(f'Running get_bufr_file_meta for NOAA S3 Clean Bucket (aws_s3) {self.s3_bucket}')

            temp_uuid = str(uuid.uuid4())

            work_dir = os.path.join(self.meta_config.work_dir, temp_uuid)

            print(f'inventory_bufr_files: {inventory_bufr_files}')
            print(f'scrub_files: {self.meta_config.scrub_files}')
            for idx, bufr_file in inventory_bufr_files.iterrows():
                file_downloaded = False
                print(
                   f'bufr_file: {bufr_file}')

                saved_filename = download_bufr_file_from_s3(work_dir, bufr_file)

                if saved_filename is None:
                    continue

                self.get_obs_counts_with_sinv(saved_filename, bufr_file)

                # clean up files
                if self.meta_config.scrub_files:
                    #os.remove( saved_filename )
                    shutil.rmtree( work_dir )
              
        ####### 2. NASA Discover
        elif self.s3_bucket == None or self.s3_bucket == 'discover' or self.s3_bucket == '':
            #get_s3_bucket(self)
            print(f'  ------ {self.s3_bucket} -----------------------------------------------------------------')
            print(f'Running get_bufr_file_meta for NASA Discover {self.s3_bucket}')

            temp_uuid = str(uuid.uuid4())

            work_dir = os.path.join(self.meta_config.work_dir, temp_uuid)

            #print(f'self.meta_config.platform: {self.platform}')
            #print(f'self.meta_config.s3_bucket: {self.s3_bucket}')
            #print(f'inventory_bufr_files: {inventory_bufr_files}')
            #print(f'scrub_files: {self.meta_config.scrub_files}')
            for idx, bufr_file in inventory_bufr_files.iterrows():
                file_downloaded = False
                print(
                   f'bufr_file: {bufr_file}')

                #if self.meta_config.s3_bucket == 'noaa-reanalyses-pds':
                #    print(#f's3_bucket: {self.s3_bucket} *********** !!!! '
                #          f's3_bucket.meta_config: {self.meta_config.s3_bucket} *********** !!!! ')
                #    saved_filename = download_bufr_file_from_s3(work_dir, bufr_file)
                try:
                    saved_filename = bufr_file['full_path'] 
                except Exception as err:
                    msg = f'\'saved_filename\' line 147 - err: {err}'
                    raise ValueError(msg) from err 

                print(
                   f'work_dir: {work_dir}')
                print(
                   f'saved_filename: {saved_filename}')

                if saved_filename is None:
                    continue

                self.get_obs_counts_with_sinv(saved_filename, bufr_file)

                # clean up files
                #if self.meta_config.scrub_files:
                    #os.remove( saved_filename )
                    #shutil.rmtree( work_dir )



    def get_obs_counts_with_sinv(self, filename, bufr_file):
        
        args = [filename]
        cmd = sch.SubprocessCmdHandler(
            nc_cmds.NCEPLIBS_SINV,
            nc_cmds.nceplibs_cmds,
            args
        )
        print(f'cmd: {cmd}')

        if not cmd.send():
            return False

        cmd.post_cmd_result(bufr_file.obs_day)

        sinv_lines_meta = cmd.parse_output(bufr_file)
        for meta in sinv_lines_meta:
            print(f'meta: {meta}')

    
        cmd.post_parsed_result(sinv_lines_meta, bufr_file)
        

@dataclass
class ObsPrepBufrFileMetaHandler(object):
    meta_config: ObsMetaCMPBQMConfig
    prepbufr_files: list = field(default_factory=list, init=False)
    date_range: DateRange = field(init=False)

    def __post_init__(self):
        self.date_range = self.meta_config.get_date_range()
        self.prepbufr_files = self.meta_config.get_prepbufr_file_list()

    def __repr__(self):
        """
        string representation of ObsPrepBufrFileMetaHandler globals
        """
        return f'meta_config: {self.meta_config}, ' \
            f'prepbufr_files: {self.prepbufr_files}, ' \
            f'date_range: {self.date_range}'

    def get_prepbufr_file_meta(self, cmd_type):

        inventory_prepbufr_files = oiq.get_bufr_files_data(
            self.prepbufr_files,
            self.date_range.start,
            self.date_range.end
        )

        temp_uuid = str(uuid.uuid4())

        work_dir = os.path.join(self.meta_config.work_dir, temp_uuid)

        print(f'inventory_prepbufr_files: {inventory_prepbufr_files}')
        print(f'scrub_files: {self.meta_config.scrub_files}')
        for idx, prepbufr_file in inventory_prepbufr_files.iterrows():
            print(
               f'bufr_file: {prepbufr_file}')

            saved_filename = download_bufr_file_from_s3(work_dir, prepbufr_file)

            if saved_filename is None:
                continue

            self.get_obs_counts_with_cmpbqm(saved_filename, prepbufr_file)

            # clean up files
            if self.meta_config.scrub_files:
                shutil.rmtree( work_dir )

    def get_obs_counts_with_cmpbqm(self, filename, prepbufr_file):
        args = [filename]
        cmd = sch.SubprocessCmdHandler(
            nc_cmds.NCEPLIBS_CMPBQM,
            nc_cmds.nceplibs_cmds,
            args
        )
        print(f'cmd: {cmd}')

        if not cmd.send():
            return False
        
        cmd.post_cmd_result(prepbufr_file.obs_day)

        cmpbqm_lines_meta = cmd.parse_output(prepbufr_file)
        for meta in cmpbqm_lines_meta:
            print(f'meta: {meta}')
        
        cmd.post_parsed_result(cmpbqm_lines_meta, prepbufr_file)
