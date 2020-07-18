import pymysql

def getRandomAccount(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'act_Id' not in keys:
        return '004A'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id from activityJoinedList where Useable = true and act_Id="%s" limit 1 ), 0);' % inputJson['act_Id']
    cursor.execute(sql)
    result =cursor.fetchone()
    if result[0] == 0 :
        db.close()
        return "013"
    sql = 'select accountId,auth.nickName from activityJoinedList as joined join FiestaAccount as auth on joined.accountId = auth.Id where joined.Useable = true and act_Id=\'%s\' and joined.ticketStatus = true order by rand() limit 1;' % inputJson['act_Id']
    cursor.execute(sql)
    result = cursor.fetchone()
    db.close()
    data = {
        'authId' : result[0],
        'nickName' : result[1]
    }
    return data 
def getLotteData(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'act_Id' not in keys:
        return '004A'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id from lotteList where Useable = true and act_Id="%s" limit 1 ), 0);' % inputJson['act_Id']
    cursor.execute(sql)
    result =cursor.fetchone()
    if result[0] == 0 :
        db.close()
        return "013"
    sql = 'select * from lotteList where Useable = true and act_Id="%s";' % inputJson['act_Id']
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    data = []
    for i in result:
        array = {
                    "Id" : str(i[0]),
                    "act_Id" : str(i[1]),
                    "accountId" :str(i[2]),
                    "Prize" : str(i[3]),
                    "lotteTime" : str(i[4]),
                    "Useable" : str(i[5])
                }
        data.append(array)
    return data 

def uploadLotteData(inputJson):
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
    if 'Prize' not in keys:
        return '004J'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'insert into lotteList('
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
        db.close()
        return '001'
    except:
        db.rollback()
        db.close()
        return '006'   
    
def updateLotteData(inputJson):
    keys = []
    values = []
    for i in inputJson.keys():
        keys.append(i)
    for i in inputJson.values():
        values.append(i)
    if 'lotteId' not in keys :
        return "004K"
    if 'Useable' in keys:
        return "0046"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from lotteList where Useable = true and Id="%s" limit 1 ), 0);' % inputJson['lotteId']
    cursor.execute(sql)
    result =cursor.fetchone()
    if(result[0] == 0):
        db.close()
        return "002"
    Id = result[0]
    keys.remove('lotteId')
    values.remove(inputJson['lotteId'])
    sql = 'update lotteList set '
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

def deleteLotteData(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'lotteId' not in keys :
        return "004K"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from lotteList where Useable = true and Id = \'%s\' limit 1 ), 0);'%inputJson['lotteId']
    cursor.execute(sql)
    ListId = cursor.fetchone()
    if(ListId[0] == 0):
        db.close()
        return '010'
    sql = 'update lotteList set Useable = False where Id =\'%s\';' % ListId[0]
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return '001'
    except:
        db.rollback()
        db.close()
        return "006"