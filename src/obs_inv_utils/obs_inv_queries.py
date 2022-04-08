import sqlalchemy as db
from datetime import datetime
from pandas import DataFrame
from sqlalchemy import Table, Column, MetaData
from sqlalchemy import Integer, String, Boolean, DateTime, Float
from sqlalchemy import inspect
from sqlalchemy import func, select, column
from sqlalchemy import and_, or_, not_
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


from obs_inv_utils import inventory_table_factory as itf

engine = db.create_engine(itf.OBS_SQLITE_DATABASE, echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)


def get_filesize_timeline_data(min_instances):

    insp = inspect(engine)
    table_exists = insp.has_table(itf.OBS_INVENTORY_TABLE)

    if not table_exists:
        msg = f'Table \'{itf.OBS_INVENTORY_TABLE}\' does not ' \
              f'exist in database: \'{itf.OBS_SQLITE_DATABASE}\'.'
        raise ValueError(msg)

    session = Session()
    oi = itf.ObsInventory

    unique_names = session.query(
        oi.filename,
        func.count(oi.filename).label('instances'),
        oi.data_type,
        oi.suffix,
        oi.data_type.concat(oi.suffix).label('un')
    ).select_from(
        oi
    ).group_by(
        'un'
    ).subquery()

    print(f'subquery unique_names: {unique_names}')

    fn_fs = session.query(
        oi.prefix,
        oi.filename,
        oi.cycle_tag,
        oi.cycle_time,
        oi.file_size,
        oi.obs_day,
        oi.inserted_at,
        unique_names.c.instances,
        unique_names.c.un
    ).select_from(
        oi
    ).join(
        unique_names,
        and_(
            unique_names.c.data_type == oi.data_type,
            unique_names.c.suffix == oi.suffix
        )
    ).filter(
        and_(
            unique_names.c.instances > min_instances,
            oi.prefix != '',
            oi.cycle_time != None,
            not_(
                or_(
                    oi.filename.contains('.txt'),
                    oi.filename.contains('./'),
                    oi.filename.contains('.nr.nr'),
                    oi.filename.contains('/tmp')
                )
            )
        )
    ).order_by(
        unique_names.c.instances, oi.filename, oi.obs_day
    ).all()

    df = DataFrame(fn_fs)

    return df
