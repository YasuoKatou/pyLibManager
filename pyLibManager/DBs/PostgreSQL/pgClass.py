# -*- coding utf-8 -*-

import psycopg2
import psycopg2.extras

class PG:

    def setDns(self, dnsDict):
        wk = []
        for key, value in dnsDict.items():
            wk.append('%s=%s' % (key, str(value), ))
        self.dns = ' '.join(wk)
        print('dns : %s' % (self.dns, ))

    def connect(self):
        return psycopg2.connect(self.dns)

    def getCursor(self, conn):
        return conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def showServerVersion(self, cur):
        cur.execute("select version() as ver")
        row = cur.fetchone()
        print(row['ver'])

#[EOF]