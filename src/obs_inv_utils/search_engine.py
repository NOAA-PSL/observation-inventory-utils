from collections import namedtuple
import json
import os
import pathlib
from datetime import datetime
from obs_inv_utils import hpss_io_interface as hpss
from obs_inv_utils import obs_storage_platforms as platforms
from config_handlers.obs_search_conf import ObservationsConfig, ObsSearchConfig
from obs_inv_utils import aws_s3_interface as s3
from obs_inv_utils import time_utils
from obs_inv_utils.time_utils import DateRange
from obs_inv_utils.hpss_io_interface import HpssTarballContents, HpssFileMeta
from obs_inv_utils.hpss_io_interface import HpssCommandRawResponse
from obs_inv_utils.aws_s3_interface import AwsS3CommandRawResponse
from typing import Optional
from dataclasses import dataclass, field
from obs_inv_utils import inventory_table_factory as tbl_factory

SECONDS_IN_A_DAY = 24*3600

hpss_inspect_tarball = hpss.hpss_cmds[hpss.CMD_INSPECT_TARBALL]

FilenameMeta = namedtuple(
    'FilenameMeta',
    [
        'prefix',
        'cycle_tag',
        'data_type',
        'cycle_time',
        'data_format',
        'suffix',
        'not_restricted_tag'
    ],
)

TarballFileMeta = namedtuple(
    'TarballFileMeta',
    [
        'cmd_result_id',
        'filename',
        'parent_dir',
        'platform',
        's3_bucket',
        'prefix',
        'cycle_tag',
        'data_type',
        'cycle_time',
        'obs_day',
        'data_format',
        'suffix',
        'nr_tag',
        'file_size',
        'permissions',
        'last_modified',
        'submitted_at',
        'latency',
        'inserted_at',
        'valid_at',
        'etag'
    ],
)

HpssCmdResult = namedtuple(
    'HpssCmdResult',
    [
        'command',
        'arg0',
        'raw_output',
        'raw_error',
        'error_code',
        'obs_day',
        'submitted_at',
        'latency'
    ],
)

AwsS3CmdResult = namedtuple(
    'HpssCmdResult',
    [
        'command',
        'arg0',
        'raw_output',
        'raw_error',
        'error_code',
        'obs_cycle_time',
        'submitted_at',
        'latency'
    ],
)


# filename parts definitions
PREFIX = 0
CYCLE_TAG = 1
DATA_TYPE = 2

OBS_FORMAT_BUFR = 'bufr'
OBS_FORMAT_BUFR_D = 'bufr_d'
OBS_FORMAT_GRB = 'grb'
OBS_FORMAT_GRIB2 = 'grib2'
OBS_FORMAT_UNKNOWN = 'unknown'
OBS_FORMATS = [
    OBS_FORMAT_BUFR,
    OBS_FORMAT_BUFR_D,
    OBS_FORMAT_GRB,
    OBS_FORMAT_GRIB2
]

ADDITIONAL_GRIB2_FORMAT_EXTENSIONS = ['1536', '576']


def get_cycle_tag(parts):
    if not isinstance(parts, list) or len(parts) < 2:
        return None
    return parts[CYCLE_TAG]


def get_data_type(parts):
    if not isinstance(parts, list) or len(parts) < 3:
        return None
    return parts[DATA_TYPE]


def get_cycle_time(tag):
    try:
        cycle_time = datetime.strptime(tag, 't%HZ')
        seconds = (cycle_time - datetime(1900, 1, 1)).total_seconds()
    except Exception as e:
        print(f'Not a valid cycle time: {tag}, error: {e}')
        return None

    if seconds < 0 or seconds > time_utils.SECONDS_IN_A_DAY:
        return None

    return int(seconds)


def get_data_format(filename):
    # strip '.nr' from filename
    if not isinstance(filename, str):
        return OBS_FORMAT_UNKNOWN

    fn = filename.removesuffix('.nr')
    file_ext = (pathlib.Path(fn).suffix).replace('.', '', 1)

    if file_ext in OBS_FORMATS:
        return file_ext

    for obs_format in OBS_FORMATS:
        if fn.endswith(obs_format):
            return obs_format

    if file_ext in ADDITIONAL_GRIB2_FORMAT_EXTENSIONS:
        return OBS_FORMAT_GRIB2

    for obs_format in OBS_FORMATS:
        if obs_format in fn:
            return obs_format

    return OBS_FORMAT_UNKNOWN


def get_combined_suffix(parts):
    if not isinstance(parts, list) or len(parts) < 4:
        return None

    suffix_parts = parts[3:]
    suffix = ''
    for part in suffix_parts:
        if not isinstance(part, str):
            print(f'Bad filename parts: {parts}, each part must be a string')
            return None
        suffix += '.' + part

    if suffix == '':
        return None

    return suffix


