# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 21:37:08 2020

@author: user
"""
import pymysql
import time
def getShowData(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'act_Id' not in keys:
        return '004A'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select * from showList where act_Id = \'%s\' and Useable = true ORDER BY showTime ASC;' % inputJson['act_Id']
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    if len(result) == 0:
        return '013'
    data = []
    for i in result:
        array = {
                    "Id" : str(i[0]),
                    "act_Id" : str(i[1]),
                    "showName" :str(i[2]),
                    "Detail" : str(i[3]),
                    "showTime" : str(i[4]),
                    "showStatus" : str(i[5]),
                    "Useable" : str(i[6])
                }
        if array['showTime'] != 'None':
            showTime = time.mktime(time.strptime(str(i[4]),"%Y-%m-%d %H:%M:%S"))
            array['showTime'] = time.strftime("%Y-%m-%d %H:%M", time.localtime(showTime))
        data.append(array)
    return data 
def uploadShowData(inputJson):
    keys = []
    values = []
    for i in inputJson.keys():
        keys.append(i)
    for i in inputJson.values():
        values.append(i)
    if 'Useable' not in keys:
        return '0045'
    if 'act_Id' not in keys:
        return '004A'
    if 'showName' not in keys:
        return '004D'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'insert into showList('
    for i in range(len(keys)):
        if i == len(keys)-1:
            sql = sql + keys[i] +')values('
        else:
            sql = sql + keys[i] + ',' 
    for i in range(len(values)):
        if i == len(values)-1:
            if values[i] == 'true':
                sql = sql + str(values[i]) +');'
            else:    
                sql = sql + '\'' +str(values[i]) + '\'' +');'
        else:
            if values[i] =='true':
                sql = sql + str(values[i]) + ','
            else:    
                sql = sql+ '\'' + str(values[i]) + '\''+ ','
    try:
        cursor.execute(sql)
        db.commit()
    except:
        print(sql)
        db.rollback()
        db.close()
        return '006'
    sql = 'select Id from New;'
    cursor.execute(sql)
    result = cursor.fetchone()
    db.close()
    data = {'showId' : result[0]}
    return data  

def updateShowData(inputJson):
    keys = []
    values = []
    for i in inputJson.keys():
        keys.append(i)
    for i in inputJson.values():
        values.append(i)
    if 'showId' not in keys:
        return '0048'
    if 'Useable' in keys:
        return "0046"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from showList where Useable = true and Id="%s" limit 1 ), 0);' % inputJson['showId']
    cursor.execute(sql)
    result = cursor.fetchone()
    if(result[0] == 0):
        db.close()
        return "013"
    Id = result[0]
    keys.remove('showId')
    values.remove(inputJson['showId'])
    sql = 'select act_Id from showList where Id = \'%s\';'%Id
    cursor.execute(sql)
    result = cursor.fetchone()
    act_Id = result[0]
    sql = 'update showList set '
    for i in range(len(keys)):
        if i == len(keys)-1:
            if(values[i] == 'true'):
                sql = sql + str(keys[i]) + '=' + 'true' + ' where Id = \'%s\'' % Id
            elif (values[i] == 'false'):
                sql = sql + str(keys[i]) + '=' + 'false' + ' where Id = \'%s\'' % Id
            else:
                sql = sql + str(keys[i]) + '=' + '\'' + str(values[i]) + '\'' + ' where Id = \'%s\'' % Id
        else:
            if(values[i] == 'true'):
                sql = sql + str(keys[i]) + '=' + 'true,'
            elif (values[i] == 'false'):
                sql = sql + str(keys[i]) + '=' + 'false,'
            else:
                sql = sql + str(keys[i]) + '=' + '\'' + str(values[i]) + '\',' 
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return '001'
    except:
        db.rollback()
        db.close()
        return "006" 

def deleteShow(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'showId' not in keys:
        return "004I"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from showList where Useable = true and Id = \'%s\' limit 1 ), 0);'%inputJson['showId']
    cursor.execute(sql)
    ListId = cursor.fetchone()
    if(ListId[0] == 0):
        db.close()
        return '010'
    sql = 'update showList set Useable = False where Id =\'%s\';' % ListId[0]
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return '001'
    except:
        db.rollback()
        db.close()
        return "006"