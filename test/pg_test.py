# -*- coding utf-8 -*-

import psycopg2
import psycopg2.extras

dns = 'host=127.0.0.1 port=5432 dbname=testdb user=test_User01 password=testUser01'
with psycopg2.connect(dns) as con:
    with con.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute("select version() as ver")
        row = cur.fetchone()
        print(row['ver'])
#[EOF]