def parse_filename(filename):
    parts = filename.split('.')
    cycle_tag = get_cycle_tag(parts)
    filename_meta = FilenameMeta(
        parts[PREFIX],
        cycle_tag,
        get_data_type(parts),
        get_cycle_time(cycle_tag),
        get_data_format(filename),
        get_combined_suffix(parts),
        filename.endswith('.nr')
    )

    return filename_meta


def parse_filename_clean_bucket(filename):
    parts = filename.split('.')
    del parts[1] # clean bucket has one extra part. the rest are the same as the dirty bucket
    cycle_tag = get_cycle_tag(parts)
    filename_meta = FilenameMeta(
        parts[PREFIX],
        cycle_tag,
        get_data_type(parts),
        get_cycle_time(cycle_tag),
        get_data_format(filename),
        get_combined_suffix(parts),
        filename.endswith('.nr')
    )

    return filename_meta


def process_aws_s3_list_objects_v2_resp(cmd_result_id, contents):
    if not isinstance(contents, s3.AwsS3ObjectsListContents):
        return None

    listed_objects = contents.listed_objects

    files_meta = []
    print(f'inside process_aws_s3_list_objects - cmd_result_id: {cmd_result_id}')
    for listed_object in listed_objects:
        fn = listed_object.name
        print(f'filename: {fn}')
        fn_meta = parse_filename(fn)
        print(f'filename meta: {fn_meta}')

        file_meta = TarballFileMeta(
            cmd_result_id,
            fn,
            contents.prefix,
            platforms.AWS_S3,
            s3.AWS_BDP_BUCKET,
            fn_meta.prefix,
            fn_meta.cycle_tag,
            fn_meta.data_type,
            fn_meta.cycle_time,
            contents.obs_cycle_time,
            fn_meta.data_format,
            fn_meta.suffix,
            fn_meta.not_restricted_tag,
            listed_object.size,
            '',
            listed_object.last_modified,
            contents.submitted_at,
            contents.latency,
            datetime.utcnow(),
            datetime.utcnow(),
            listed_object.etag
        )
        files_meta.append(file_meta)

    if len(files_meta) > 0:
        tbl_factory.insert_obs_inv_items(files_meta)

def process_aws_s3_clean_resp(cmd_result_id, contents):
    if not isinstance(contents, s3.AwsS3ObjectsListContents):
        return None

    listed_objects = contents.listed_objects

    files_meta = []
    print(f'inside process_aws_s3_list_objects - cmd_result_id: {cmd_result_id}')
    print(f'inside process_aws_s3_list_objects - contents: {contents}')
    fn = os.path.basename(contents.prefix)
    print(f'filename: {fn}')
    fn_meta = parse_filename_clean_bucket(fn)
    print(f'filename meta: {fn_meta}')

    listed_object = listed_objects[0]
    files_meta.append(TarballFileMeta(
            cmd_result_id,
            fn,
            os.path.dirname(contents.prefix) + "/",
            platforms.AWS_S3, # using AWS_S3 instead of AWS_S3_CLEAN to enable sinv work properly
            s3.AWS_BDP_BUCKET,
            fn_meta.prefix,
            fn_meta.cycle_tag,
            fn_meta.data_type,
            fn_meta.cycle_time,
            contents.obs_cycle_time,
            fn_meta.data_format,
            fn_meta.suffix,
            fn_meta.not_restricted_tag,
            listed_object.size,
            '',
            listed_object.last_modified,
            contents.submitted_at,
            contents.latency,
            datetime.utcnow(),
            datetime.utcnow(),
            listed_object.etag
    ))

    if len(files_meta) > 0:
        tbl_factory.insert_obs_inv_items(files_meta)

def process_inspect_tarball_resp(cmd_result_id, contents):
    if not isinstance(contents, hpss.HpssTarballContents):
        return None

    inspected_files = contents.inspected_files

    tarball_files_meta = []

    for inspected_file in inspected_files:
        fn = inspected_file.name
        print(f'filename: {fn}')
        fn_meta = parse_filename(fn)
        print(f'filename meta: {fn_meta}')

        tarball_file_meta = TarballFileMeta(
            cmd_result_id,
            fn,
            contents.parent_dir,
            platforms.HPSS_HERA,
            '',
            fn_meta.prefix,
            fn_meta.cycle_tag,
            fn_meta.data_type,
            fn_meta.cycle_time,
            contents.observation_day,
            fn_meta.data_format,
            fn_meta.suffix,
            fn_meta.not_restricted_tag,
            inspected_file.size,
            inspected_file.permissions,
            inspected_file.last_modified,
            contents.submitted_at,
            contents.latency,
            datetime.utcnow(),
            datetime.utcnow(),
            ''
        )
        tarball_files_meta.append(tarball_file_meta)

    tbl_factory.insert_obs_inv_items(tarball_files_meta)


