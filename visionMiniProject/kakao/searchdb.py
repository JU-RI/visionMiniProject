import pymysql

record = None

def sqlinsert(gender, age, corner):
    con = pymysql.connect(host='localhost', user='root', password='1234', db='marketplace')
    cur = con.cursor()
    sqlread = "insert into market values('"+gender+"','"+age+"','"+corner+"')"
    cur.execute(sqlread)
    con.commit()
    con.close()

def sqlselect():
    global result
    con = pymysql.connect(host='localhost', user='root', password='1234', db='marketplace')
    cur = con.cursor()
    sqlread = "select * from market"
    cur.execute(sqlread)
    record = cur.fetchall()
    # result = []
    # while True:
    #     record = cur.fetchone()
    #     if record == None:
    #         break
    #     else:
    #         result.append(list(record))
    # print(result)
    con.commit()
    con.close()
    return record