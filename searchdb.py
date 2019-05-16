import pymysql

record = None

def sqlinsert(gender,age,corner):
    con = pymysql.connect(host ='localhost', user='root', password = '1234', db = 'marketplace')
    cur = con.cursor()
    sqlread = "insert into market values('"+gender+"','"+age+"','"+corner+"','')"
    cur.execute(sqlread)
    con.commit()
    con.close()


def sqlselect():
    con = pymysql.connect(host ='localhost', user='root', password = '1234', db = 'marketplace')
    cur = con.cursor()
    sqlread = "select * from market"
    cur.execute(sqlread)
    record = cur.fetchall()
    con.commit()
    con.close()
    return record