def default_datetime_converter(obj):
   if isinstance(obj, datetime):
      return obj.__str__()


def post_aws_s3_cmd_result(raw_response, obs_cycle_time):
    if not isinstance(raw_response, AwsS3CommandRawResponse):
        msg = 'raw_response must be of type AwsS3CommandRawResponse. It is'\
              f' actually of type: {type(raw_response)}'
        raise TypeError(msg)

    output_str = json.dumps(raw_response.output,
                            default=default_datetime_converter)
    cmd_result_data = tbl_factory.CmdResultData(
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

    cmd_result_id = tbl_factory.insert_cmd_result(cmd_result_data)
    return cmd_result_id


def post_hpss_cmd_result(raw_response, obs_day):
    if not isinstance(raw_response, HpssCommandRawResponse):
        msg = 'raw_response must be of type HpssCommandRawResponse. It is'\
              f' actually of type: {type(raw_response)}'
        raise TypeError(msg)

    cmd_result_data = tbl_factory.CmdResultData(
        raw_response.command,
        raw_response.args_0,
        raw_response.output,
        raw_response.error,
        raw_response.return_code,
        obs_day,
        raw_response.submitted_at,
        raw_response.latency,
        datetime.utcnow()
    )

    print(f'HPSS cmd_result: {cmd_result_data}')
    cmd_result_id = tbl_factory.insert_cmd_result(cmd_result_data)

    return cmd_result_id


@dataclass
class ObsInventorySearchEngine(object):
    obs_inv_conf: ObservationsConfig
    search_configs: list[ObsSearchConfig] = field(default_factory=list)
    cmd_post_id: int = field(default_factory=int, init=False)

    def __post_init__(self):
        self.search_configs = self.obs_inv_conf.get_obs_inv_search_configs()

    def get_obs_file_info(self):

        date_range = self.obs_inv_conf.get_search_date_range()
        master_list = []
        print(f'search config date range: {date_range}')

        all_search_paths_finished = False
        loop_count = 0
        while not all_search_paths_finished:
            print(
                f'loop {loop_count} of while loop, all_search_paths_finished: {all_search_paths_finished}')
            loop_count += 1
            finished_count = 0
            for key, search_config in self.search_configs.items():
                # print(f'search_config: {search_config}')
                search_path = search_config.get_current_search_path()

                if search_config.get_date_range().at_end():
                    end = search_config.get_date_range().end
                    finished_count += 1
                    print(f'Finished search, path: {search_path}, end: {end}')
                    continue

                args = [search_path]
                print(f'args: {args}, search_path: {search_path}')
                platform = search_config.get_storage_platform()
                n_hours = 6
                n_days = 0
                if platform == platforms.AWS_S3 or platform == platforms.AWS_S3_CLEAN:
                    cmd = s3.AwsS3CommandHandler(s3.CMD_GET_S3_OBJ_LIST, args)
                elif platform == platforms.HERA_HPSS:
                    cmd = hpss.HpssCommandHandler(
                        hpss.CMD_INSPECT_TARBALL, args)
                    n_hours = 0
                    n_days = 1

                print(f'cmd: {cmd}, finished_count: {finished_count}')

                success = cmd.send()

                raw_resp = cmd.get_raw_response()

                if platform == platforms.AWS_S3 or platform == platforms.AWS_S3_CLEAN:
                    print('posting command results for aws s3')
                    self.cmd_post_id = post_aws_s3_cmd_result(
                        raw_resp,
                        search_config.get_date_range().current
                    )
                elif platform == platforms.HERA_HPSS:
                    self.cmd_post_id = post_hpss_cmd_result(
                        raw_resp,
                        search_config.get_date_range().current
                    )

                print(f'self.cmd_post_id: {self.cmd_post_id}')

                if success:
                    current_time = search_config.get_date_range().current
                    print(f'current_time: {current_time}')
                    contents = cmd.parse_response(current_time)

                    if platform == platforms.AWS_S3:
                        file_meta = process_aws_s3_list_objects_v2_resp(
                            self.cmd_post_id,
                            contents
                        )
                    elif platform == platforms.AWS_S3_CLEAN:
                        file_meta = process_aws_s3_clean_resp(
                            self.cmd_post_id,
                            contents
                        )
                    elif platform == platforms.HERA_HPSS:
                        file_meta = process_inspect_tarball_resp(
                            self.cmd_post_id,
                            contents
                        )
                else:
                    msg = f'Command failed!!!!!!!!!!!!!!!!!!!!!!!!!!!!! - error code: {cmd.get_raw_response}.'
                    print(msg)

                raw_resp = cmd.get_raw_response()

                search_config.get_date_range().increment(days=n_days, hours=n_hours)
                print(f'Current search path: {search_path}')

            if finished_count == len(self.search_configs):
                all_search_paths_finished = True
