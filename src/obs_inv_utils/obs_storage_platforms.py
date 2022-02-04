HERA_HPSS = 'hera_hpss'
HERA_SCRATCH = 'hera_scratch' 
AWS_S3 = 'aws_s3'
AZURE_BLOB = 'azure_blob'

PLATFORMS = [HERA_HPSS, HERA_SCRATCH, AWS_S3, AZURE_BLOB]

def is_valid(storage_location):
    if storage_location in PLATFORMS:
        return True

    return False
