import datetime

from oslo_config import cfg
from oslo_db.sqlalchemy import models
from sqlalchemy import (Column, String)
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import orm
from sqlalchemy import DateTime, Integer, Text, JSON
from sqlalchemy import PrimaryKeyConstraint, ForeignKey

CONF = cfg.CONF
BASE = declarative_base()


def MediumText():
    return Text().with_variant(MEDIUMTEXT(), 'mysql')


class MatildaCostBase(models.ModelBase):
    metadata = None

    def __copy__(self):
        session = orm.Session()

        copy = session.merge(self, load=False)
        session.expunge(copy)
        return copy

    def save(self, session=None):
        from matilda_cost.db.sqlalchemy import api as db_api
        if session is None:
            session = db_api.get_session()

        super(MatildaCostBase, self).save(session=session)

    def delete(self, session=None):
        from matilda_cost.db.sqlalchemy import api as db_api
        if session is None:
            session = db_api.get_session()

        super(MatildaCostBase, self).delete(session=session)

    def __repr__(self):
        items = ['%s=%r' % (col.name, getattr(self, col.name))
                 for col in self.__table__.columns]
        return "<%s.%s[object at %x] {%s}>" % (self.__class__.__module__,
                                               self.__class__.__name__,
                                               id(self), ','.join(items))

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Accounts(BASE, MatildaCostBase):

    __tablename__ = 'accounts'

    account_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    created_dt = Column(DateTime)
    cloud_provider = Column(String(50))
    credentials = Column(JSON)

class Granularity(BASE, MatildaCostBase):
    __tablename__ = 'Granularity'
    cd = Column(Integer, primary_key=True)
    value = Column(String(45))


class Metrics(BASE, MatildaCostBase):
    __tablename__ = 'Metrics'
    cd = Column(Integer, primary_key=True)
    value = Column(String(45))


class Config_Type(BASE, MatildaCostBase):
    __tablename__ = 'Config_Type'
    cd = Column(Integer, primary_key=True)
    value = Column(String(45))


class Dimension(BASE, MatildaCostBase):
    __tablename__ = 'Dimension'
    cd = Column(Integer, primary_key=True)
    value = Column(String(45))


class Config(BASE, MatildaCostBase):
    __tablename__ = 'Config'
    __table_args__ = {'autoload': True}
    __table_args__ = (
        PrimaryKeyConstraint('Key'),
    )
    Key = Column(Integer, ForeignKey('Dimension.cd'))
    Type = Column(Integer, ForeignKey('config_type.cd'))

class ReqPayload(BASE, MatildaCostBase):

    __tablename__ = 'req_payload'

    id = Column(Integer, autoincrement=True,
                primary_key=True)
    input_json = Column(JSON)
    output_json_from_aws = Column(JSON)
    output_json_for_ui = Column(JSON)
    account_id = Column(String(20))


class Request(BASE, MatildaCostBase):

    __tablename__ = 'request'

    request_id = Column(Integer, autoincrement=True,
                        primary_key=True)
    start_dt = Column(DateTime, primary_key=True)
    end_dt = Column(DateTime, primary_key=True)
    account_id = Column(String(20))
    time_stamp = Column(DateTime, default=datetime.datetime.now())
    groupby = Column(JSON)
    filter_by = Column(JSON)
