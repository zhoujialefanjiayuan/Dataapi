from datetime import datetime,timedelta

import  pymysql as py

host = '101.132.47.14'
port = 3306
ps = 'w113796'
us = 'root'
database = 'user_log'

con = py.connect(host=host,password=ps,port= port,user= us,database=database,autocommit=True)
cursor = con.cursor()
tablenamesql = 'show tables'
cursor.execute(tablenamesql)
tablenames = [i[0] for i in cursor.fetchall()]



#只抓取启动任务前5分钟数据
current_time = datetime.now() - timedelta(minutes=5)

for i in tablenames:
    search_sql = 'select sum(paied) from %s where created_at <="%s" and iscal_paied=0'%(i,current_time)
    cursor.execute(search_sql)
    sum = cursor.fetchall()[0][0]
    if sum == None:
        continue
    changepaied = 'update %s set iscal_paied=1 where created_at <= "%s" and iscal_paied=0'%(i,current_time)
    cursor.execute(changepaied)

    #更新余额
    username = i.split('_')[0]
    update_sql = 'update dataapi.user set balance = (balance -%s) where username="%s"'%(sum,username)
    print(update_sql)
    cursor.execute(update_sql)
    con.close()










