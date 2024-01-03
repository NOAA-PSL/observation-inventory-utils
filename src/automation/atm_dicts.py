import automation_utils as au
from automation_utils import InventoryInfo



airs_airsev = InventoryInfo(
    obs_name='airs_airsev',
    key='observations/reanalysis/airs/airsev/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.airsev.tm00.bufr_d',
    start='20070201T000000Z',
    platform=au.CLEAN_PLATFORM,
    cycling_interval='21600',
    s3_bucket=au.REANALYSIS_BUCKET,
    s3_prefix='observations/reanalysis/airs/airsev/%Y/%m/bufr/',
    bufr_files='gdas.%z.airsev.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV
)

airs_aqua = InventoryInfo(
    obs_name='airs_aqua',
    key='observations/reanalysis/airs/nasa/aqua/%Y/%m/bufr/airs_disc_final.%Y%m%d.t%Hz.bufr',
    start='20020831T000000Z',
    platform=au.CLEAN_PLATFORM,
    cycling_interval='21600',
    s3_bucket=au.REANALYSIS_BUCKET,
    s3_prefix='observations/reanalysis/airs/nasa/aqua/%Y/%m/bufr/',
    bufr_files='airs_disc_final.%z.bufr',
    nceplibs_cmd=au.NCEPLIBS_SINV
)

amsua_1bamua = InventoryInfo(
    obs_name='amsua_1bamua',
    key='observations/reanalysis/amsua/1bamua/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.1bamua.tm00.bufr_d',
    start='19981026T000000Z',
    platform=au.CLEAN_PLATFORM,
    cycling_interval='21600',
    s3_bucket=au.REANALYSIS_BUCKET,
    s3_prefix='observations/reanalysis/amsua/1bamua/%Y/%m/bufr/',
    bufr_files='gdas.%z.1bamua.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV
)



atm_infos = [airs_airsev, airs_aqua, amsua_1bamua]