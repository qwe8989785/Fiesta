# -*- coding: utf-8 -*-
import pymysql
import TagModel
import math
import time
import re
import random
def getActByTag(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if "Tag" not in keys:
        return '004G'
    Tag = TagModel.setTag(inputJson['Tag'])
    if Tag == None:
        return '013'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select * from Activity where Tag like \'%{tag}%\' and act_Status = true and Useable = true and viewStatus = true order by rand() limit 10;'.format(tag=Tag)
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) == 0:
        return '013'
    sql = 'SHOW COLUMNS FROM Activity'
    cursor.execute(sql)
    title = []
    for i in cursor.fetchall():
        title.append(i[0])
    data = []
    for i in range(len(result)):
        array = {}
        for j in range(len(result[0])):
            if title[j] == 'Tag' :
                array[title[j]] = TagModel.catchTag(result[i][j])
            elif title[j] == 'startTime' or title[j] == 'endTime':
                if str(result[i][j]) == 'None':
                    array[title[j]] = str(result[i][j])
                else:
                    startTime = time.mktime(time.strptime(str(result[i][j]),"%Y-%m-%d %H:%M:%S"))
                    array[title[j]] = time.strftime("%Y-%m-%d %H:%M", time.localtime(startTime))
            elif title[j] == 'Photo':
                if str(result[i][j]) == 'None':
                    array[title[j]] = str('https://imgur.com/iNGnle2.jpg')
                else:
                    array[title[j]] = str(result[i][j])
            else:    
                array[title[j]] = str(result[i][j])
        data.append(array)
    return data

def getRecommendAct(inputJson,Id):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if "act_Id" not in keys:
        return '004A'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select Latitude,Longitude,Distance,Tag from FiestaAccount where Id = \'%s\';' % Id
    cursor.execute(sql)
    result = cursor.fetchone()
    if len(result) == 0:
        return '014' 
    Lat = result[0]
    Lon = result[1]
    Km_Dis = result[2]
    Tag = result[3]
    sql = 'SHOW COLUMNS FROM Activity'
    cursor.execute(sql)
    title = []
    for i in cursor.fetchall():
        title.append(i[0])
    La_dis = Km_Dis / 110.574
    Lo_dis = Km_Dis / (111.320*math.cos(Lat*math.pi/180))
    data = []
    if len(inputJson['act_Id'])!=0:
        for i in Tag.split(','):
            sql = 'select * from Activity where Latitude < {bigLat} or Latitude > {smallLat} or Longitude < {bigLon} or Longitude > {smallLon} and Tag like \'%{Tag}%\' and Id not In('.format(bigLat=Lat+La_dis,smallLat=Lat-La_dis,bigLon=Lon+Lo_dis,smallLon=Lon-Lo_dis,Tag = i)
            for no,values in enumerate(inputJson['act_Id']):
                if no == len(inputJson['act_Id']) -1:
                    sql = sql + str(values)
                else:
                    sql = sql  + str(values) +','
            sql = sql + ') and Useable = true and act_Status = true and viewStatus = true order by rand() limit 10;'
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) != 0:
                for act in result:
                    data.append(act)
    else:
        for i in Tag.split(','):
            sql = 'select * from Activity where Latitude < {bigLat} or Latitude > {smallLat} or Longitude < {bigLon} or Longitude > {smallLon} and Tag like \'%{Tag}%\' and Useable = true and act_Status = true  and viewStatus = true order by rand() limit 10;'.format(bigLat=Lat+La_dis,smallLat=Lat-La_dis,bigLon=Lon+Lo_dis,smallLon=Lon-Lo_dis,Tag = i)
            cursor.execute(sql)
            result = cursor.fetchall()
            if len(result) != 0:
                for act in result:
                    data.append(act)
    final = []
    for act in random.sample(data,10):
        temp = {}
        for i in range(len(title)):
            if title[i] == 'Tag' :
                temp[title[i]] = TagModel.catchTag(act[i])
            elif title[i] == 'startTime' or title[i] == 'endTime':
                if str(act[i]) == 'None':
                    temp[title[i]] = str(act[i])
                else:
                    startTime = time.mktime(time.strptime(str(act[i]),"%Y-%m-%d %H:%M:%S"))
                    temp[title[i]] = time.strftime("%Y-%m-%d %H:%M", time.localtime(startTime))
            elif title[i] == 'Photo':
                    if str(act[i]) == 'None':
                        temp[title[i]] = str('https://imgur.com/iNGnle2.jpg')
                    else:
                        temp[title[i]] = str(act[i])
            else:    
                temp[title[i]] = str(act[i])
        final.append(temp)
    return final

