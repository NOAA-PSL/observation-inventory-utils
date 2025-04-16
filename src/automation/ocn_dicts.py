import automation_utils as au
from automation_utils import InventoryInfo

adt_nesdis_cryosat2_v2 = InventoryInfo(
    obs_name='adt_nesdis_cryosat2_v2',
    key='observations/reanalysis/adt/nesdis/cryosat2/%Y/%m/24h/iodav2/cryosat2.nesdis.adt.%Y%m%d.T%H%M%SZ.iodav2.nc',
    start='20100716T000000Z',
    s3_prefix='observations/reanalysis/adt/nesdis/cryosat2/%Y/%m/24h/iodav2/',
    files='cryosat2.nesdis.adt.%z.iodav2.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET,
)

adt_nesdis_cryosat2_v3 = InventoryInfo(
    obs_name='adt_nesdis_cryosat2_v3',
    key='observations/reanalysis/adt/nesdis/cryosat2/%Y/%m/24h/iodav3/cryosat2.nesdis.adt.%Y%m%d.T%H%M%SZ.iodav3.nc',
    start='20100716T000000Z',
    s3_prefix='observations/reanalysis/adt/nesdis/cryosat2/%Y/%m/24h/iodav3/',
    files='cryosat2.nesdis.adt.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET,
)

adt_nesdis_ers1_v2 = InventoryInfo(
    obs_name='adt_nesdis_ers1_v2',
    key='observations/reanalysis/adt/nesdis/ers1/%Y/%m/24h/iodav2/ers1.nesdis.adt.%Y%m%d.T%H%M%SZ.iodav2.nc',
    start='19930101T120000Z',
    s3_prefix='observations/reanalysis/adt/nesdis/ers1/%Y/%m/24h/iodav2/',
    files='ers1.nesdis.adt.%z.iodav2.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET,
)

adt_nesdis_ers1_v3 = InventoryInfo(
    obs_name='adt_nesdis_ers1_v3',
    key='observations/reanalysis/adt/nesdis/ers1/%Y/%m/24h/iodav3/ers1.nesdis.adt.%Y%m%d.T%H%M%SZ.iodav3.nc',
    start='19930101T120000Z',
    s3_prefix='observations/reanalysis/adt/nesdis/ers1/%Y/%m/24h/iodav3/',
    files='ers1.nesdis.adt.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET,
)

adt_nesdis_jason2_v2 = InventoryInfo(
    obs_name='adt_nesdis_jason2_v2',
    key='observations/reanalysis/adt/nesdis/jason2/%Y/%m/24h/iodav2/jason2.nesdis.adt.%Y%m%d.T%H%M%SZ.iodav2.nc',
    start='20080712T000000Z',
    s3_prefix='observations/reanalysis/adt/nesdis/jason2/%Y/%m/24h/iodav2/',
    files='jason2.nesdis.adt.%z.iodav2.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET,
)

adt_nesdis_jason2_v3 = InventoryInfo(
    obs_name='adt_nesdis_jason2_v3',
    key='observations/reanalysis/adt/nesdis/jason2/%Y/%m/24h/iodav3/jason2.nesdis.adt.%Y%m%d.T%H%M%SZ.iodav3.nc',
    start='20080712T000000Z',
    s3_prefix='observations/reanalysis/adt/nesdis/jason2/%Y/%m/24h/iodav3/',
    files='jason2.nesdis.adt.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET,
)

adt_nesdis_jason3_v2 = InventoryInfo(
    obs_name='adt_nesdis_jason3_v2',
    key='observations/reanalysis/adt/nesdis/jason3/%Y/%m/24h/iodav2/jason3.nesdis.adt.%Y%m%d.T%H%M%SZ.iodav2.nc',
    start='20160217T000000Z',
    s3_prefix='observations/reanalysis/adt/nesdis/jason3/%Y/%m/24h/iodav2/',
    files='jason3.nesdis.adt.%z.iodav2.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET,
)

adt_nesdis_jason3_v3 = InventoryInfo(
    obs_name='adt_nesdis_jason3_v3',
    key='observations/reanalysis/adt/nesdis/jason3/%Y/%m/24h/iodav3/jason3.nesdis.adt.%Y%m%d.T%H%M%SZ.iodav3.nc',
    start='20160217T000000Z',
    s3_prefix='observations/reanalysis/adt/nesdis/jason3/%Y/%m/24h/iodav3/',
    files='jason3.nesdis.adt.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET,
)

