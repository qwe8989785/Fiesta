import pymysql

def getDataByShow(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'showId' not in keys:
        return '004I'
    Id = inputJson['showId']
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Skills39', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select Id from showScore where Useable = true and showId="%s" limit 1 ), 0);' % Id
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == 0 :
        return '013'
    sql = 'SHOW COLUMNS FROM showScore'
    cursor.execute(sql)
    title = []
    data = {}
    result = cursor.fetchall()
    for i in result:
        title.append(i[0])
    sql = 'select * from showScore where showId = \'%s\'' % Id
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    data = []
    for i in range(len(result)):
        array = {}
        for j in range(len(result[0])):   
                array[title[j]] = str(result[i][j])
        data.append(array)
    return data

def getDataByAuth(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'auth_Id' not in keys:
        return '0048'
    Id = inputJson['auth_Id']
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Skills39', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select Id from showScore where Useable = true and accountId="%s" limit 1 ), 0);' % Id
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == 0 :
        return '013'
    sql = 'SHOW COLUMNS FROM showScore'
    cursor.execute(sql)
    title = []
    data = {}
    result = cursor.fetchall()
    for i in result:
        title.append(i[0])
    sql = 'select * from showScore where accountId = \'%s\'' % Id
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    data = []
    for i in range(len(result)):
        array = {}
        for j in range(len(result[0])):   
                array[title[j]] = str(result[i][j])
        data.append(array)
    return data

def uploadData(inputJson):
    keys = []
    values = []
    for i in inputJson.keys():
        keys.append(i)
    for i in inputJson.values():
        values.append(i)
    if 'authId' not in keys:
        return "0048"
    if 'showId' not in keys:
        return "004A"
    if 'Useable' not in keys:
        return "0045"
    if 'scoreDate' not in keys:
        return '004L'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Skills39', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'insert into showScore('
    for i in range(len(keys)):
        if keys[i] == 'authId':
            keys[i] = 'accountId'
        if i == len(keys)-1:
            sql = sql + keys[i] +')values('
        else:
            sql = sql + keys[i] + ',' 
    for i in range(len(values)):
        if i == len(values)-1:
            if values[i] == 'true' or values[i] == 'false' :
                sql = sql + str(values[i]) +');'
            else:    
                sql = sql + '\'' +str(values[i]) + '\'' +');'
        else:
            if values[i] =='true' or values[i] == 'false':
                sql = sql + str(values[i]) + ','
            else:    
                sql = sql+ '\'' + str(values[i]) + '\''+ ','
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
    except:
        db.rollback()
        db.close()
        return '006'
    
def updateData(inputJson):
    keys = []
    values = []
    for i in inputJson.keys():
        keys.append(i)
    for i in inputJson.values():
        values.append(i)
    if 'show_scoreId' not in keys :
        return "004N"
    if 'Useable' in keys:
        return "0046"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Skills39', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from showScore where Useable = true and Id="%s" limit 1 ), 0);' % inputJson['actScoreId']
    cursor.execute(sql)
    result =cursor.fetchone()
    if(result[0] == 0):
        db.close()
        return "002"
    Id = result[0]
    keys.remove('show_scoreId')
    values.remove(inputJson['show_scoreId'])
    sql = 'update showScore set '
    for i in range(len(keys)):
        if i == len(keys)-1:
            if(values[i] == 'true'):
                sql = sql + keys[i] + '=' + 'true' + ' where Id = \'%s\'' % Id
            elif (values[i] == 'false'):
                sql = sql + keys[i] + '=' + 'false' + ' where Id = \'%s\'' % Id
            else:
                sql = sql + keys[i] + '=' + '\'' + str(values[i]) + '\'' + ' where Id = \'%s\'' % Id
        else:
            if(values[i] == 'true'):
                sql = sql + keys[i] + '=' + 'true,'
            elif (values[i] == 'false'):
                sql = sql + keys[i] + '=' + 'false,'
            else:
                sql = sql + keys[i] + '=' + '\'' + str(values[i]) + '\',' 
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return "001"
    except:
        db.rollback()
        db.close()
        return "006" 
    
def deleteData(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'show_scoreId' not in keys:
        return "004N"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Skills39', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from showScore where Useable = true and Id="%s" limit 1 ), 0);' % inputJson['show_scoreId']
    cursor.execute(sql)
    Id =cursor.fetchone()
    if(Id[0] == 0):
        db.close()
        return "002"
    sql = 'update showScore set Useable = false where Id = \'%s\'' % Id[0]
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return "001"
    except:
        db.rollback()
        db.close()
        return "006"