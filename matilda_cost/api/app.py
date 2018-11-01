from oslo_config import cfg
import oslo_messaging as messaging
from oslo_log import log
from flask_oslolog import OsloLog

from matilda_cost.api.controller.api import app
from etc.path import get_file
import json
import sys


CONF = cfg.CONF

opts = [
    cfg.StrOpt('api_host', default='0.0.0.0'),
    cfg.StrOpt('api_port', default=6011),
]
CONF.register_opts(opts)
LOG = OsloLog(app).logger
#LOG = log.getLogger(__name__)


def build_server():
    log.register_options(CONF)
    CONF(default_config_files=['{0}'.format(get_file())])
    host, port = CONF.api_host, CONF.api_port
    debug = CONF.debug
    LOG.info('App server running on %r:%r' % (host, port))
    app.run(host, int(port), debug=True)

build_server()