def getRecommendActTest(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if "act_Id" not in keys:
        return '004A'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'SHOW COLUMNS FROM Activity'
    cursor.execute(sql)
    title = []
    for i in cursor.fetchall():
        title.append(i[0])
    if len(inputJson['act_Id'])!=0:
        sql = 'select * from Activity where Id not in (';
        for no,values in enumerate(inputJson['act_Id']):
            if no == len(inputJson['act_Id']) -1:
                sql = sql + str(values)
            else:
                sql = sql  + str(values) +','
        sql = sql + ') and Useable = true and act_Status = true and viewStatus = true order by rand() limit 10;'
    else:
        sql = 'select * from Activity where Useable = true and act_Status = true and viewStatus = true order by rand() limit 10;'
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) == 0:
        return '013'
    data = []
    for i in range(len(result)):
        array = {}
        for j in range(len(result[0])):
            if title[j] == 'Tag' :
                array[title[j]] = TagModel.catchTag(result[i][j])
            elif title[j] == 'startTime' or title[j] == 'endTime':
                if str(result[i][j]) == 'None':
                    array[title[j]] = str(result[i][j])
                else:
                    startTime = time.mktime(time.strptime(str(result[i][j]),"%Y-%m-%d %H:%M:%S"))
                    array[title[j]] = time.strftime("%Y-%m-%d %H:%M", time.localtime(startTime))
            elif title[j] == 'Photo':
                if str(result[i][j]) == 'None':
                    array[title[j]] = str('https://imgur.com/iNGnle2.jpg')
                else:
                    array[title[j]] = str(result[i][j])
            else:    
                array[title[j]] = str(result[i][j])
        data.append(array)
    return data
def getActivityData(inputJson):
    Id = inputJson['Id']
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select Id from Activity where Useable = true and Id="%s" limit 1 ), 0);' % Id
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == 0 :
        db.close()
        return '010'
    sql = 'SHOW COLUMNS FROM Activity'
    cursor.execute(sql)
    title = []
    data = {}
    result = cursor.fetchall()
    for i in result:
        title.append(i[0])
    sql = 'select * from Activity where Id = \'%s\'' % Id
    cursor.execute(sql)
    result = cursor.fetchone()
    for i in range(len(title)):
        if title[i] == 'Tag' :
            data[title[i]] = TagModel.catchTag(result[i])
        elif title[i] == 'startTime' or title[i] == 'endTime':
            if str(result[i]) == 'None':
                data[title[i]] = str(result[i])
            else:
                startTime = time.mktime(time.strptime(str(result[i]),"%Y-%m-%d %H:%M:%S"))
                data[title[i]] = time.strftime("%Y-%m-%d %H:%M", time.localtime(startTime))
        elif title[i] == 'Photo':
                if str(result[i]) == 'None':
                    data[title[i]] = str('https://imgur.com/iNGnle2.jpg')
                else:
                    data[title[i]] = str(result[i])
        else:    
            data[title[i]] = str(result[i])
    sql = 'select accountId from ActivityJoinedList where act_Id = \'%s\';' % Id
    cursor.execute(sql)
    data['joinedAuth'] = []
    for i in cursor.fetchall():
        data['joinedAuth'].append(i[0])
    db.close()
    return data

def uploadActivityData(inputJson):
    keys = []
    values = []
    for i in inputJson.keys():
        keys.append(i)
    for i in inputJson.values():
        values.append(i)
    if 'act_Name' not in keys:
        return "0047"
    if 'Useable' not in keys:
        return "0045"
    if 'Tag' not in keys:
        return '004G'
    if 'viewStauts' not in keys :
        return '004Q'
    if 'peopleMaxium' not in keys :
        return '004R'
    Tag = TagModel.setTag(inputJson['Tag'])
    for i in range(len(values)):
        if values[i] == inputJson['Tag']:
            values[i] = Tag
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'insert into Activity('
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
    cursor.execute(sql)
    sql = 'update FiestaGroup set deadLine = \'{time}\' where Id = \'{Id}\';'.format(time=inputJson['endTime'],Id = inputJson['groupId'] )
    cursor.execute(sql)
    try:   
        db.commit()
       # db.close()
       # return '001'
    except:
        print(sql)
        db.rollback()
        db.close()
        return '006'
    sql = 'select Id from activity where act_Name = \'{name}\' and groupId =\'{group}\' and Useable = true and startTime = \'{time}\';'.format(name=inputJson['act_Name'],group=inputJson['groupId'],time=inputJson['startTime'])
    cursor.execute(sql)
    result = cursor.fetchone()
    return {'act_Id' : result[0]}

