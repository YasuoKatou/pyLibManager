# -*- coding utf-8 -*-

from pyLibManager.lib_manager import load_classes
from pyLibManager.lib_manager import run_lib_manager

class SampleAP002:

    def __init__(self):
        self.myAppDef = {
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
            'app': [
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
            ],
            'dto': {'db': {'connect': None, 'cursor': None}}
        }
        load_classes(self.myAppDef, defPrint=True)

    def run(self):
        print('start SampleAP002.run')
        run_lib_manager(self.myAppDef)
        print('end SampleAP002.run')

if __name__ == '__main__':
    ap = SampleAP002()
    ap.run()

#[EOF]