adt_nesdis_saral_v2 = InventoryInfo(
    obs_name='adt_nesdis_saral_v2',
    key='observations/reanalysis/adt/nesdis/saral/%Y/%m/24h/iodav2/saral.nesdis.adt.%Y%m%d.T%H%M%SZ.iodav2.nc',
    start='20130314T000000Z',
    s3_prefix='observations/reanalysis/adt/nesdis/saral/%Y/%m/24h/iodav2/',
    files='saral.nesdis.adt.%z.iodav2.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET,
)

adt_nesdis_saral_v3 = InventoryInfo(
    obs_name='adt_nesdis_saral_v3',
    key='observations/reanalysis/adt/nesdis/saral/%Y/%m/24h/iodav3/saral.nesdis.adt.%Y%m%d.T%H%M%SZ.iodav3.nc',
    start='20130314T000000Z',
    s3_prefix='observations/reanalysis/adt/nesdis/saral/%Y/%m/24h/iodav3/',
    files='saral.nesdis.adt.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET,
)

adt_nesdis_sentinel3a_v2 = InventoryInfo(
    obs_name='adt_nesdis_sentinel3a_v2',
    key='observations/reanalysis/adt/nesdis/sentinel3a/%Y/%m/24h/iodav2/sentinel3a.nesdis.adt.%Y%m%d.T%H%M%SZ.iodav2.nc',
    start='20160301T000000Z',
    s3_prefix='observations/reanalysis/adt/nesdis/sentinel3a/%Y/%m/24h/iodav2/',
    files='sentinel3a.nesdis.adt.%z.iodav2.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET,
)

adt_nesdis_sentinel3a_v3 = InventoryInfo(
    obs_name='adt_nesdis_sentinel3a_v3',
    key='observations/reanalysis/adt/nesdis/sentinel3a/%Y/%m/24h/iodav3/sentinel3a.nesdis.adt.%Y%m%d.T%H%M%SZ.iodav3.nc',
    start='20160301T000000Z',
    s3_prefix='observations/reanalysis/adt/nesdis/sentinel3a/%Y/%m/24h/iodav3/',
    files='sentinel3a.nesdis.adt.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET,
)

adt_nesdis_sentinel3b_v2 = InventoryInfo(
    obs_name='adt_nesdis_sentinel3b_v2',
    key='observations/reanalysis/adt/nesdis/sentinel3b/%Y/%m/24h/iodav2/sentinel3b.nesdis.adt.%Y%m%d.T%H%M%SZ.iodav2.nc',
    start='20160301T000000Z',
    s3_prefix='observations/reanalysis/adt/nesdis/sentinel3b/%Y/%m/24h/iodav2/',
    files='sentinel3b.nesdis.adt.%z.iodav2.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET,
)

adt_nesdis_sentinel3b_v3 = InventoryInfo(
    obs_name='adt_nesdis_sentinel3b_v3',
    key='observations/reanalysis/adt/nesdis/sentinel3b/%Y/%m/24h/iodav3/sentinel3b.nesdis.adt.%Y%m%d.T%H%M%SZ.iodav3.nc',
    start='20160301T000000Z',
    s3_prefix='observations/reanalysis/adt/nesdis/sentinel3b/%Y/%m/24h/iodav3/',
    files='sentinel3b.nesdis.adt.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET,
)

adt_nesdis_topex_poseidon_v2 = InventoryInfo(
    obs_name='adt_nesdis_topex_poseidon_v2',
    key='observations/reanalysis/adt/nesdis/topex_poseidon/%Y/%m/24h/iodav2/topex_poseidon.nesdis.adt.%Y%m%d.T%H%M%SZ.iodav2.nc',
    start='20160301T000000Z',
    s3_prefix='observations/reanalysis/adt/nesdis/topex_poseidon/%Y/%m/24h/iodav2/',
    files='topex_poseidon.nesdis.adt.%z.iodav2.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET,
)

adt_nesdis_topex_poseidon_v3 = InventoryInfo(
    obs_name='adt_nesdis_topex_poseidon_v3',
    key='observations/reanalysis/adt/nesdis/topex_poseidon/%Y/%m/24h/iodav3/topex_poseidon.nesdis.adt.%Y%m%d.T%H%M%SZ.iodav3.nc',
    start='20160301T000000Z',
    s3_prefix='observations/reanalysis/adt/nesdis/topex_poseidon/%Y/%m/24h/iodav3/',
    files='topex_poseidon.nesdis.adt.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET,
)