def updateActivityData(inputJson):
    keys = []
    values = []
    for i in inputJson.keys():
        keys.append(i)
    for i in inputJson.values():
        values.append(i)
    if 'act_Id' not in keys :
        return "004A"
    if 'Useable' in keys:
        return "0046"
    if 'Tag' in keys:
            Tag = TagModel.setTag(inputJson['Tag'])
            for i in range(len(values)):
                if values[i] == inputJson['Tag']:
                    values[i] = Tag
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from Activity where Useable = true and Id="%s" limit 1 ), 0);' % inputJson['act_Id']
    cursor.execute(sql)
    result =cursor.fetchone()
    if(result[0] == 0):
        db.close()
        return "002"
    Id = result[0]
    keys.remove('act_Id')
    values.remove(inputJson['act_Id'])
    sql = 'update Activity set '
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
    
def deleteActivityData(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'Id' not in keys:
        return "0048"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from Activity where Useable = true and Id="%s" limit 1 ), 0);' % inputJson['Id']
    cursor.execute(sql)
    Id =cursor.fetchone()
    if(Id[0] == 0):
        db.close()
        return "002"
    sql = 'update Activity set Useable = false where Id = \'%s\'' % Id[0]
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return "001"
    except:
        db.rollback()
        db.close()
        return "006"
def updataUnexpiredActivity(InputJson):
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select act_Id from ActivityJoinedList join Activity on ActivityJoinedList.act_Id = Activity.Id where Activity.act_Status = true and Activity.Useable = true and ActivityJoinedList.Useable = true and ActivityJoinedList.accountId = \'%s\';' % InputJson['Id']
    cursor.execute(sql)
    JoinedActList = cursor.fetchall()
    sql = 'select Id , act_Id from unexpiredActivity where accountId = \'%s\' and Useable = true;' % InputJson['Id']
    cursor.execute(sql)
    unexpiredActList = cursor.fetchall()
    unexpiredId=[]
    unexpiredActId=[]
    JoinedActId=[]
    if len(unexpiredActList) == 0:
        for i in JoinedActList:
            sql = 'insert into unexpiredActivity(act_Id,accountId,Useable) values(\'{act_Id}\',\'{account_Id}\',true);'.format(act_Id=i[0],account_Id = InputJson['Id'])
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
                db.close()
                return "006" 
        db.close()
        return '001'
    else:
        for i in unexpiredActList:
            unexpiredId.append(i[0])
            unexpiredActId.append(i[1])
        for i in JoinedActList:
            JoinedActId.append(i[0])
        for i in JoinedActId:
            if i not in unexpiredActId:
                sql = 'insert into unexpiredActivity(act_Id,accountId,Useable) values(\'{act_Id}\',\'{account_Id}\',true);'.format(act_Id=i,account_Id = InputJson['Id'])
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    db.rollback()
                    db.close()
                    return "006"
        for i in range(len(unexpiredId)):
            if unexpiredActId[i] not in JoinedActId:
                sql = 'update unexpiredActivity set Useable = False where Id = \'%s\';' % unexpiredId[i]
                try:
                    cursor.execute(sql)
                    db.commit()
                except:
                    db.rollback()
                    db.close()
                    return "006"
    db.close()
    return '001'

def deleteJoinedAct(inputJson):
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
    sql = 'update ActivityJoinedList set Useable = False where Id =\'%s\';' % ListId[0]
    cursor.execute(sql)
    sql = 'update Activity set JoinedCount = JoinedCount - 1 where Id = \'%s\';' % inputJson['act_Id']
    cursor.execute(sql)
    try:
        db.commit()
        db.close()
        return '001'
    except:
        db.rollback()
        db.close()
        return "006"

