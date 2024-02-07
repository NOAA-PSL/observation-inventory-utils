'''
Stored information necessary for inventory of clean bucket atmosphere variables

NOTE: START DATES NEED TO BE UPDATED TO REFLECT BACK FILLING FROM SHERRIES WORK
'''
import automation_utils as au
from automation_utils import InventoryInfo


airs_airsev = InventoryInfo(
    obs_name='airs_airsev',
    key='observations/reanalysis/airs/airsev/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.airsev.tm00.bufr_d',
    start='20070201T000000Z',
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
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
    cycling_interval=au.CYCLING_6H,
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
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
    s3_prefix='observations/reanalysis/amsua/1bamua/%Y/%m/bufr/',
    bufr_files='gdas.%z.1bamua.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV
)

amsua_nasa_aqua = InventoryInfo(
    obs_name='amsua_nasa_aqua',
    key='observations/reanalysis/amsua/nasa/aqua/%Y/%m/bufr/amsua_disc_final.%Y%m%d.t%Hz.bufr',
    start='20020901T000000Z',
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
    s3_prefix='observations/reanalysis/amsua/nasa/aqua/%Y/%m/bufr/',
    bufr_files='amsua_disc_final.%z.bufr',
    nceplibs_cmd=au.NCEPLIBS_SINV
)

