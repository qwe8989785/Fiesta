import pymysql

def getDataByAct(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'act_Id' not in keys:
        return '004A'
    Id = inputJson['act_Id']
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select Id from show_UserFeedBack where Useable = true and act_Id="%s" limit 1 ), 0);' % Id
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == 0 :
        return '013'
    sql = 'SHOW COLUMNS FROM show_UserFeedBack'
    cursor.execute(sql)
    title = []
    data = {}
    result = cursor.fetchall()
    for i in result:
        title.append(i[0])
    sql = 'select * from show_UserFeedBack where act_Id = \'%s\'' % Id
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
    if 'show_scoreId' not in keys:
        return "004N"
    if 'act_Id' not in keys:
        return "004A"
    if 'Useable' not in keys:
        return "0045"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'insert into show_UserFeedBack('
    for i in range(len(keys)):
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
    if 'Id' not in keys :
        return "0048"
    if 'Useable' in keys:
        return "0046"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from show_UserFeedBack where Useable = true and Id="%s" limit 1 ), 0);' % inputJson['Id']
    cursor.execute(sql)
    result =cursor.fetchone()
    if(result[0] == 0):
        db.close()
        return "002"
    Id = result[0]
    keys.remove('Id')
    values.remove(inputJson['Id'])
    sql = 'update show_UserFeedBack set '
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
    if 'Id' not in keys:
        return "0048"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from show_UserFeedBack where Useable = true and Id="%s" limit 1 ), 0);' % inputJson['Id']
    cursor.execute(sql)
    Id =cursor.fetchone()
    if(Id[0] == 0):
        db.close()
        return "002"
    sql = 'update show_UserFeedBack set Useable = false where Id = \'%s\'' % Id[0]
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return "001"
    except:
        db.rollback()
        db.close()
        return "006"