#!/usr/bin/env python

import os
from sqlite3 import dbapi2 as sqlite


FULL = 'dict.sqlite'
BARE = 'dict_bare.sqlite'
os.unlink(BARE)
TABS1 = [ 'browse_keyword', 'browse_usage', 'browse_keyword_usage' ]
TABS2 = [ tab.replace('browse_','') for tab in TABS1 ]

conn = sqlite.connect(BARE)
curs = conn.cursor()
curs.execute("ATTACH '%s' AS orig;"%FULL)

for TAB1,TAB2 in map(None,TABS1,TABS2):
    sql = "SELECT sql FROM orig.sqlite_master WHERE name='%s';"%TAB1
    create, = curs.execute(sql).fetchone()
    curs.execute(create.replace('browse_',''))
    sql = "INSERT INTO %s SELECT * FROM orig.%s;"%(TAB2,TAB1)
    curs.execute(sql)

conn.commit()
conn.close()
