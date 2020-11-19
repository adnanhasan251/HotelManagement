import sqlite3
def connect(dbname):
    global cursor, dbconn
    dbconn = sqlite3.connect(dbname+'.db')
    cursor = dbconn.cursor()
def create(tname, head):
    cursor.execute("CREATE TABLE IF NOT EXISTS "+tname+" ("+head+")")
def insert(tname, data):
    cursor.execute("INSERT INTO "+tname+" VALUES ("+data+")")
    dbconn.commit()
def update(tname, uinfo, condition):
    cursor.execute("UPDATE "+tname+" SET "+uinfo+" WHERE "+condition)
def get(tname, info, filter):
    cursor.execute("SELECT "+info+" FROM "+tname+" WHERE "+filter)
    get=cursor.fetchall()
    return get
def seetable(tname):
    cursor.execute("SELECT * FROM "+tname)
    tablecontent=cursor.fetchall()
    return tablecontent

'''connect('test11')
create('tabletest', 'fname, lname, phone')
insert("tabletest", "'adnan', 'hasan', 12345")
insert("tabletest", "'test1', 'test2', 123456")
update('tabletest', "lname='HASAN'", "fname='adnan'")
print(seetable('tabletest'))
print(get("tabletest", "fname", "lname='test2'"))'''