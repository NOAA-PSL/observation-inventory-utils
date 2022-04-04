import re
import attr
from collections import namedtuple, OrderedDict
import boto3
from datetime import datetime
from botocore.config import Config
from botocore import UNSIGNED


bdp_config = Config(
    region_name = 'us-east-1',
    signature_version = UNSIGNED,
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)

nl = '\n'

AwsS3ObjectsListContents = namedtuple(
    'AwsS3ObjectsListContents',
    [
        'prefix',
        'files_count',
        'listed_objects',
        'obs_cycle_time',
        'submitted_at',
        'latency'
    ],
)

AwsS3CommandRawResponse = namedtuple(
    'AwsS3CommandRawResponse',
    [
        'command',
        'return_code',
        'output',
        'success',
        'args_0',
        'submitted_at',
        'latency'
    ],
)


AwsS3FileMeta = namedtuple(
    'AwsS3FileMeta',
    [
        'name',
        'permissions',
        'last_modified',
        'size'
    ],
)


AwsS3Command = namedtuple(
    'AwsS3Command',
    [
        'command',
        'arg_validator',
        'output_parser'
    ],
)

AWS_BDP_BUCKET = 'noaa-reanalyses-pds'
CMD_GET_S3_OBJ_LIST = 'list_objects'


def get_bdp_s3_client():
    try:
        client = boto3.client('s3', config=bdp_config)
    except Exception as e:
        msg = f'Problem getting boto3 s3 client - error: {e}'
        raise ValueError(msg)

    return client


def get_s3_objects_list(client, bucket=None, prefix=None):
    try:
        response = client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    except Exception as e:
        msg = f'Problem getting list for prefix: {prefix}, error: {e}'
        print(msg)

    return response
        

def get_objects_list_args_valid(args):
    if not isinstance(args, list):
        msg = f'Args must be in the form of a list, args: {args}'
        raise TypeError(msg)
    cmd = aws_s3_cmds[CMD_GET_S3_OBJ_LIST].command
    print(f'{nl}{nl}In inspect tarball args valid: cmd: {cmd}{nl}{nl}')
    if (len(args) > 1 or len(args) == 0):
        msg = f'Command "{cmd}" accepts exactly 1 argument, received ' \
              f'{len(args)}.'
        raise ValueError(msg)

    arg = args[0]

    try:
        m = re.search(r'[^A-Za-z0-9\._\-\/]', arg)
        if m is not None and m.group(0) is not None:
            print('Only a-z A-Z 0-9 and - . / _ characters allowed in filepath')
            raise ValueError(f'Invalid characters found in file path: {arg}')
    except Exception as e:
        raise ValueError(f'Invalid file path: {e}')

    return True


def s3_object_list_v2_parser(obj_list_contents, obs_cycle_time):
    if not isinstance(obj_list_contents, AwsS3CommandRawResponse):
        msg = f'Response needs to be an instance type AwsS3CommandRawResponse.'\
              f'Received type: {type(obj_list_contents)}'
        raise TypeError(msg)

    # print(f'obs_cycle_time: {obs_cycle_time}, contents: {obj_list_contents}')

    object_list = obj_list_contents.output.get('Contents')
    # print(f'object_list: {object_list}')

    files_meta = list()
    prefix = obj_list_contents.args_0
    permissions = ''
    file_count = len(object_list)

    for object_item in object_list:
        print(f'object_item: {object_item}')

        size = object_item.get('Size')
        last_modified = object_item.get('LastModified')
        fn_str = object_item.get('Key')
        fn = fn_str[len(prefix):]
        
        print(f'fn: {fn}')
        files_meta.append(
            AwsS3FileMeta(fn, permissions, last_modified, size))

    # print(f'files_meta: {files_meta}')
    return AwsS3ObjectsListContents(
        prefix,
        file_count,
        files_meta,
        obs_cycle_time,
        obj_list_contents.submitted_at,
        obj_list_contents.latency
    )


aws_s3_cmds = {
    'list_objects': AwsS3Command(
        get_s3_objects_list,
        get_objects_list_args_valid,
        s3_object_list_v2_parser,
    )
}


def is_valid_aws_s3_cmd(instance, attribute, value):
    print(f'In is_valid_aws_s3_cmd: value: {value}')
    if value not in aws_s3_cmds:
        msg = f'AWS s3 command {value} is not valid. Use one of: ' \
              f'{aws_s3_cmds.keys()}'
        raise KeyError(msg)
    return True


@attr.s(slots=True)
class AwsS3CommandHandler(object):

    command = attr.ib(validator=is_valid_aws_s3_cmd)
    args = attr.ib(default=attr.Factory(list))
    kwargs = attr.ib(init=False)
    cmd_obj = attr.ib(init=False)
    raw_resp = attr.ib(default=None)
    submitted_at = attr.ib(default=None)
    finished_at = attr.ib(default=None)
    client = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.cmd_obj = aws_s3_cmds[self.command]
        print(f'In __attrs_post_init__: self.args: {self.args}')
        if self.cmd_obj.arg_validator(self.args):
            self.kwargs = {'bucket': AWS_BDP_BUCKET, 'prefix': self.args[0]}

        self.client = get_bdp_s3_client()
        print(f'kwargs: {self.kwargs}')


    def send(self):
        try:
            self.submitted_at = datetime.utcnow()
            response = self.cmd_obj.command(self.client, **self.kwargs)
            self.finished_at = datetime.utcnow()
        except Exception as e:
            msg = f'Error after sending command {self.command}, error: {e}.'
            raise ValueError(msg)
        response_type = type(response)
        # print(f'type(response): {response_type}, response: {response}')
        resp_meta = response.get('ResponseMetadata')
        # print(f'resp_meta: {resp_meta}')
        self.raw_resp = response
        returncode = 404
        contents = response.get('Contents')
        # print(f'contents: {contents}')
        if resp_meta is not None:
            returncode = resp_meta.get('HTTPStatusCode')
            if contents is None:
                returncode = 404

        self.raw_resp = AwsS3CommandRawResponse(
            self.command,
            returncode,
            response,
            (returncode == 200),
            self.args[0],
            self.submitted_at,
            float(self.get_cmd_duration())
        )

        print(f'raw_resp: {self.raw_resp}')

        return (returncode == 200)


    def get_raw_response(self):
        return self.raw_resp


    def get_cmd_duration(self):
        diff = self.finished_at - self.submitted_at
        return (diff.seconds + diff.microseconds/1000000)


    def parse_response(self, obs_cycle_time):
        if self.raw_resp is not None:
            return self.cmd_obj.output_parser(self.raw_resp, obs_cycle_time)
        else:
            return None
