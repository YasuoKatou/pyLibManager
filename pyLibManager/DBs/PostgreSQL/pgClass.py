# -*- coding utf-8 -*-

import os
import psycopg2
import psycopg2.extras

class PG:

    def setDns(self, dnsDict):
        wk = []
        for key, value in dnsDict.items():
            wk.append('%s=%s' % (key, str(value), ))
        self.dns = ' '.join(wk)
        print('dns : %s' % (self.dns, ))

    def setDnsString(self, dnsString):
        self.dns = dnsString
        print('dns : %s' % (self.dns, ))

    def getDnsByEnv(self, env_name):
        dns = os.environ.get(env_name)
        assert dns, '環境変数[%s] (PostgreSQL接続文字列) が設定されていません.' % (env_name, )
        return dns

    def connect(self):
        return psycopg2.connect(self.dns)

    def getCursor(self, conn):
        return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def showServerVersion(self, cur):
        cur.execute("select version() as ver")
        row = cur.fetchone()
        print(row['ver'])

#[EOF]