def getJoinedAuth(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'act_Id' not in keys:
        return "004A"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select accountId,Auth.userName,Auth.nickName,ticketKinds,ticketStatus,Notes from ActivityJoinedList join FiestaAccount as Auth on accountId = Auth.Id where act_Id = \'%s\';' % inputJson['act_Id']
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    data = []
    for i in result:
        array = {
            'authId' : str(i[0]),
            'userName' : str(i[1]),
            'nickName' : str(i[2]),
            'ticketKinds' : str(i[3]),
            'ticketStatus' : str(i[4]),
            'Notes' : str(i[5])
        }
        data.append(array)
    return data

def setJoinedAuth(inputJson):
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
    result = cursor.fetchone()
    if result[0] != 0:
        db.close()
        return '018'
    sql = 'select peopleMaxium-joinedCount from activity where Id =\'%s\';' % inputJson['act_Id']
    cursor.execute(sql)
    result = cursor.fetchone()
    if result[0] == 0:
        db.close()
        return '017'
    if 'ticketKinds' in keys:
        sql = 'insert into ActivityJoinedList(act_Id,accountId,ticketKinds,ticketStatus,Useable,Notes) values(\'{actId}\',\'{accountId}\',\'{ticket}\',false,true,\'{Notes}\');'.format(actId = inputJson['act_Id'],accountId = inputJson['authId'],ticket = inputJson['ticketKinds'],Notes = inputJson['Notes'])
    else:
        sql = 'insert into ActivityJoinedList(act_Id,accountId,ticketStatus,Useable,Notes) values(\'{actId}\',\'{accountId}\',false,true,\'{Notes}\');'.format(actId = inputJson['act_Id'],accountId = inputJson['authId'],Notes = inputJson['Notes'])
    cursor.execute(sql)
    sql = 'update Activity set JoinedCount = JoinedCount + 1 where Id = \'%s\';' % inputJson['act_Id']
    cursor.execute(sql)
    try:
        db.commit()
        db.close()
        return '001'
    except:
        db.rollback()
        db.close()
        return "006"

def setJoinedAuthbyGroup(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'groupId' not in keys:
        return "0049"
    if 'act_Id' not in keys:
        return "004A"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from GroupMember where Useable = true and groupId=\'%s\' limit 1 ), 0);' % inputJson['groupId']
    cursor.execute(sql)
    result = cursor.fetchone()
    if result[0] == 0:
        return '011'
    sql = 'select accountId from GroupMember where groupId = \'%s\';' % inputJson['groupId']
    cursor.execute(sql)
    result = cursor.fetchall()
    sql = 'select peopleMaxium-joinedCount from activity where Id =\'%s\';' % inputJson['act_Id']
    cursor.execute(sql)
    people = cursor.fetchone()
    if people[0] < len(result):
        return '017'
    for i in result:
        sql = 'select ifnull((select id  from ActivityJoinedList where Useable = true and act_Id=\'{actId}\' and accountId = \'{accountId}\' limit 1 ), 0);'.format(actId = inputJson['act_Id'],accountId = i[0])
        cursor.execute(sql)
        ex = cursor.fetchone()
        if ex[0] == 0:
            if 'ticketKinds' in keys:
                sql = 'insert into ActivityJoinedList(act_Id,accountId,ticketKinds,Useable) values(\'{actId}\',\'{accountId}\',\'{ticket}\',true);'.format(actId = inputJson['act_Id'],accountId = i[0],ticket = inputJson['ticketKinds'])
            else:
                sql = 'insert into ActivityJoinedList(act_Id,accountId,Useable) values(\'{actId}\',\'{accountId}\',true);'.format(actId = inputJson['act_Id'],accountId = i[0])
            cursor.execute()
            sql = 'update Activity set JoinedCount = JoinedCount + 1 where Id = \'%s\';' % inputJson['act_Id']
            cursor.execute(sql)
    try:     
        db.commit()
        db.close()
        return '001'
    except:
        db.rollback()
        db.close()
        return "006"    
    
def getTouchPeople(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'act_Id' not in keys:
        return "004A"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select accountId from act_touchPeople where act_Id = \'%s\';' % inputJson['act_Id']
    cursor.execute(sql)
    touchList = {
            'authId' : []
            }
    for i in cursor.fetchall():
        touchList['authId'].append(str(i[0]))
    db.close()
    return touchList

def setTouchPeople(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'authId' not in keys:
        return "0048"
    if 'act_Id' not in keys:
        return "004A"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'insert into act_touchPeople(act_Id,accountId,Useable) values(\'{actId}\',\'{accountId}\',true);'.format(actId = inputJson['act_Id'],accountId = inputJson['authId'])
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return '001'
    except:
        db.rollback()
        db.close()
        return "006"

def deleteTouchPeople(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'authId' not in keys:
        return "0048"
    if 'act_Id' not in keys:
        return "004A"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from act_touchPeople where Useable = true and act_Id=\'{actId}\' and accountId = \'{accountId}\' limit 1 ), 0);'.format(actId = inputJson['act_Id'],accountId = inputJson['authId'])
    cursor.execute(sql)
    ListId = cursor.fetchone()
    if(ListId[0] == 0):
        db.close()
        return '010'
    sql = 'update act_touchPeople set Useable = False where Id =\'%s\';' % ListId[0]
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return '001'
    except:
        db.rollback()
        db.close()
        return "006"

def updateOverTimeAct():
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select Id from Activity where endTime < sysdate() ;'
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) == 0:
        return '010'
    for Id in result:
        sql = 'update Activity set act_Status = False where Id = \'%d\';' % Id[0]
        cursor.execute(sql)
        sql = 'update unexpiredActivity set Useable = False where Id = \'%d\';' % Id[0]
        cursor.execute(sql)
    try:
        db.commit()
        db.close()
        return '001'
    except:
        db.rollback()
        db.close()
        return "006"
        
def getSimpleData(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'Search' not in keys:
        return '004B'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'SHOW COLUMNS FROM Activity'
    cursor.execute(sql)
    title = []
    for i in cursor.fetchall():
        title.append(i[0])
    sql = 'select * from Activity where act_Name like \'%{search}%\' limit 10;'.format(search=inputJson['Search'])
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result)==0:
        db.close()
        return '013'
    data = []
    for i in range(len(result)):
        array = {}
        for j in range(len(result[0])):
            if title[j] == 'Tag' :
                array[title[j]] = TagModel.catchTag(result[i][j])
            elif title[j] == 'startTime' or title[j] == 'endTime':
                if str(result[i][j]) == 'None':
                    array[title[j]] = str(result[i][j])
                else:
                    startTime = time.mktime(time.strptime(str(result[i][j]),"%Y-%m-%d %H:%M:%S"))
                    array[title[j]] = time.strftime("%Y-%m-%d %H:%M", time.localtime(startTime))
            elif title[j] == 'Photo':
                if str(result[i][j]) == 'None':
                    array[title[j]] = str('https://imgur.com/iNGnle2.jpg')
                else:
                    array[title[j]] = str(result[i][j])
            else:    
                array[title[j]] = str(result[i][j])
        data.append(array)
    return data   

def CountPeople(inputJson):
    key = []
    for i in inputJson.keys():
        key.append(i)
    if 'act_Id' not in key:
        return '004A'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select Id from Activity where Useable = true and Id="%s" limit 1 ), 0);' % inputJson['act_Id']
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == 0 :
        db.close()
        return '010'
    sql ='select Models from Activity where Useable = true and Id=\'%s\';' % inputJson['act_Id']
    cursor.execute(sql)
    Models = cursor.fetchone()
    if Models[0] == None or  '3' not in re.split(r',',Models[0]):
        sql ='select count(*) from ActivityJoinedList where Useable = true and act_Id=\'%s\';' % inputJson['act_Id']
        cursor.execute(sql)
        result = cursor.fetchone()
        print('result:'+str(result[0]))
        data = [
            {
                'People' : result[0]
            }
        ]
        return data
    else :
        result = re.split(r',',Models[0])
        if '3' in result:
            sql = 'select ticketKinds,Mounts-Remainder from Ticket where act_Id = \'%s\';' % inputJson['act_Id']
            cursor.execute(sql)
            ticket = cursor.fetchall()
            if len(ticket) == 0:
                return '013'
            data = []
            array ={}
            total = 0
            for i in ticket:
                total += i[1]
                array [i[0]]=i[1]
            array['total'] = total
            data.append(array)
            print('result:'+str(ticket))
            return data
        
def getExpireAct(Id):
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select Act.Id,Act.act_Name,Act.act_Description,Act.Photo,Act.act_Status from ActivityJoinedList as JL join Activity as Act on JL.act_Id = Act.Id where JL.Expired = true and JL.accountId = \'%s\';' % Id
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    if len(result) == 0:
        return '013'
    data = []
    for i in result:
        array = {
                    'Id' : str(i[0]),
                    'act_Name' : str(i[1]),
                    'act_Description' : str(i[2]),
                    'Photo' : str(i[3]),
                    'act_Status' : str(i[4])
                }
        data.append(array)
    return data   

def getTicketData(Id,act_Id):
    key = []
    for i in inputJson.keys():
        key.append(i)
    if 'act_Id' not in key:
        return '004A'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta_Online', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select accountId,Auth.userName,Auth.nickName,ticketKinds,ticketStatus,Notes from ActivityJoinedList join FiestaAccount as Auth on accountId = Auth.Id where act_Id = \'{act_Id}\' and accountId = \'{authId}\';'.format(act_Id=inputJson['act_Id'],authId = Id) 
    cursor.execute(sql)
    result = cursor.fetchone()
    db.close()
    data = [{
        'act_Id': str(inputJson['act_Id']),
        'authId' : str(result[0]),
        'userName' : str(result[1]),
        'nickName' : str(result[2]),
        'ticketKinds' : str(result[3]),
        'ticketStatus' : str(result[4]),
        'Notes' : str(result[5])
    }]
    return data
