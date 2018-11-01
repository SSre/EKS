import datetime
import logging
import uuid

from sqlalchemy import Boolean, BigInteger, Column, DateTime, Enum, Float
from sqlalchemy import dialects
from sqlalchemy import ForeignKey, Index, Integer, MetaData, String, Table, JSON
from sqlalchemy import Text
from sqlalchemy.types import NullType

log = logging.getLogger(__name__)


def MediumText():
    return Text().with_variant(dialects.mysql.MEDIUMTEXT(), 'mysql')


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    accounts = Table('accounts', meta,
                     Column('account_id', Integer,
                            primary_key=True, autoincrement=True),
                     Column('name', String(50)),
                     Column('created_dt', DateTime),
                     Column('cloud_provider', String(50)),
                     Column('credentials', JSON),
                     mysql_engine='InnoDB',
                     mysql_charset='utf8')

    granularity = Table('Granularity', meta,
                        Column('id', Integer, primary_key=True, autoincrement=True),
                        Column('value', String(length=50)),
                        mysql_engine='InnoDB',
                        mysql_charset='utf8')


    metrics = Table('Metrics', meta,
                    Column('id', Integer, primary_key=True, autoincrement=True),
                    Column('value', String(length=50)),
                    mysql_engine = 'InnoDB',
                    mysql_charset = 'utf8')


    config_Type = Table('Config_Type', meta,
                        Column('id', Integer, primary_key=True, autoincrement=True),
                        Column('value', String(length=50)),
                        mysql_engine='InnoDB',
                        mysql_charset='utf8')

    dimension = Table('Dimension', meta,
                      Column('id', Integer, primary_key=True, autoincrement=True),
                      Column('value', String(length=50)),
                      mysql_engine = 'InnoDB',
                      mysql_charset = 'utf8')

    config = Table('Config', meta,
                   Column('id', Integer, primary_key=True, autoincrement=True),
                   Column('value', String(length=50)),
                   mysql_engine='InnoDB',
                   mysql_charset='utf8')

    request = Table('request', meta,
                      Column('request_id', Integer, primary_key=True, autoincrement=True),
                      Column('start_dt', DateTime),
                      Column('end_dt', DateTime),
                      Column('account_id', String(length=20)),
                      Column('time_stamp', DateTime),
                      Column('groupby', JSON),
                      Column('filter_by', JSON),
                      mysql_engine = 'InnoDB',
                      mysql_charset = 'utf8')

    req_payload = Table('req_payload', meta,
                   Column('id', Integer, primary_key=True, autoincrement=True),
                   Column('input_json', JSON),
                   Column('output_json_from_aws', JSON),
                   Column('output_json_for_ui', JSON),
                   Column('account_id', String(length=20)),
                   mysql_engine='InnoDB',
                   mysql_charset='utf8')

    tables = [accounts, granularity, metrics, config_Type, dimension, config, request, req_payload]

    for table in tables:
        try:
            table.create()
        except Exception:
            log.info(repr(table))
            log.exception('Exception while creating table')
            raise

    if migrate_engine.name == 'mysql':
        migrate_engine.execute(
            'ALTER TABLE migrate_version CONVERT TO CHARACTER SET utf8')
        migrate_engine.execute(
            'ALTER DATABASE %s DEFAULT CHARACTER SET utf8' %
            migrate_engine.url.database)


def downgrade(migrage_engine):
    raise NotImplementedError('Downgrade is not implemented')
