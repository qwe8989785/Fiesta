import pymysql

def getTicketData(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'ticketId' not in keys:
        return '004P'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id from Ticket where Useable = true and Id="%s" limit 1 ), 0);' % inputJson['ticketId']
    cursor.execute(sql)
    result =cursor.fetchone()
    if result[0] == 0 :
        db.close()
        return "013"
    sql = 'select * from Ticket where Useable = true and Id="%s";' % inputJson['ticketId']
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    data = []
    for i in result:
        array = {
                    "Id" : str(i[0]),
                    "act_Id" : str(i[1]),
                    "ticketKinds" :str(i[2]),
                    "Mounts" : str(i[3]),
                    "Remainder" : str(i[4]),
                    "Price" : str(i[5]),
                    "Useable" : str(i[6])
                }
        data.append(array)
    return data 

def getTicketDatabyActId(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'act_Id' not in keys:
        return '004A'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id from Ticket where Useable = true and act_Id="%s" limit 1 ), 0);' % inputJson['act_Id']
    cursor.execute(sql)
    result =cursor.fetchone()
    if result[0] == 0 :
        db.close()
        return "013"
    sql = 'select * from Ticket where Useable = true and act_Id="%s";' % inputJson['act_Id']
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    data = []
    for i in result:
        array = {
                    "Id" : str(i[0]),
                    "act_Id" : str(i[1]),
                    "ticketKinds" :str(i[2]),
                    "Mounts" : str(i[3]),
                    "Remainder" : str(i[4]),
                    "Price" : str(i[5]),
                    "Useable" : str(i[6])
                }
        data.append(array)
    return data 

def uploadTicketData(inputJson):
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
    if 'ticketKinds' not in keys:
        return '004O'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'insert into Ticket('
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
    
def updateTicketData(inputJson):
    keys = []
    values = []
    for i in inputJson.keys():
        keys.append(i)
    for i in inputJson.values():
        values.append(i)
    if 'ticketId' not in keys :
        return "004P"
    if 'Useable' in keys:
        return "0046"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from Ticket where Useable = true and Id="%s" limit 1 ), 0);' % inputJson['ticketId']
    cursor.execute(sql)
    result =cursor.fetchone()
    if(result[0] == 0):
        db.close()
        return "002"
    Id = result[0]
    keys.remove('ticketId')
    values.remove(inputJson['ticketId'])
    sql = 'update Ticket set '
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

