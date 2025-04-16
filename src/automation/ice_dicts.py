import automation_utils as au
from automation_utils import InventoryInfo

icec_emc_dmsp_v2 = InventoryInfo(
    obs_name='icec_emc_dmsp_v2',
    key='observations/reanalysis/icec/emc/dmsp/%Y/%m/24h/iodav2/icec.emc.ssmi_l1b_dmsp.%Y%m%d.T%H%M%SZ.iodav2.nc',
    start='20030601T120000Z',
    s3_prefix='observations/reanalysis/icec/emc/dmsp/%Y/%m/24h/iodav2/',
    files='icec.emc.ssmi_l1b_dmsp.%z.iodav2.nc',
    inv_cmd=au.HV_IODA_META,
    cycling_interval=au.CYCLING_DAILY,
    platform=au.CLEAN_PLATFORM
)

icec_emc_dmsp_v3 = InventoryInfo(
    obs_name='icec_emc_dmsp_v3',
    key='observations/reanalysis/icec/emc/dmsp/%Y/%m/24h/iodav3/icec.emc.ssmi_l1b_dmsp.%Y%m%d.T%H%M%SZ.iodav3.nc',
    start='20030601T120000Z',
    s3_prefix='observations/reanalysis/icec/emc/dmsp/%Y/%m/24h/iodav3/',
    files='icec.emc.ssmi_l1b_dmsp.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META,
    cycling_interval=au.CYCLING_DAILY,
    platform=au.CLEAN_PLATFORM
)

icec_nsidc_nh_v2 = InventoryInfo(
    obs_name='icec_nsidc_nh_v2',
    key='observations/reanalysis/icec/nsidc/nh/%Y/%m/24h/iodav2/icec.nsidc.nh.%Y%m%d.T%H%M%SZ.iodav2.nc',
    start='19790601T120000Z',
    s3_prefix='observations/reanalysis/icec/nsidc/nh/%Y/%m/24h/iodav2/',
    files='icec.nsidc.nh.%z.iodav2.nc',
    inv_cmd=au.HV_IODA_META,
    cycling_interval=au.CYCLING_DAILY,
    platform=au.CLEAN_PLATFORM
)

icec_nsidc_nh_v3 = InventoryInfo(
    obs_name='icec_nsidc_nh_v3',
    key='observations/reanalysis/icec/nsidc/nh/%Y/%m/24h/iodav3/icec.nsidc.nh.%Y%m%d.T%H%M%SZ.iodav3.nc',
    start='20030601T120000Z',
    s3_prefix='observations/reanalysis/icec/nsidc/nh/%Y/%m/24h/iodav3/',
    files='icec.nsidc.nh.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META,
    cycling_interval=au.CYCLING_DAILY,
    platform=au.CLEAN_PLATFORM
)

icec_nsidc_sh_v2 = InventoryInfo(
    obs_name='icec_nsidc_sh_v2',
    key='observations/reanalysis/icec/nsidc/sh/%Y/%m/24h/iodav2/icec.nsidc.sh.%Y%m%d.T%H%M%SZ.iodav2.nc',
    start='19790601T120000Z',
    s3_prefix='observations/reanalysis/icec/nsidc/sh/%Y/%m/24h/iodav2/',
    files='icec.nsidc.sh.%z.iodav2.nc',
    inv_cmd=au.HV_IODA_META,
    cycling_interval=au.CYCLING_DAILY,
    platform=au.CLEAN_PLATFORM
)

icec_nsidc_sh_v3 = InventoryInfo(
    obs_name='icec_nsidc_sh_v3',
    key='observations/reanalysis/icec/nsidc/sh/%Y/%m/24h/iodav3/icec.nsidc.sh.%Y%m%d.T%H%M%SZ.iodav3.nc',
    start='20030601T120000Z',
    s3_prefix='observations/reanalysis/icec/nsidc/sh/%Y/%m/24h/iodav3/',
    files='icec.nsidc.sh.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META,
    cycling_interval=au.CYCLING_DAILY,
    platform=au.CLEAN_PLATFORM
)

icefb_esa_cryosat2_v2 = InventoryInfo(
    obs_name='icefb_esa_cryosat2_v2',
    key='observations/reanalysis/icefb/esa/cryosat2/%Y/%m/24h/iodav2/icefb.esa.l2_cryosat2.%Y%m%d.T%H%M%SZ.iodav2.nc',
    start='20100906T120000Z',
    s3_prefix='observations/reanalysis/icefb/esa/cryosat2/%Y/%m/24h/iodav2/',
    files='icefb.esa.l2_cryosat2.%z.iodav2.nc',
    inv_cmd=au.HV_IODA_META,
    cycling_interval=au.CYCLING_DAILY,
    platform=au.CLEAN_PLATFORM
)

icefb_esa_cryosat2_v3 = InventoryInfo(
    obs_name='icefb_esa_cryosat2_v3',
    key='observations/reanalysis/icefb/esa/cryosat2/%Y/%m/24h/iodav3/icefb.esa.l2_cryosat2.%Y%m%d.T%H%M%SZ.iodav3.nc',
    start='20100906T120000Z',
    s3_prefix='observations/reanalysis/icefb/esa/cryosat2/%Y/%m/24h/iodav3/',
    files='icefb.esa.l2_cryosat2.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META,
    cycling_interval=au.CYCLING_DAILY,
    platform=au.CLEAN_PLATFORM
)

ice_infos = [icec_emc_dmsp_v2, icec_emc_dmsp_v3, icec_nsidc_nh_v2, icec_nsidc_nh_v3, icec_nsidc_sh_v2, icec_nsidc_sh_v3, icefb_esa_cryosat2_v2,
             icefb_esa_cryosat2_v3, ]