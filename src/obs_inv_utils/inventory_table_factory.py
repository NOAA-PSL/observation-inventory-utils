import sqlalchemy as db
from datetime import datetime
from obs_inv_utils import search_engine as se
from sqlalchemy import Table, Column, MetaData
from sqlalchemy import Integer, String, Boolean, DateTime, Float
from sqlalchemy import inspect
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

OBS_SQLITE_DATABASE = 'sqlite:///observations_inventory.db'
OBS_INVENTORY_TABLE = 'obs_inventory'
HPSS_CMD_RESULTS_TABLE = 'hpss_cmd_results'

engine = db.create_engine(OBS_SQLITE_DATABASE, echo = True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


def create_obs_inventory_table():
    insp = inspect(engine)
    table_exists = insp.has_table(OBS_INVENTORY_TABLE)
    print(f'obs_inventory table exists: {table_exists}')
    if not insp.has_table(OBS_INVENTORY_TABLE):
        metadata = MetaData(engine)

        Table(OBS_INVENTORY_TABLE, metadata, 
            Column('obs_id', Integer, primary_key = True), 
            Column('filename', String), 
            Column('parent_dir', String),
            Column('platform', String),
            Column('s3_bucket', String),
            Column('prefix', String),
            Column('cycle_tag', String),
            Column('data_type', String),
            Column('cycle_time', Integer),
            Column('obs_day', DateTime),
            Column('data_format', String),
            Column('suffix', String),
            Column('nr_tag', Boolean),
            Column('file_size', Integer),
            Column('permissions', String),
            Column('last_modified', DateTime),
            Column('inserted_at', DateTime),
        )

        metadata.create_all(engine)


def create_hpss_cmd_results_table():
    insp = inspect(engine)
    table_exists = insp.has_table(HPSS_CMD_RESULTS_TABLE)
    print(f'hpss_cmd_results table exists: {table_exists}')
    if not insp.has_table(HPSS_CMD_RESULTS_TABLE):
        metadata = MetaData(engine)

        Table(HPSS_CMD_RESULTS_TABLE, metadata,
            Column('cmd_result_id', Integer, primary_key = True),
            Column('command', String),
            Column('arg0', String),
            Column('raw_output', String),
            Column('raw_error', String),
            Column('error_code', String),
            Column('obs_day', DateTime),
            Column('submitted_at', DateTime),
            Column('latency', String),
            Column('inserted_at', DateTime),
        )

        metadata.create_all(engine)



class ObsInventory(Base):
    __tablename__ = OBS_INVENTORY_TABLE

    obs_id = Column(Integer, primary_key=True)
    filename = Column(String(255))
    parent_dir = Column(String(1023))
    platform = Column(String(63))
    s3_bucket = Column(String(63))
    prefix = Column(String(63))
    cycle_tag = Column(String(63))
    data_type = Column(String(63))
    cycle_time = Column(Integer)
    obs_day = Column(DateTime())
    data_format = Column(String(63))
    suffix = Column(String(63))
    nr_tag = Column(Boolean())
    file_size = Column(Integer())
    permissions = Column(String(15))
    last_modified = Column(DateTime())
    inserted_at = Column(DateTime())


class HpssCmdResult(Base):
    __tablename__ = HPSS_CMD_RESULTS_TABLE

    cmd_result_id = Column(Integer, primary_key=True)
    command = Column(String(512))
    arg0 = Column(String(256))
    raw_output = Column(String(50000))
    raw_error = Column(String(50000))
    error_code = Column(Integer())
    obs_day = Column(DateTime())
    submitted_at = Column(DateTime())
    latency = Column(Float())
    inserted_at = Column(DateTime())


def insert_obs_inv_items(obs_inv_items):
    if not isinstance(obs_inv_items, list):
        msg = 'Inserted observation inventory items must be in the form' \
              f' of a list.  Received type: {type(obs_inv_items)}'
        raise TypeError(msg)


    rows = []
    for obs_item in obs_inv_items:
        if not isinstance(obs_item, se.TarballFileMeta):
            msg = 'Each observation inventory item must be in the form' \
                  f' of TarballFileMeta. Item type: {type(obs_item)}'
            raise TypeError(msg)

        tbl_item = ObsInventory(
            filename=obs_item.filename,
            parent_dir=obs_item.parent_dir,
            platform=obs_item.platform,
            s3_bucket=obs_item.s3_bucket,
            prefix=obs_item.prefix,
            cycle_tag=obs_item.cycle_tag,
            data_type=obs_item.data_type,
            cycle_time=obs_item.cycle_time,
            obs_day=obs_item.obs_day,
            data_format=obs_item.data_format,
            suffix=obs_item.suffix,
            nr_tag=obs_item.nr_tag,
            file_size=obs_item.file_size,
            permissions=obs_item.permissions,
            last_modified=obs_item.last_modified,
            inserted_at=obs_item.inserted_at,
        )
        rows.append(tbl_item)

    session = Session()
    session.bulk_save_objects(rows)
    session.commit()
    session.close()


def insert_hpss_cmd_result(hpss_cmd_result):
    if not isinstance(hpss_cmd_result, se.HpssCmdResult):
        msg = 'Inserted hpss command result item must be in the form' \
              f' of type: HpssCmdResult.  Received type: {type(hpss_cmd_result)}'
        raise TypeError(msg)

    tbl_item = HpssCmdResult(
        command=hpss_cmd_result.command,
        arg0=hpss_cmd_result.arg0,
        raw_output=hpss_cmd_result.raw_output,
        raw_error=hpss_cmd_result.raw_error,
        error_code=hpss_cmd_result.error_code,
        obs_day=hpss_cmd_result.obs_day,
        submitted_at=hpss_cmd_result.submitted_at,
        latency=hpss_cmd_result.latency,
        inserted_at=datetime.utcnow()
    )

    session = Session()
    session.add(tbl_item)
    session.commit()
    session.close()


create_obs_inventory_table()
create_hpss_cmd_results_table()
