import automation_utils as au
from automation_utils import InventoryInfo

ozone_nasa_mls = InventoryInfo(
    obs_name='ozone_nasa_mls',
    key='observations/reanalysis/ozone/nasa/mls/%Y/%m/netcdf/MLS-v5.0-oz.%Y%m%d_%Hz.nc',
    start='20040801T000000Z',
    s3_prefix='observations/reanalysis/ozone/nasa/mls/%Y/%m/netcdf/',
    files='MLS-v5.0-oz.%z.nc',
    inv_cmd=au.HV_OZONE_NC_META,
    cycling_interval=au.CYCLING_6H,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

ozone_nasa_omieff = InventoryInfo(
    obs_name='ozone_nasa_omieff',
    key='observations/reanalysis/ozone/nasa/omi-eff/%Y/%m/netcdf/OMIeff-adj.%Y%m%d_%Hz.nc',
    start='20041001T000000Z',
    s3_prefix='observations/reanalysis/ozone/nasa/omi-eff/%Y/%m/netcdf/',
    files='OMIeff-adj.%z.nc',
    inv_cmd=au.HV_OZONE_NC_META,
    cycling_interval=au.CYCLING_6H,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

ozone_nasa_ompslp = InventoryInfo(
    obs_name='ozone_nasa_ompslp',
    key='observations/reanalysis/ozone/nasa/omps-lp/%Y/%m/netcdf/OMPS-LPoz-Vis.%Y%m%d_%Hz.nc',
    start='20120101T000000Z',
    s3_prefix='observations/reanalysis/ozone/nasa/omps-lp/%Y/%m/netcdf/',
    files='OMPS-LPoz-Vis.%z.nc',
    inv_cmd=au.HV_OZONE_NC_META,
    cycling_interval=au.CYCLING_6H,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

ozone_nasa_ompsnmeff = InventoryInfo(
    obs_name='ozone_nasa_ompsnmeff',
    key='observations/reanalysis/ozone/nasa/omps-nm-eff/%Y/%m/netcdf/OMPSNM.%Y%m%d_%Hz.nc',
    start='20121201T000000Z',
    s3_prefix='observations/reanalysis/ozone/nasa/omps-nm-eff/%Y/%m/netcdf/',
    files='OMPSNM.%z.nc',
    inv_cmd=au.HV_OZONE_NC_META,
    cycling_interval=au.CYCLING_6H,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

ozone_nasa_ompsnm = InventoryInfo(
    obs_name='ozone_nasa_ompsnm',
    key='observations/reanalysis/ozone/nasa/omps-nm/%Y/%m/netcdf/OMPSNP.%Y%m%d_%Hz.nc',
    start='20130101T000000Z',
    s3_prefix='observations/reanalysis/ozone/nasa/omps-nm/%Y/%m/netcdf/',
    files='OMPSNP.%z.nc',
    inv_cmd=au.HV_OZONE_NC_META,
    cycling_interval=au.CYCLING_6H,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

ozone_infos = [ozone_nasa_mls, ozone_nasa_omieff, ozone_nasa_ompslp]