def deleteTicketData(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'ticketId' not in keys :
        return "004P"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from Ticket where Useable = true and Id = \'%s\' limit 1 ), 0);'%inputJson['ticketId']
    cursor.execute(sql)
    ListId = cursor.fetchone()
    if(ListId[0] == 0):
        db.close()
        return '010'
    sql = 'update TicketList set Useable = False where Id =\'%s\';' % ListId[0]
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return '001'
    except:
        db.rollback()
        db.close()
        return "006"
    
def vaildTicket(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'authId' not in keys :
        return "0048"
    if 'act_Id' not in keys :
        return "004A"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from unexpiredActivity where Useable = true and act_Id=\'{actId}\' and accountId = \'{accountId}\' and ticketStatus = false limit 1 ), 0);'.format(actId = inputJson['act_Id'],accountId = inputJson['authId'])
    cursor.execute(sql)
    Id = cursor.fetchone()
    if(Id[0] == 0):
        db.close()
        return '010'
    sql = 'update unexpiredActivity set ticketStatus = true where Id = \'%s\';' % Id[0]
    cursor.execute(sql)
    sql = 'select ifnull((select id  from ActivityJoinedList where Useable = true and act_Id=\'{actId}\' and accountId = \'{accountId}\' and ticketStatus = false limit 1 ), 0);'.format(actId = inputJson['act_Id'],accountId = inputJson['authId'])
    cursor.execute(sql)
    Id = cursor.fetchone()
    sql = 'update ActivityJoinedList set ticketStatus = true where Id = \'%s\';' % Id[0]
    cursor.execute(sql)
    try:
        db.commit()
        db.close()
        return '001'
    except:
        db.rollback()
        db.close()
        return "006"
    
def vaildTicketbyQRcode(inputJson,authId):
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select  Act.Id from groupMember join Activity as Act on groupId = Act.groupId where accountId = \'%s\';' % authId
    cursor.execute(sql)
    result = cursor.fetchall()
    if result == None:
        return '022'
    temp = []
    for i in result:
        temp.append(i[0])
    if inputJson['act_Id'] not in temp:
        return '022'
    sql = 'select ifnull((select id  from unexpiredActivity where Useable = true and act_Id=\'{actId}\' and accountId = \'{accountId}\' and ticketStatus = false limit 1 ), 0);'.format(actId = inputJson['act_Id'],accountId = authId)
    cursor.execute(sql)
    Id = cursor.fetchone()
    if(Id[0] == 0):
        db.close()
        return '010'
    sql = 'update unexpiredActivity set ticketStatus = true where Id = \'%s\';' % Id[0]
    cursor.execute(sql)
    sql = 'select ifnull((select id  from ActivityJoinedList where Useable = true and act_Id=\'{actId}\' and accountId = \'{accountId}\' and ticketStatus = false limit 1 ), 0);'.format(actId = inputJson['act_Id'],accountId = authId)
    cursor.execute(sql)
    Id = cursor.fetchone()
    sql = 'update ActivityJoinedList set ticketStatus = true where Id = \'%s\';' % Id[0]
    cursor.execute(sql)
    try:
        db.commit()
    except:
        db.rollback()
        db.close()
        return "006"
    sql = 'select Act.act_Name,Auth.nickName,ticketKinds,ticketStatus,Notes from ActivityJoinedList join Activity as Act on act_Id = Act.Id join FiestaAccount as Auth on accountId = Auth.Id where Id = \'%s\' ;' % Id[0]
    cursor.execute(sql)
    result = cursor.fetchone()
    db.close()
    data = [{
        'act_Name' : result[0],
        'nickName' : result[1],
        'ticketKinds' : result[2],
        'ticketStatus' : result[3],
        'Notes' : result[4]
    }]
    return data

def updateTicketNotes(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'authId' not in keys:
        return "0048"
    if 'act_Id' not in keys:
        return "004A"
    if 'Notes' not in keys:
        return "004S"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from ActivityJoinedList where Useable = true and act_Id=\'{actId}\' and accountId = \'{accountId}\' limit 1 ), 0);'.format(actId = inputJson['act_Id'],accountId = inputJson['authId'])
    cursor.execute(sql)
    ListId = cursor.fetchone()
    if(ListId[0] == 0):
        db.close()
        return '010'
    sql = 'update ActivityJoinedList set Notes = \'{Notes}\' where Id =\'{Id}\';'.format(Notes = inputJson['Notes'],Id = ListId[0])
    cursor.execute(sql)
    try:
        db.commit()
        db.close()
        return '001'
    except:
        db.rollback()
        db.close()
        return "006"

def updateTicketStatusFalse(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'authId' not in keys:
        return "0048"
    if 'act_Id' not in keys:
        return "004A"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from ActivityJoinedList where Useable = true and act_Id=\'{actId}\' and accountId = \'{accountId}\' limit 1 ), 0);'.format(actId = inputJson['act_Id'],accountId = inputJson['authId'])
    cursor.execute(sql)
    ListId = cursor.fetchone()
    if(ListId[0] == 0):
        db.close()
        return '010'
    sql = 'update ActivityJoinedList set ticketStatus = False where Id =\'%s\';' % ListId[0]
    cursor.execute(sql)
    try:
        db.commit()
        db.close()
        return '001'
    except:
        db.rollback()
        db.close()
        return "006"