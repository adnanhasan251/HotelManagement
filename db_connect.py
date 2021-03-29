import sqlite3

def connect(dbname):
    global cursor, dbconn
    dbconn = sqlite3.connect(dbname+'.db')
    cursor = dbconn.cursor()
def create(tname, head):
    cursor.execute("CREATE TABLE IF NOT EXISTS "+tname+" ("+head+")")
    # could also use for increase readability:
    # cursor.execute(f"CREATE TABLE IF NOT EXISTS {tname} ({head})")
def insert(tname, data):
    cursor.execute("INSERT INTO "+tname+" VALUES ("+data+")")
    dbconn.commit()
def update(tname, uinfo, condition):
    cursor.execute("UPDATE "+tname+" SET "+uinfo+" WHERE "+condition)
    dbconn.commit()
    # could also use:
    # cursor.execute(f"UPDATE {tname} SET {uinfo} where {condition}")

def get(tname, info, _filter):  # filter is a reserved keyword in python.
    cursor.execute("SELECT "+info+" FROM "+tname+" WHERE "+_filter)
    # could also use:
    # cursor.execute(f"SELECT {info} FROM {tname} WHERE {filter}")
    _get = cursor.fetchall()    # will cause some nasty bugs since `get`
                                # is already a defined function. So changed to `_get`
    return _get

def seetable(tname):
    cursor.execute("SELECT * FROM "+tname)
    tablecontent = cursor.fetchall()
    return tablecontent

def delt(tname, cond):
    cursor.execute("DELETE FROM "+tname+" WHERE "+cond)
    dbconn.commit()