amsua_nasa_r21c = InventoryInfo(
    obs_name='amsua_nasa_r21c',
    key='observations/reanalysis/amsua/nasa/r21c_repo/%Y/%m/bufr/gmao_r21c_repro.%Y%m%d.t%Hz.1bamu.tm00.bufr',
    start='19981026T000000Z',
    s3_prefix='observations/reanalysis/amsua/nasa/r21c_repro/%Y/%m/bufr/',
    bufr_files='gmao_r21c_repro.%z.1bamu.tm00.bufr',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

amsub_1bamub = InventoryInfo(
    obs_name='amsub_1bamub',
    key='observations/reanalysis/amsub/1bamub/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.1bamub.tm00.bufr_d',
    start='19981026T000000Z',
    s3_prefix='observations/reanalysis/amsub/1bamub/%Y/%m/bufr/',
    bufr_files='gdas.%z.1bamub.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

amv_merged = InventoryInfo(
    obs_name='amv_merged',
    key='observations/reanalysis/amv/merged/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.satwnd.tm00.bufr_d',
    start='19790101T000000Z',
    s3_prefix='observations/reanalysis/amv/merged/%Y/%m/bufr/',
    bufr_files='gdas.%z.satwnd.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

amv_satwnd = InventoryInfo(
    obs_name='amv_satwnd',
    key='observations/reanalysis/amv/satwnd/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.satwnd.tm00.bufr_d',
    start='19900101T000000Z',
    s3_prefix='observations/reanalysis/amv/satwnd/%Y/%m/bufr/',
    bufr_files='gdas.%z.satwnd.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

atms_atms = InventoryInfo(
    obs_name='atms_atms',
    key='observations/reanalysis/atms/atms/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.atms.tm00.bufr_d',
    start='20120101T000000Z',
    s3_prefix='observations/reanalysis/atms/atms/%Y/%m/bufr/',
    bufr_files='gdas.%z.atms.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

avhrr_avcsam = InventoryInfo(
    obs_name='avhrr_avcsam',
    key='observations/reanalysis/avhrr/nasa/21cr_repro/avcsam/%Y/%m/bufr/gmao.%Y%m%d.t%Hz.avcsam.tm00.bufr_d',
    start='19981026T000000Z',
    s3_prefix='observations/reanalysis/avhrr/nasa/21cr_repro/avcsam/%Y/%m/bufr/',
    bufr_files='gmao.%z.avcsam.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

avhrr_avcspm = InventoryInfo(
    obs_name='avhrr_avcspm',
    key='observations/reanalysis/avhrr/nasa/21cr_repro/avcspm/%Y/%m/bufr/gmao.%Y%m%d.t%Hz.avcspm.tm00.bufr_d',
    start='20010301T000000Z',
    s3_prefix='observations/reanalysis/avhrr/nasa/21cr_repro/avcspm/%Y/%m/bufr/',
    bufr_files='gmao.%z.avcspm.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

conv_prepbufr_acft_profiles = InventoryInfo(
    obs_name='conv_prepbufr_acft_profiles',
    key='observations/reanalysis/conv/prepbufr.acft_profiles/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.prepbufr.acft_profiles.nr',
    start='19790101T000000Z',
    s3_prefix='observations/reanalysis/conv/prepbufr.acft_profiles/%Y/%m/bufr/',
    bufr_files='gdas.%z.prepbufr.acft_profiles.nr',
    nceplibs_cmd=au.NCEPLIBS_CMPBQM,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

conv_prepbufr = InventoryInfo(
    obs_name='conv_prepbufr',
    key='observations/reanalysis/conv/prepbufr/%Y/%m/prepbufr/gdas.%Y%m%d.t%Hz.prepbufr.nr',
    start='19790101T000000Z',
    s3_prefix='observations/reanalysis/conv/prepbufr/%Y/%m/prepbufr/',
    bufr_files='gdas.%z.prepbufr.nr',
    nceplibs_cmd=au.NCEPLIBS_CMPBQM,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

cris_cris = InventoryInfo(
    obs_name='cris_cris',
    key='observations/reanalysis/cris/cris/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.cris.tm00.bufr_d',
    start='20121001T000000Z',
    s3_prefix='observations/reanalysis/cris/cris/%Y/%m/bufr/',
    bufr_files='gdas.%z.cris.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

cris_crisf4 = InventoryInfo(
    obs_name='cris_crisf4',
    key='observations/reanalysis/cris/crisf4/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.crisf4.tm00.bufr_d',
    start='20180101T000000Z',
    s3_prefix='observations/reanalysis/cris/crisf4/%Y/%m/bufr/',
    bufr_files='gdas.%z.crisf4.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

geo_geoimr = InventoryInfo(
    obs_name='geo_geoimr',
    key='observations/reanalysis/geo/geoimr/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.geoimr.tm00.bufr_d',
    start='20020101T000000Z',
    s3_prefix='observations/reanalysis/geo/geoimr/%Y/%m/bufr/',
    bufr_files='gdas.%z.geoimr.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

geo_goesfv = InventoryInfo(
    obs_name='geo_goesfv',
    key='observations/reanalysis/geo/goesfv/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.goesfv.tm00.bufr_d',
    start='20070201T000000Z',
    s3_prefix='observations/reanalysis/geo/goesfv/%Y/%m/bufr/',
    bufr_files='gdas.%z.goesfv.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

geo_goesnd = InventoryInfo(
    obs_name='geo_goesnd',
    key='observations/reanalysis/geo/goesnd/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.goesnd.tm00.bufr_d',
    start='19970901T000000Z',
    s3_prefix='observations/reanalysis/geo/goesnd/%Y/%m/bufr/',
    bufr_files='gdas.%z.goesnd.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

geo_gsrasr = InventoryInfo(
    obs_name='geo_gsrasr',
    key='observations/reanalysis/geo/gsrasr/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.gsrasr.tm00.bufr_d',
    start='20210322T120000Z',
    s3_prefix='observations/reanalysis/geo/gsrasr/%Y/%m/bufr/',
    bufr_files='gdas.%z.gsrasr.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

geo_gsrcsr = InventoryInfo(
    obs_name='geo_gsrcsr',
    key='observations/reanalysis/geo/gsrcsr/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.gsrcsr.tm00.bufr_d',
    start='20210322T120000Z',
    s3_prefix='observations/reanalysis/geo/gsrcsr/%Y/%m/bufr/',
    bufr_files='gdas.%z.gsrcsr.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

gmi_nasa_gmiv7 = InventoryInfo(
    obs_name='gmi_nasa_gmiv7',
    key='observations/reanalysis/gmi/nasa/gmi_v7/%Y/%m/bufr/gmi_v7_L1CR.%Y%m%d.t%Hz.bufr',
    start='20140305T000000Z',
    s3_prefix='observations/reanalysis/gmi/nasa/gmi_v7/%Y/%m/bufr/',
    bufr_files='gmi_v7_L1CR.%z.bufr',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

gps_eumetsat = InventoryInfo(
    obs_name='gps_eumetsat',
    key='observations/reanalysis/gps/eumetsat/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.gpsro.tm00.bufr_d',
    start='20010901T000000Z',
    s3_prefix='observations/reanalysis/gps/eumetsat/%Y/%m/bufr/',
    bufr_files='gdas.%z.gpsro.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

gps_gpsro = InventoryInfo(
    obs_name='gps_gpsro',
    key='observations/reanalysis/gps/gpsro/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.gpsro.tm00.bufr_d',
    start='20010501T000000Z',
    s3_prefix='observations/reanalysis/gps/gpsro/%Y/%m/bufr/',
    bufr_files='gdas.%z.gpsro.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

hirs_1bhrs2 = InventoryInfo(
    obs_name='hirs_1bhrs2',
    key='observations/reanalysis/hirs/1bhrs2/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.1bhrs2.tm00.bufr_d', 
    start='19790101T000000Z', 
    s3_prefix='observations/reanalysis/hirs/1bhrs2/%Y/%m/bufr/',
    bufr_files='gdas.%z.1bhrs2.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,   
)

hirs_1bhrs3 = InventoryInfo(
    obs_name='hirs_1bhrs3',
    key='observations/reanalysis/hirs/1bhrs3/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.1bhrs3.tm00.bufr_d',
    start='19981026T000000Z',
    s3_prefix='observations/reanalysis/hirs/1bhrs3/%Y/%m/bufr/',
    bufr_files='gdas.%z.1bhrs3.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,  
)

hirs_1bhrs4 = InventoryInfo(
    obs_name='hirs_1bhrs4',
    key='observations/reanalysis/hirs/1bhrs4/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.1bhrs4.tm00.bufr_d',
    start='20020101T000000Z',
    s3_prefix='observations/reanalysis/hirs/1bhrs4/%Y/%m/bufr/',
    bufr_files='gdas.%z.1bhrs4.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

iasi_mtiasi = InventoryInfo(
    obs_name='iasi_mtiasi',
    key='observations/reanalysis/iasi/mtiasi/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.mtiasi.tm00.bufr_d',
    start='20080101T000000Z',
    s3_prefix='observations/reanalysis/iasi/mtiasi/%Y/%m/bufr/',
    bufr_files='gdas.%z.mtiasi.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

mhs_1bmhs = InventoryInfo(
    obs_name='mhs_1bmhs',
    key='observations/reanalysis/mhs/1bmhs/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.1bmhs.tm00.bufr_d',
    start='20021001T000000Z',
    s3_prefix='observations/reanalysis/mhs/1bmhs/%Y/%m/bufr/',
    bufr_files='gdas.%z.1bmhs.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

msu_1bmsu = InventoryInfo(
    obs_name='msu_1bmsu',
    key='observations/reanalysis/msu/1bmsu/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.1bmsu.tm00.bufr_d',
    start='19790101T000000Z',
    s3_prefix='observations/reanalysis/msu/1bmsu/%Y/%m/bufr/',
    bufr_files='gdas.%z.1bmsu.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

ozone_cfsr = InventoryInfo(
    obs_name='ozone_cfsr',
    key='observations/reanalysis/ozone/cfsr/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.osbuv8.tm00.bufr_d',
    start='19790101T000000Z',
    s3_prefix='observations/reanalysis/ozone/cfsr/%Y/%m/bufr/',
    bufr_files='gdas.%z.osbuv8.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

ozone_nasa_sbuv_v87 = InventoryInfo(
    obs_name='ozone_nasa_sbuv_v87',
    key='observations/reanalysis/ozone/nasa/sbuv_v87/%Y/%m/bufr/sbuv_v87.%Y%m%d.t%Hz.bufr',
    start='19991015T000000Z',
    s3_prefix='observations/reanalysis/ozone/nasa/sbuv_v87/%Y/%m/bufr/', 
    bufr_files='sbuv_v87.%z.bufr',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

ozone_ncep_gome = InventoryInfo(
    obs_name='ozone_ncep_gome',
    key='observations/reanalysis/ozone/ncep/gome/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.gome.tm00.bufr_d',
    start='20090101T000000Z',
    s3_prefix='observations/reanalysis/ozone/ncep/gome/%Y/%m/bufr/',
    bufr_files='gdas.%z.gome.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

ozone_ncep_omi = InventoryInfo(
    obs_name='ozone_ncep_omi',
    key='observations/reanalysis/ozone/ncep/omi/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.omi.tm00.bufr_d',
    start='20100101T000000Z',
    s3_prefix='observations/reanalysis/ozone/ncep/omi/%Y/%m/bufr/',
    bufr_files='gdas.%z.omi.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

ozone_ncep_ompslp = InventoryInfo(
    obs_name='ozone_ncep_ompslp',
    key='observations/reanalysis/ozone/ncep/ompslp/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.ompslp.tm00.bufr_d',
    start='20210322T120000Z',
    s3_prefix='observations/reanalysis/ozone/ncep/ompslp/%Y/%m/bufr/',
    bufr_files='gdas.%z.ompslp.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

ozone_ncep_ompsn8 = InventoryInfo(
    obs_name='ozone_ncep_ompsn8',
    key='observations/reanalysis/ozone/ncep/ompsn8/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.ompsn8.tm00.bufr_d',
    start='20210101T000000Z',
    s3_prefix='observations/reanalysis/ozone/ncep/ompsn8/%Y/%m/bufr/',
    bufr_files='gdas.%z.ompsn8.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

ozone_ncep_ompst8 = InventoryInfo(
    obs_name='ozone_ncep_ompst8',
    key='observations/reanalysis/ozone/ncep/ompst8/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.ompst8.tm00.bufr_d',
    start='20210101T000000Z',
    s3_prefix='observations/reanalysis/ozone/ncep/ompst8/%Y/%m/bufr/',
    bufr_files='gdas.%z.ompst8.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

saphir_saphir = InventoryInfo(
    obs_name='saphir_saphir',
    key='observations/reanalysis/saphir/saphir/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.saphir.tm00.bufr_d',
    start='20170201T000000Z', 
    s3_prefix='observations/reanalysis/saphir/saphir/%Y/%m/bufr/',
    bufr_files='gdas.%z.saphir.tm00.bufr_d', 
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

seviri_sevcsr = InventoryInfo(
    obs_name='seviri_sevcsr',
    key='observations/reanalysis/seviri/sevcsr/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.sevcsr.tm00.bufr_d',
    start='20100512T000000Z',
    s3_prefix='observations/reanalysis/seviri/sevcsr/%Y/%m/bufr/',
    bufr_files='gdas.%z.sevcsr.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

ssmi_eumetsat = InventoryInfo(
    obs_name='ssmi_eumetsat',
    key='observations/reanalysis/ssmi/eumetsat/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.ssmit.tm00.bufr_d',
    start='19870109T120000Z',
    s3_prefix='observations/reanalysis/ssmi/eumetsat/%Y/%m/bufr/',
    bufr_files='gdas.%z.ssmit.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

ssmi_ssmit = InventoryInfo(
    obs_name='ssmi_ssmit',
    key='observations/reanalysis/ssmi/ssmit/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.ssmit.tm00.bufr_d',
    start='20000316T120000Z',
    s3_prefix='observations/reanalysis/ssmi/ssmit/%Y/%m/bufr/',
    bufr_files='gdas.%z.ssmit.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

ssmis_eumetsat = InventoryInfo(
    obs_name='ssmis_eumetsat',
    key='observations/reanalysis/ssmis/eumetsat/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.ssmisu.tm00.bufr_d',
    start='20051101T000000Z',
    s3_prefix='observations/reanalysis/ssmis/eumetsat/%Y/%m/bufr/',
    bufr_files='gdas.%z.ssmisu.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

ssmis_ssmisu = InventoryInfo(
    obs_name='ssmis_ssmisu',
    key='observations/reanalysis/ssmis/ssmisu/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.ssmisu.tm00.bufr_d',
    start='20091001T000000Z',
    s3_prefix='observations/reanalysis/ssmis/ssmisu/%Y/%m/bufr/',
    bufr_files='gdas.%z.ssmisu.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

ssu_1bssu = InventoryInfo(
    obs_name='ssu_1bssu', 
    key='observations/reanalysis/ssu/1bssu/%Y/%m/bufr/gdas.%Y%m%d.t%Hz.1bssu.tm00.bufr_d',
    start='19790101T000000Z',
    s3_prefix='observations/reanalysis/ssu/1bssu/%Y/%m/bufr/',
    bufr_files='gdas.%z.1bssu.tm00.bufr_d',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)

trmm_nasa_tmi = InventoryInfo(
    obs_name='trmm_nasa_tmi',
    key='observations/reanalysis/trmm/nasa/tmi/%Y/%m/bufr/tmi.V05A.%Y%m%d.t%Hz.bufr',
    start='19980101T000000Z',
    s3_prefix='observations/reanalysis/trmm/nasa/tmi/%Y/%m/bufr/',
    bufr_files='tmi.V05A.%z.bufr',
    nceplibs_cmd=au.NCEPLIBS_SINV,
    platform=au.CLEAN_PLATFORM,
    cycling_interval=au.CYCLING_6H,
    s3_bucket=au.REANALYSIS_BUCKET,
)


#38 items
atm_infos = [airs_airsev, airs_aqua, amsua_1bamua, amsua_nasa_aqua, amsua_nasa_r21c, amsub_1bamub, amv_merged, amv_satwnd, atms_atms,
             avhrr_avcsam, avhrr_avcspm, conv_prepbufr_acft_profiles, conv_prepbufr, cris_cris, cris_crisf4, geo_geoimr,
             geo_goesfv, geo_goesnd, geo_gsrasr, geo_gsrcsr, gmi_nasa_gmiv7, gps_eumetsat, gps_gpsro, hirs_1bhrs2, hirs_1bhrs3, hirs_1bhrs4,
             iasi_mtiasi, mhs_1bmhs, msu_1bmsu, ozone_nasa_sbuv_v87, saphir_saphir, seviri_sevcsr, ssmi_eumetsat,
             ssmi_ssmit, ssmis_eumetsat, ssmis_ssmisu, ssu_1bssu, trmm_nasa_tmi]