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
    start='20180526T120000Z',
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
    start='20180526T120000Z',
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
    start='19930101T120000Z',
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
    start='19930101T120000Z',
    s3_prefix='observations/reanalysis/adt/nesdis/topex_poseidon/%Y/%m/24h/iodav3/',
    files='topex_poseidon.nesdis.adt.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET,
)

insitu_ncei_wod_v2 = InventoryInfo(
    obs_name='insitu_ncei_wod_v2',
    key='observations/reanalysis/insitu/ncei/wod/%Y/%m/24h/iodav2/wod.ncei.insitu.%Y%m%d.T%H%M%SZ.iodav2.nc',
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
    key='observations/reanalysis/insitu/ncei/wod/%Y/%m/24h/iodav3/wod.ncei.insitu.%Y%m%d.T%H%M%SZ.iodav3.nc',
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
    files='sss.jpl.smap_l2_sentinel1a.%.iodav2.nc',
    inv_cmd=au.HV_IODA_META, 
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_DAILY,
    s3_bucket=au.REANALYSIS_BUCKET
)

sss_jpl_sentinel1a_v3 = InventoryInfo(
    obs_name='sss_jpl_sentinel1a_v3',
    key='observations/reanalysis/sss/jpl/sentinel1a/%Y/%m/24h/iodav3/sss.jpl.smap_l2_sentinel1a.%Y%m%d.T%H%M%SZ.iodav3.nc',
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

sst_nesdis_amsr2_v2 = InventoryInfo(
    obs_name='sst_nesdis_amsr2_v2',
    key='observations/reanalysis/sst/nesdis/amsr2/%Y/%m/24h/iodav2/sst.nesdis.amsr2.%Y%m%d.T%H%M%SZ.iodav2.nc',
    start='20181111T120000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/amsr2/%Y/%m/24h/iodav2/', 
    files='sst.nesdis.amsr2.%z.iodav2.nc',
    inv_cmd=au.HV_IODA_META,
    cycling_interval=au.CYCLING_DAILY,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_amsr2_v3 = InventoryInfo(
    obs_name='sst_nesdis_amsr2_v3',
    key='observations/reanalysis/sst/nesdis/amsr2/%Y/%m/24h/iodav3/sst.nesdis.amsr2.%Y%m%d.T%H%M%SZ.iodav3.nc',
    start='20181111T120000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/amsr2/%Y/%m/24h/iodav3/', 
    files='sst.nesdis.amsr2.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META,
    cycling_interval=au.CYCLING_DAILY,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_gpm_v2 = InventoryInfo(
    obs_name='sst_nesdis_gpm_v2',
    key='observations/reanalysis/sst/nesdis/gpm/%Y/%m/24h/iodav2/sst.nesdis.gmi_gpm.%Y%m%d.T%H%M%SZ.iodav2.nc',
    start='20181111T120000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/gpm/%Y/%m/24h/iodav2/', 
    files='sst.nesdis.gmi_gpm.%z.iodav2.nc',
    inv_cmd=au.HV_IODA_META,
    cycling_interval=au.CYCLING_DAILY,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_gpm_v3 = InventoryInfo(
    obs_name='sst_nesdis_gpm_v3',
    key='observations/reanalysis/sst/nesdis/gpm/%Y/%m/24h/iodav3/sst.nesdis.gmi_gpm.%Y%m%d.T%H%M%SZ.iodav3.nc',
    start='20181111T120000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/gpm/%Y/%m/24h/iodav3/', 
    files='sst.nesdis.gmi_gpm.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META,
    cycling_interval=au.CYCLING_DAILY,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_metopa_v2 = InventoryInfo(
    obs_name='sst_nesdis_metopa_v2',
    key='observations/reanalysis/sst/nesdis/metopa/%Y/%m/24h/iodav2/sst.nesdis.avhrr_l3u_metopa.%Y%m%d.T%H%M%SZ.iodav2.nc',
    start='20061215T120000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/metopa/%Y/%m/24h/iodav2/', 
    files='sst.nesdis.avhrr_l3u_metopa.%z.iodav2.nc',
    inv_cmd=au.HV_IODA_META,
    cycling_interval=au.CYCLING_DAILY,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_metopa_v3 = InventoryInfo(
    obs_name='sst_nesdis_metopa_v3',
    key='observations/reanalysis/sst/nesdis/metopa/%Y/%m/24h/iodav3/sst.nesdis.avhrr_l3u_metopa.%Y%m%d.T%H%M%SZ.iodav3.nc',
    start='20061215T120000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/metopa/%Y/%m/24h/iodav3/', 
    files='sst.nesdis.avhrr_l3u_metopa.%z.iodav3.nc',
    inv_cmd=au.HV_IODA_META,
    cycling_interval=au.CYCLING_DAILY,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_noaa07_v2 = InventoryInfo(
    obs_name='sst_nesdis_noaa07_v2',
    key='observations/reanalysis/sst/nesdis/noaa07/%Y/%m/1h/superob_0p25/iodav2/nesdis.avhrr_noaa07.sst.%Y%m%d.T%H%M%SZ.iodav2.so0p25.nc',
    start='19810901T000000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/noaa07/%Y/%m/1h/superob_0p25/iodav2/',
    files='nesdis.avhrr_noaa07.sst.%z.iodav2.so0p25.nc',
    cycling_interval=au.CYCLING_HOURLY,
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_noaa07_v3 = InventoryInfo(
    obs_name='sst_nesdis_noaa07_v3',
    key='observations/reanalysis/sst/nesdis/noaa07/%Y/%m/1h/superob_0p25/iodav3/nesdis.avhrr_noaa07.sst.%Y%m%d.T%H%M%SZ.iodav3.so0p25.nc',
    start='19810901T000000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/noaa07/%Y/%m/1h/superob_0p25/iodav3/',
    files='nesdis.avhrr_noaa07.sst.%z.iodav3.so0p25.nc',
    cycling_interval=au.CYCLING_HOURLY,
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_noaa09_v2 = InventoryInfo(
    obs_name='sst_nesdis_noaa09_v2',
    key='observations/reanalysis/sst/nesdis/noaa09/%Y/%m/1h/superob_0p25/iodav2/nesdis.avhrr_noaa09.sst.%Y%m%d.T%H%M%SZ.iodav2.so0p25.nc',
    start='19850131T000000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/noaa09/%Y/%m/1h/superob_0p25/iodav2/',
    files='nesdis.avhrr_noaa09.sst.%z.iodav2.so0p25.nc',
    cycling_interval=au.CYCLING_HOURLY,
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_noaa09_v3 = InventoryInfo(
    obs_name='sst_nesdis_noaa09_v3',
    key='observations/reanalysis/sst/nesdis/noaa09/%Y/%m/1h/superob_0p25/iodav3/nesdis.avhrr_noaa09.sst.%Y%m%d.T%H%M%SZ.iodav3.so0p25.nc',
    start='19850131T000000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/noaa09/%Y/%m/1h/superob_0p25/iodav3/',
    files='nesdis.avhrr_noaa09.sst.%z.iodav3.so0p25.nc',
    cycling_interval=au.CYCLING_HOURLY,
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_noaa11_v2 = InventoryInfo(
    obs_name='sst_nesdis_noaa11_v2',
    key='observations/reanalysis/sst/nesdis/noaa11/%Y/%m/1h/superob_0p25/iodav2/nesdis.avhrr_noaa11.sst.%Y%m%d.T%H%M%SZ.iodav2.so0p25.nc',
    start='19881108T000000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/noaa11/%Y/%m/1h/superob_0p25/iodav2/',
    files='nesdis.avhrr_noaa11.sst.%z.iodav2.so0p25.nc',
    cycling_interval=au.CYCLING_HOURLY,
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_noaa11_v3 = InventoryInfo(
    obs_name='sst_nesdis_noaa11_v3',
    key='observations/reanalysis/sst/nesdis/noaa11/%Y/%m/1h/superob_0p25/iodav3/nesdis.avhrr_noaa11.sst.%Y%m%d.T%H%M%SZ.iodav3.so0p25.nc',
    start='19881108T000000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/noaa11/%Y/%m/1h/superob_0p25/iodav3/',
    files='nesdis.avhrr_noaa11.sst.%z.iodav3.so0p25.nc',
    cycling_interval=au.CYCLING_HOURLY,
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_noaa12_v2 = InventoryInfo(
    obs_name='sst_nesdis_noaa12_v2',
    key='observations/reanalysis/sst/nesdis/noaa12/%Y/%m/1h/superob_0p25/iodav2/nesdis.avhrr_noaa12.sst.%Y%m%d.T%H%M%SZ.iodav2.so0p25.nc',
    start='19910916T000000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/noaa12/%Y/%m/1h/superob_0p25/iodav2/',
    files='nesdis.avhrr_noaa12.sst.%z.iodav2.so0p25.nc',
    cycling_interval=au.CYCLING_HOURLY,
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_noaa12_v3 = InventoryInfo(
    obs_name='sst_nesdis_noaa12_v3',
    key='observations/reanalysis/sst/nesdis/noaa12/%Y/%m/1h/superob_0p25/iodav3/nesdis.avhrr_noaa12.sst.%Y%m%d.T%H%M%SZ.iodav3.so0p25.nc',
    start='19910916T000000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/noaa12/%Y/%m/1h/superob_0p25/iodav3/',
    files='nesdis.avhrr_noaa12.sst.%z.iodav3.so0p25.nc',
    cycling_interval=au.CYCLING_HOURLY,
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_noaa14_v2 = InventoryInfo(
    obs_name='sst_nesdis_noaa14_v2',
    key='observations/reanalysis/sst/nesdis/noaa14/%Y/%m/1h/superob_0p25/iodav2/nesdis.avhrr_noaa14.sst.%Y%m%d.T%H%M%SZ.iodav2.so0p25.nc',
    start='19950119T180000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/noaa14/%Y/%m/1h/superob_0p25/iodav2/',
    files='nesdis.avhrr_noaa14.sst.%z.iodav2.so0p25.nc',
    cycling_interval=au.CYCLING_HOURLY,
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_noaa14_v3 = InventoryInfo(
    obs_name='sst_nesdis_noaa14_v3',
    key='observations/reanalysis/sst/nesdis/noaa14/%Y/%m/1h/superob_0p25/iodav3/nesdis.avhrr_noaa14.sst.%Y%m%d.T%H%M%SZ.iodav3.so0p25.nc',
    start='19950119T180000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/noaa14/%Y/%m/1h/superob_0p25/iodav3/',
    files='nesdis.avhrr_noaa14.sst.%z.iodav3.so0p25.nc',
    cycling_interval=au.CYCLING_HOURLY,
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_noaa15_v2 = InventoryInfo(
    obs_name='sst_nesdis_noaa15_v2',
    key='observations/reanalysis/sst/nesdis/noaa15/%Y/%m/1h/superob_0p25/iodav2/nesdis.avhrr_noaa15.sst.%Y%m%d.T%H%M%SZ.iodav2.so0p25.nc',
    start='19981101T000000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/noaa15/%Y/%m/1h/superob_0p25/iodav2/',
    files='nesdis.avhrr_noaa15.sst.%z.iodav2.so0p25.nc',
    cycling_interval=au.CYCLING_HOURLY,
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_noaa15_v3 = InventoryInfo(
    obs_name='sst_nesdis_noaa15_v3',
    key='observations/reanalysis/sst/nesdis/noaa15/%Y/%m/1h/superob_0p25/iodav3/nesdis.avhrr_noaa15.sst.%Y%m%d.T%H%M%SZ.iodav3.so0p25.nc',
    start='19981101T000000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/noaa15/%Y/%m/1h/superob_0p25/iodav3/',
    files='nesdis.avhrr_noaa15.sst.%z.iodav3.so0p25.nc',
    cycling_interval=au.CYCLING_HOURLY,
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_noaa16_v2 = InventoryInfo(
    obs_name='sst_nesdis_noaa16_v2',
    key='observations/reanalysis/sst/nesdis/noaa16/%Y/%m/1h/superob_0p25/iodav2/nesdis.avhrr_noaa16.sst.%Y%m%d.T%H%M%SZ.iodav2.so0p25.nc',
    start='20001026T000000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/noaa16/%Y/%m/1h/superob_0p25/iodav2/',
    files='nesdis.avhrr_noaa16.sst.%z.iodav2.so0p25.nc',
    cycling_interval=au.CYCLING_HOURLY,
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_noaa16_v3 = InventoryInfo(
    obs_name='sst_nesdis_noaa16_v3',
    key='observations/reanalysis/sst/nesdis/noaa16/%Y/%m/1h/superob_0p25/iodav3/nesdis.avhrr_noaa16.sst.%Y%m%d.T%H%M%SZ.iodav3.so0p25.nc',
    start='20001026T000000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/noaa16/%Y/%m/1h/superob_0p25/iodav3/',
    files='nesdis.avhrr_noaa16.sst.%z.iodav3.so0p25.nc',
    cycling_interval=au.CYCLING_HOURLY,
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_noaa19_v2 = InventoryInfo(
    obs_name='sst_nesdis_noaa19_v2',
    key='observations/reanalysis/sst/nesdis/noaa19/%Y/%m/24h/iodav2/sst.nesdis.avhrr_l3u_noaa19.%Y%m%d.T%H%M%SZ.iodav2.nc',
    start='20090222T120000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/noaa19/%Y/%m/24h/iodav2/',
    files='sst.nesdis.avhrr_l3u_noaa19.%z.iodav2.nc',
    cycling_interval=au.CYCLING_DAILY,
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

sst_nesdis_noaa19_v3 = InventoryInfo(
    obs_name='sst_nesdis_noaa19_v3',
    key='observations/reanalysis/sst/nesdis/noaa19/%Y/%m/24h/iodav3/sst.nesdis.avhrr_l3u_noaa19.%Y%m%d.T%H%M%SZ.iodav3.nc',
    start='20090222T120000Z',
    s3_prefix='observations/reanalysis/sst/nesdis/noaa19/%Y/%m/24h/iodav3/',
    files='sst.nesdis.avhrr_l3u_noaa19.%z.iodav3.nc',
    cycling_interval=au.CYCLING_DAILY,
    inv_cmd=au.HV_IODA_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

insitu_wod_apb = InventoryInfo(
    obs_name='insitu_wod_apb',
    key='observations/reanalysis/insitu/wod/apb/%Y/%m/wod_apb_%Y-%m-%dT%H.nc',
    start='19980206T000000Z',
    s3_prefix='observations/reanalysis/insitu/wod/apb/%Y/%m/',
    files='wod_apb_%Y-%m-%dT%H.nc',
    cycling_interval=au.CYCLING_6H,
    inv_cmd=au.HV_WOD_NC_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

insitu_wod_ctd = InventoryInfo(
    obs_name='insitu_wod_ctd',
    key='observations/reanalysis/insitu/wod/ctd/%Y/%m/wod_ctd_%Y-%m-%dT%H.nc',
    start='19700102T180000Z',
    s3_prefix='observations/reanalysis/insitu/wod/ctd/%Y/%m/',
    files='wod_ctd_%Y-%m-%dT%H.nc',
    cycling_interval=au.CYCLING_6H,
    inv_cmd=au.HV_WOD_NC_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

insitu_wod_drb = InventoryInfo(
    obs_name='insitu_wod_drb',
    key='observations/reanalysis/insitu/wod/drb/%Y/%m/wod_drb_%Y-%m-%dT%H.nc',
    start='19860403T000000Z',
    s3_prefix='observations/reanalysis/insitu/wod/drb/%Y/%m/',
    files='wod_drb_%Y-%m-%dT%H.nc',
    cycling_interval=au.CYCLING_6H,
    inv_cmd=au.HV_WOD_NC_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

insitu_wod_gld = InventoryInfo(
    obs_name='insitu_wod_gld',
    key='observations/reanalysis/insitu/wod/gld/%Y/%m/wod_gld_%Y-%m-%dT%H.nc',
    start='20000415T180000Z',
    s3_prefix='observations/reanalysis/insitu/wod/gld/%Y/%m/',
    files='wod_gld_%Y-%m-%dT%H.nc',
    cycling_interval=au.CYCLING_6H,
    inv_cmd=au.HV_WOD_NC_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

insitu_wod_mbt = InventoryInfo(
    obs_name='insitu_wod_mbt',
    key='observations/reanalysis/insitu/wod/mbt/%Y/%m/wod_mbt_%Y-%m-%dT%H.nc',
    start='19700101T000000Z',
    s3_prefix='observations/reanalysis/insitu/wod/mbt/%Y/%m/',
    files='wod_mbt_%Y-%m-%dT%H.nc',
    cycling_interval=au.CYCLING_6H,
    inv_cmd=au.HV_WOD_NC_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

insitu_wod_mrb = InventoryInfo(
    obs_name='insitu_wod_mrb',
    key='observations/reanalysis/insitu/wod/mrb/%Y/%m/wod_mrb_%Y-%m-%dT%H.nc',
    start='19780101T000000Z',
    s3_prefix='observations/reanalysis/insitu/wod/mrb/%Y/%m/',
    files='wod_mrb_%Y-%m-%dT%H.nc',
    cycling_interval=au.CYCLING_6H,
    inv_cmd=au.HV_WOD_NC_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

insitu_wod_osd = InventoryInfo(
    obs_name='insitu_wod_osd',
    key='observations/reanalysis/insitu/wod/osd/%Y/%m/wod_osd_%Y-%m-%dT%H.nc',
    start='19730101T000000Z',
    s3_prefix='observations/reanalysis/insitu/wod/osd/%Y/%m/',
    files='wod_osd_%Y-%m-%dT%H.nc',
    cycling_interval=au.CYCLING_6H,
    inv_cmd=au.HV_WOD_NC_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

insitu_wod_pfl = InventoryInfo(
    obs_name='insitu_wod_pfl',
    key='observations/reanalysis/insitu/wod/pfl/%Y/%m/wod_pfl_%Y-%m-%dT%H.nc',
    start='19940706T060000Z',
    s3_prefix='observations/reanalysis/insitu/wod/pfl/%Y/%m/',
    files='wod_pfl_%Y-%m-%dT%H.nc',
    cycling_interval=au.CYCLING_6H,
    inv_cmd=au.HV_WOD_NC_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

insitu_wod_uor = InventoryInfo(
    obs_name='insitu_wod_uor',
    key='observations/reanalysis/insitu/wod/uor/%Y/%m/wod_uor_%Y-%m-%dT%H.nc',
    start='19860513T000000Z',
    s3_prefix='observations/reanalysis/insitu/wod/uor/%Y/%m/',
    files='wod_uor_%Y-%m-%dT%H.nc',
    cycling_interval=au.CYCLING_6H,
    inv_cmd=au.HV_WOD_NC_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

insitu_wod_xbt = InventoryInfo(
    obs_name='insitu_wod_xbt',
    key='observations/reanalysis/insitu/wod/xbt/%Y/%m/wod_xbt_%Y-%m-%dT%H.nc',
    start='19860513T000000Z',
    s3_prefix='observations/reanalysis/insitu/wod/xbt/%Y/%m/',
    files='wod_xbt_%Y-%m-%dT%H.nc',
    cycling_interval=au.CYCLING_6H,
    inv_cmd=au.HV_WOD_NC_META,
    platform=au.CLEAN_PLATFORM,
    s3_bucket=au.REANALYSIS_BUCKET
)

ocn_infos = [adt_nesdis_cryosat2_v2, adt_nesdis_cryosat2_v3, adt_nesdis_ers1_v2, adt_nesdis_ers1_v3, adt_nesdis_jason2_v2, adt_nesdis_jason2_v3, adt_nesdis_jason3_v2,
             adt_nesdis_jason3_v3, adt_nesdis_saral_v2, adt_nesdis_saral_v3, adt_nesdis_sentinel3a_v2, adt_nesdis_sentinel3a_v3, adt_nesdis_sentinel3b_v2,
             adt_nesdis_sentinel3b_v3, adt_nesdis_topex_poseidon_v2, adt_nesdis_topex_poseidon_v3, insitu_ncei_wod_v2, insitu_ncei_wod_v3, 
             sss_jpl_sentinel1a_v2, sss_jpl_sentinel1a_v3, sst_jpl_coriolis_v2, sst_jpl_coriolis_v3, sst_nesdis_amsr2_v2, sst_nesdis_amsr2_v3,
             sst_nesdis_gpm_v2, sst_nesdis_gpm_v3, sst_nesdis_metopa_v2, sst_nesdis_metopa_v3, sst_nesdis_noaa07_v2, sst_nesdis_noaa07_v3, 
             sst_nesdis_noaa09_v2, sst_nesdis_noaa09_v3, sst_nesdis_noaa11_v2, sst_nesdis_noaa11_v3, sst_nesdis_noaa12_v2, sst_nesdis_noaa12_v3, 
             sst_nesdis_noaa14_v2, sst_nesdis_noaa14_v3, sst_nesdis_noaa15_v2, sst_nesdis_noaa15_v3, sst_nesdis_noaa16_v2, sst_nesdis_noaa16_v3,
             sst_nesdis_noaa19_v2, sst_nesdis_noaa19_v3, insitu_wod_apb, insitu_wod_ctd, insitu_wod_drb, insitu_wod_gld, insitu_wod_mbt, insitu_wod_mrb,
             insitu_wod_osd, insitu_wod_pfl, insitu_wod_uor, insitu_wod_xbt]