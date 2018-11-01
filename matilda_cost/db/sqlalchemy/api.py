""" 8/14/2018, 04:30 PM """
# coding=utf-8
# !/usr/bin/env python

import sys
import threading

from oslo_config import cfg
from sqlalchemy import DateTime, Integer, Text, JSON
from oslo_db import exception as db_exc
from oslo_db import options as oslo_db_options
from oslo_db.sqlalchemy import session as db_session
from oslo_db.sqlalchemy import utils as sqlalchemyutils
from oslo_log import log as logging
from sqlalchemy.exc import SQLAlchemyError
from matilda_cost.db.sqlalchemy import models
from matilda_cost.utils.time import get_time
from sqlalchemy.sql.expression import cast
import MySQLdb


api_db_opts = [
    cfg.StrOpt('db_connection',
               secret=True,
               default='mysql+pymysql://root:openstack@192.168.10.226/matilda_cost'),
]

CONF = cfg.CONF

opt_group = cfg.OptGroup(name='database')
CONF.register_group(opt_group)
CONF.register_opts(oslo_db_options.database_opts, opt_group)
CONF.register_opts(api_db_opts, opt_group)


LOG = logging.getLogger(__name__)

_ENGINE_FACADE = {'matilda_cost': None}
_CSS_FACADE = 'matilda_cost'
_LOCK = threading.Lock()


def _create_facade(conf_group):

    return db_session.EngineFacade(
        sql_connection=conf_group.db_connection,
        autocommit=True,
        expire_on_commit=False,
        mysql_sql_mode=conf_group.mysql_sql_mode,
        idle_timeout=conf_group.idle_timeout,
        connection_debug=conf_group.connection_debug,
        max_pool_size=conf_group.max_pool_size,
        max_overflow=conf_group.max_overflow,
        pool_timeout=conf_group.pool_timeout,
        sqlite_synchronous=conf_group.sqlite_synchronous,
        connection_trace=conf_group.connection_trace,
        max_retries=conf_group.max_retries,
        retry_interval=conf_group.retry_interval)


def _create_facade_lazily(facade, conf_group):
    global _LOCK, _ENGINE_FACADE
    if _ENGINE_FACADE[facade] is None:
        with _LOCK:
            if _ENGINE_FACADE[facade] is None:
                _ENGINE_FACADE[facade] = _create_facade(conf_group)
    return _ENGINE_FACADE[facade]


def get_engine(use_slave=False):
    conf_group = CONF.database
    facade = _create_facade_lazily(_CSS_FACADE, conf_group)
    return facade.get_engine(use_slave=use_slave)


def get_session(use_slave=False, **kwargs):
    conf_group = CONF.database
    facade = _create_facade_lazily(_CSS_FACADE, conf_group)
    return facade.get_session(use_slave=use_slave, **kwargs)


def get_backend():
    """The backend is this module itself."""
    return sys.modules[__name__]


def model_query(model,
                args=None,
                session=None):
    if session is None:
        session = get_session()

    query = sqlalchemyutils.model_query(model, session, args)
    return query

def get_accounts(cloud_provider, name):
    try:
        session = get_session()
        with session.begin():
            query = session.query(models.Accounts)
            if cloud_provider != None:
                query = query.filter_by(cloud_provider=cloud_provider)
            if name is not None:
                query = query.filter_by(name=name)
            return query.all()
    except (MySQLdb.Error, MySQLdb.Warning, SQLAlchemyError) as e:
        return str(e)

def get_granularity():
    try:
        session = get_session()
        with session.begin():
            query = session.query(models.Granularity)
            return query.all()
    except (MySQLdb.Error, MySQLdb.Warning, SQLAlchemyError) as e:
        return str(e)

def get_metrics():
    try:
        session = get_session()
        with session.begin():
            query = session.query(models.Metrics)
            return query.all()
    except (MySQLdb.Error, MySQLdb.Warning, SQLAlchemyError) as e:
        return str(e)

def get_group_by():
    try:
        session = get_session()
        with session.begin():
            query = session.query(models.Dimension.value).join(models.Config). \
                    filter(models.Config_Type.cd == 1). \
                    filter(models.Config_Type.cd == models.Config.Type)
            return query.all()
    except (MySQLdb.Error, MySQLdb.Warning, SQLAlchemyError) as e:
        return str(e)