insitu_ncei_wod_v2 = InventoryInfo(
    obs_name='insitu_ncei_wod_v2',
    key='observations/reanalysis/insitu/ncei/wod/%Y/%m/24h/iodav2/wod.ncei.insitu.%Y%m%d.T%H%M%S.iodav2.nc',
    start='19700101T120000Z',
    s3_prefix='observations/reanalysis/insitu/ncei/wod/%Y/%m/24h/iodav2/',
    files='wod.ncei.insitu.%z.iodav2.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET
)

insitu_ncei_wod_v3 = InventoryInfo(
    obs_name='insitu_ncei_wod_v3',
    key='observations/reanalysis/insitu/ncei/wod/%Y/%m/24h/iodav3/wod.ncei.insitu.%Y%m%d.T%H%M%S.iodav3.nc',
    start='19700101T120000Z',
    s3_prefix='observations/reanalysis/insitu/ncei/wod/%Y/%m/24h/iodav3/',
    files='wod.ncei.insitu.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET
)

sss_jpl_sentinel1a_v2 = InventoryInfo(
    obs_name='sss_jpl_sentinel1a_v2',
    key='observations/reanalysis/sss/jpl/sentinel1a/%Y/%m/24h/iodav2/sss.jpl.smap_l2_sentinel1a.%Y%m%d.T%H%M%S.iodav2.nc',
    start='20150401T120000Z',
    s3_prefix='observations/reanalysis/sss/jpl/sentinel1a/%Y/%m/24h/iodav2/',
    files='sss.jpl.smap_l2_sentinel1a.%z.iodav2.nc',
    inv_cmd=au.HV_IODA_META, 
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET
)

sss_jpl_sentinel1a_v3 = InventoryInfo(
    obs_name='sss_jpl_sentinel1a_v3',
    key='observations/reanalysis/sss/jpl/sentinel1a/%Y/%m/24h/iodav3/sss.jpl.smap_l2_sentinel1a.%Y%m%d.T%H%M%S.iodav3.nc',
    start='20150401T120000Z',
    s3_prefix='observations/reanalysis/sss/jpl/sentinel1a/%Y/%m/24h/iodav3/',
    files='sss.jpl.smap_l2_sentinel1a.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META, 
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_jpl_coriolis_v2 = InventoryInfo(
    obs_name='sst_jpl_coriolis_v2',
    key='observations/reanalysis/sst/jpl/coriolis/%Y/%m/24h/iodav2/sst.jpl.windsat_coriolis.%Y%m%d.T%H%M%SZ.iodav2.nc',
    start='20181111T120000Z',
    s3_prefix='observations/reanalysis/sst/jpl/coriolis/%Y/%m/24h/iodav2',
    files='sst.jpl.windsat_coriolis.%z.iodav2.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_jpl_coriolis_v3 = InventoryInfo(
    obs_name='sst_jpl_coriolis_v3',
    key='observations/reanalysis/sst/jpl/coriolis/%Y/%m/24h/iodav3/sst.jpl.windsat_coriolis.%Y%m%d.T%H%M%SZ.iodav3.nc',
    start='20181111T120000Z',
    s3_prefix='observations/reanalysis/sst/jpl/coriolis/%Y/%m/24h/iodav3',
    files='sst.jpl.windsat_coriolis.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET
)

#Next step is to add all the SST / NESDIS 

ocn_infos = [adt_nesdis_cryosat2_v2, adt_nesdis_cryosat2_v3, adt_nesdis_ers1_v2, adt_nesdis_ers1_v3, adt_nesdis_jason2_v2, adt_nesdis_jason2_v3, adt_nesdis_jason3_v2,
             adt_nesdis_jason3_v3, adt_nesdis_saral_v2, adt_nesdis_saral_v3, adt_nesdis_sentinel3a_v2, adt_nesdis_sentinel3a_v3, adt_nesdis_sentinel3b_v2,
             adt_nesdis_sentinel3b_v3, adt_nesdis_topex_poseidon_v2, adt_nesdis_topex_poseidon_v3, insitu_ncei_wod_v2, insitu_ncei_wod_v3, 
             sss_jpl_sentinel1a_v2, sss_jpl_sentinel1a_v3, sst_jpl_coriolis_v2, sst_jpl_coriolis_v3]