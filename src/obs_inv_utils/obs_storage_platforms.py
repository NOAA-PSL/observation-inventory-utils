HERA_HPSS = 'hera_hpss'
HERA_SCRATCH = 'hera_scratch' 
AWS_S3 = 'aws_s3'
AWS_S3_CLEAN = 'aws_s3_clean'
AZURE_BLOB = 'azure_blob'
DISCOVER = 'discover'

PLATFORMS = [HERA_HPSS, HERA_SCRATCH, AWS_S3, AWS_S3_CLEAN, AZURE_BLOB, DISCOVER]

def is_valid(storage_location):
    if storage_location in PLATFORMS:
        return True

    return False