def get_filter():
    try:
        session = get_session()
        with session.begin():
            query = session.query(models.Dimension.value).join(models.Config). \
                    filter(models.Config_Type.cd == 2). \
                    filter(models.Config_Type.cd == models.Config.Type)
            return query.all()
    except (MySQLdb.Error, MySQLdb.Warning, SQLAlchemyError) as e:
        return str(e)

def create_dimension(id, value):
    data = {
        "cd": id,
        "value": value
    }
    try:
        session = get_session()
        with session.begin():
            req_data = models.Dimension()
            req_data.update(data)
            req_data.save(session=session)
        return req_data
    except (MySQLdb.Error, MySQLdb.Warning, SQLAlchemyError) as e:
        return str(e)

def create_account(name, cloud_provider, credentials):
    data = {
        "name": name,
        "created_dt": str(get_time()),
        "cloud_provider": cloud_provider,
        "credentials": credentials
    }
    try:
        session = get_session()
        with session.begin():
            req_data = models.Accounts()
            req_data.update(data)
            req_data.save(session=session)
        return req_data
    except (MySQLdb.Error, MySQLdb.Warning, SQLAlchemyError) as e:
        return str(e)

def create_config_type(id, value):
    data = {
        "cd": id,
        "value": value
    }
    try:
        session = get_session()
        with session.begin():
            req_data = models.Config_Type()
            req_data.update(data)
            req_data.save(session=session)
        return req_data
    except (MySQLdb.Error, MySQLdb.Warning, SQLAlchemyError) as e:
        return str(e)

def create_config(key, type):
    data = {
        "Key": key,
        "Type": type
    }
    try:
        session = get_session()
        with session.begin():
            req_data = models.Config()
            req_data.update(data)
            req_data.save(session=session)
        return req_data
    except (MySQLdb.Error, MySQLdb.Warning, SQLAlchemyError) as e:
        return str(e)

def create_granularity(id, value):
    data = {
        "cd": id,
        "value": value
    }
    try:
        session = get_session()
        with session.begin():
            req_data = models.Granularity()
            req_data.update(data)
            req_data.save(session=session)
        return req_data
    except (MySQLdb.Error, MySQLdb.Warning, SQLAlchemyError) as e:
        return str(e)

def create_metrics(id, value):
    data = {
        "cd": id,
        "value": value
    }
    try:
        session = get_session()
        with session.begin():
            req_data = models.Metrics()
            req_data.update(data)
            req_data.save(session=session)
        return req_data
    except (MySQLdb.Error, MySQLdb.Warning, SQLAlchemyError) as e:
        return str(e)

def update_account(account_id, name, credentials):
    try:
        session = get_session()
        with session.begin():
            query = session.query(models.Accounts)
            query = query.filter_by(account_id=account_id)
            query = query.filter_by(name=name)
            req_data = {
                'credentials': credentials
            }
            rows = query.update(req_data)
            if not rows:
                raise Exception('Failed Task Flow table update')
        return rows
    except (MySQLdb.Error, MySQLdb.Warning, SQLAlchemyError) as e:
        return str(e)

def create_req(data):
    try:
        session = get_session()
        with session.begin():
            req_data = models.Request()
            req_data.update(data)
            req_data.save(session=session)
        return req_data
    except (MySQLdb.Error, MySQLdb.Warning, SQLAlchemyError) as e:
        return str(e)

def create_req_payload(data):
    try:
        session = get_session()
        with session.begin():
            req_data = models.ReqPayload()
            req_data.update(data)
            req_data.save(session=session)
        return req_data
    except (MySQLdb.Error, MySQLdb.Warning, SQLAlchemyError) as e:
        return str(e)

def get_req(start_dt, end_dt, account_name):
    try:
        session = get_session()
        with session.begin():
            query = session.query(models.Request)
            if start_dt != None:
                query = query.filter_by(start_dt=start_dt)
            if end_dt is not None:
                query = query.filter_by(end_dt=end_dt)
            if account_name is not None:
                query = query.filter_by(account_id=account_name)
            return query.all()
    except (MySQLdb.Error, MySQLdb.Warning, SQLAlchemyError) as e:
        return str(e)

def get_req_payload(input_json):
    try:
        session = get_session()
        with session.begin():
            query = session.query(models.ReqPayload)
            if input_json != None:
                query = query.filter_by(input_json=cast(input_json, JSON))
            return query.all()
    except (MySQLdb.Error, MySQLdb.Warning, SQLAlchemyError) as e:
        return str(e)