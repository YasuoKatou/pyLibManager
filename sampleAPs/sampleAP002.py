# -*- coding utf-8 -*-

import json
import logging
import logging.config
import pathlib

from pyLibManager.lib_manager import load_classes
from pyLibManager.lib_manager import run_lib_manager
from pyLibManager.lib_manager import setLogConfig

class SampleAP002:

    def __init__(self):
        log_conf = self._initLogger()
        self.myAppDef = {
            'logConfig': log_conf,
            'clazzDef': [
                {'module': 'pyLibManager.DBs.PostgreSQL.pgClass', 'classes': []}
            ],
            'DBInfo': {
                'pgDef': {
                    'host': '127.0.0.1', 'port': 5432,
                    'dbname': 'testdb',
                    'user': 'test_User01', 'password': 'testUser01',
                },
            },
            'app': {
                'config':[
                    {"fqdn": "pyLibManager.DBs.PostgreSQL.pgClass.PG",
                     "method": "setLogConfig",
                     "param": "logConfig"
                    },
                    {'fqdn': 'pyLibManager.DBs.PostgreSQL.pgClass.PG',
                    'method': 'setDns',
                    'param': 'DBInfo.pgDef',
                    },
                    {'fqdn': 'pyLibManager.DBs.PostgreSQL.pgClass.PG',
                    'method': 'connect',
                    'result': 'dto.db.connect',
                    },
                    {'fqdn': 'pyLibManager.DBs.PostgreSQL.pgClass.PG',
                    'method': 'getCursor',
                    'param': 'dto.db.connect',
                    'result': 'dto.db.cursor',
                    },
                    {'fqdn': 'pyLibManager.DBs.PostgreSQL.pgClass.PG',
                    'method': 'showServerVersion',
                    'param': 'dto.db.cursor',
                    },
                ]
            },
            'dto': {'db': {'connect': None, 'cursor': None}}
        }
        load_classes(self.myAppDef, defPrint=True)

    def _initLogger(self):
        p = pathlib.Path(__file__)
        j = p.parent / 'sampleAP_log.json'
        with open(j, 'r') as f:
            log_conf = json.load(f)
        logging.config.dictConfig(log_conf)
        self.logger = logging.getLogger(__name__)
        return log_conf

    def run(self):
        self.logger.info('start SampleAP002.run')
        setLogConfig(self.myAppDef['logConfig'])
        run_lib_manager(self.myAppDef)
        self.logger.info('end SampleAP002.run')

if __name__ == '__main__':
    ap = SampleAP002()
    ap.run()

#[EOF]