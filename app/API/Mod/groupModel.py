# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 14:53:05 2020

@author: user
"""
import pymysql
import TagModel
def getGroupData(inputJson):
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from FiestaGroup where Useable = true and Id="%s" limit 1 ), 0);' % inputJson['groupId']
    cursor.execute(sql)
    result =cursor.fetchone()
    if result[0] == 0 :
        db.close()
        return "011"
    sql = 'SHOW COLUMNS FROM FiestaGroup'
    cursor.execute(sql)
    data = cursor.fetchall()
    title = []
    resultDit ={}
    for i in data :
        title.append(i[0])
    sql = 'SELECT * from FiestaGroup WHERE Id =\'%s\''% inputJson['groupId']
    cursor.execute(sql)
    result = cursor.fetchone()
    db.close()
    for i in range(len(title)):
        if title[i] == 'Tag' :
            print(TagModel.catchTag(result[i]))
            resultDit[title[i]] = TagModel.catchTag(result[i])
        elif title[i] == 'Photo':
            if str(result[i]) == 'None':
                resultDit[title[i]] = str('https://imgur.com/iNGnle2.jpg')
            else:
                resultDit[title[i]] = str(result[i])
        else:    
            resultDit[title[i]] = str(result[i])
    return resultDit
def uploadGroupData(inputJson):
    keys = []
    values = []
    for i in inputJson.keys():
        keys.append(i)
    for i in inputJson.values():
        values.append(i)
    if 'authId' not in keys:
        return "0048"
    if 'groupName' not in keys:
        return "0041"
    if 'Useable' not in keys:
        return "0045"
    if 'Tag' in keys:
        Tag = TagModel.setTag(inputJson['Tag'])
        for i in range(len(values)):
            if values[i] == inputJson['Tag']:
                values[i] = Tag
    keys.remove('authId')
    values.remove(inputJson['authId'])
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from FiestaGroup where Useable = true and groupName="%s" limit 1 ), 0);' % inputJson['groupName']
    cursor.execute(sql)
    result =cursor.fetchone()
    if(result[0] != 0):
        db.close()
        return "005"
    else:
        groupName = inputJson['groupName']
    sql = 'insert into FiestaGroup('
    for i in range(len(keys)):
        if i == len(keys)-1:
            sql = sql + keys[i] +')values('
        else:
            sql = sql + keys[i] + ',' 
    for i in range(len(values)):
        if i == len(values)-1:
            if values[i] == 'true' or values[i] == 'false':
                sql = sql + values[i] +');'
            else:    
                sql = sql + '\'' +values[i] + '\'' +');'
        else:
            if values[i] =='true' or values[i] == 'false':
                sql = sql + values[i] + ','
            else:    
                sql = sql+ '\'' + values[i] + '\''+ ','
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        db.close()
        print(sql)
        return '006'
    sql = 'select ifnull((select id  from FiestaGroup where Useable = true and groupName="%s" limit 1 ), 0);' % groupName
    cursor.execute(sql)
    groupId = cursor.fetchone()
    for i in range(len(inputJson['authId'])):
        if i == 0:
            sql = 'insert into GroupMember(groupId,accountId,Authority,Useable) values(\'{groupId}\',\'{accountId}\',\'{Authority}\',True);'.format(groupId =groupId[0],accountId =inputJson['authId'][i],Authority='3')
            print(sql)
            try:
                cursor.execute(sql)
                db.commit()
            except:
                db.rollback()
                db.close()
                print(sql)
                return '006'
        else:
            sql = 'insert into GroupMember(groupId,accountId,Authority,Useable) values(\'{groupId}\',\'{accountId}\',\'{Authority}\',True);'.format(groupId =groupId[0],accountId =inputJson['authId'][i],Authority='1')
            print(sql)
            try:
                cursor.execute(sql)
                db.commit()
            except pymysql.Error as e:
                print(e)
                db.rollback()
                db.close()
                print(sql)
                return '006'
    db.close()
    data = {'groupId':groupId[0]}
    return data
def updateGroupData(inputJson):
    keys = []
    values = []
    for i in inputJson.keys():
        keys.append(i)
    for i in inputJson.values():
        values.append(i)
    if 'groupId' not in keys :
        return "0049"
    if 'Useable' in keys:
        return "0046"
    if 'Tag' in keys:
        Tag = TagModel.setTag(inputJson['Tag'])
        for i in range(len(values)):
            if values[i] == inputJson['Tag']:
                values[i] = Tag
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from FiestaGroup where Useable = true and Id="%s" limit 1 ), 0);' % inputJson['groupId']
    cursor.execute(sql)
    result =cursor.fetchone()
    if(result[0] == 0):
        db.close()
        return "002"
    Id = result[0]
    keys.remove('groupId')
    values.remove(inputJson['groupId'])
    sql = 'update FiestaGroup set '
    for i in range(len(keys)):
        if i == len(keys)-1:
            if(values[i] == 'true'):
                sql = sql + keys[i] + '=' + 'true' + ' where Id = \'%s\'' % Id
            elif (values[i] == 'false'):
                sql = sql + keys[i] + '=' + 'false' + ' where Id = \'%s\'' % Id
            else:
                sql = sql + keys[i] + '=' + '\'' + values[i] + '\'' + ' where Id = \'%s\'' % Id
        else:
            if(values[i] == 'true'):
                sql = sql + keys[i] + '=' + 'true,'
            elif (values[i] == 'false'):
                sql = sql + keys[i] + '=' + 'false,'
            else:
                sql = sql + keys[i] + '=' + '\'' + values[i] + '\','  
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return "001"
    except:
        db.rollback()
        db.close()
        return "006" 

def deleteGroupData(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'groupId' not in keys:
        return "0049"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from FiestaGroup where Useable = true and Id="%s" limit 1 ), 0);' % inputJson['groupId']
    cursor.execute(sql)
    Id =cursor.fetchone()
    if(Id[0] == 0):
        db.close()
        return "002"
    sql = 'update FiestaGroup set Useable = false,timeStatus = false where Id = \'%s\'' % Id[0]
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return "001"
    except:
        db.rollback()
        db.close()
        return "006"

def getGroupMember(inputJson):    
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'groupId' not in keys:
        return "0049"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from groupMember where Useable = true and groupId="%s" limit 1 ), 0);' % inputJson['groupId']
    cursor.execute(sql)
    Id =cursor.fetchone()
    if(Id[0] == 0):
        db.close()
        return "013"
    sql = 'select accountId,Authority,FiestaAccount.Photo from groupMember join fiestaAccount on groupMember.accountId = fiestaAccount.Id where groupmember.groupId = \'%s\' and groupmember.Useable = true;' % inputJson['groupId']
    cursor.execute(sql)
    result = cursor.fetchall()
    db.close()
    data = []
    for i in result:
        array = {
            'authId' : str(i[0]),
            'Authority' : str(i[1]),
            'Photo' : str(i[2])
        }
        if str(i[2]) == 'None':
            array['Photo'] = str('https://imgur.com/iNGnle2.jpg')
        data.append(array)
    return data

def uploadGroupMember(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'authId' not in keys:
        return "0048"
    if 'groupId' not in keys:
        return "0049"
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from FiestaGroup where Useable = true and Id="%s" limit 1 ), 0);' % inputJson['groupId']
    cursor.execute(sql)
    Id =cursor.fetchone()
    if(Id[0] == 0):
        db.close()
        return "002"
    sql = 'select ifnull((select id  from FiestaAccount where Useable = true and Id="%s" limit 1 ), 0);' % inputJson['authId']
    cursor.execute(sql)
    Id =cursor.fetchone()
    if(Id[0] == 0):
        db.close()
        return "002"
    sql = 'insert into GroupMember(groupId,accountId,Authority,Useable) values(\'{groupId}\',\'{accountId}\',1,True);'.format(groupId=inputJson['groupId'],accountId=inputJson['authId'])
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return "001"
    except:
        db.rollback()
        db.close()
        return "006" 

def updateGroupMember(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'authId' not in keys:
        return "0048"
    if 'groupId' not in keys:
        return "0049"
    if 'Authority' not in keys:
        return '004H'
    if 'Useable' in keys :
        return '0046'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from GroupMember where Useable = true and groupId = \'{groupId}\' and accountId = \'{authId}\' limit 1 ), 0);'.format(groupId = inputJson['groupId'] , authId = inputJson['authId'])
    cursor.execute(sql)
    Id =cursor.fetchone()
    if(Id[0] == 0):
        db.close()
        return "002"
    
    sql = 'update GroupMember set Authority = \'{auth}\' where Id = \'{Id}\';'.format(auth = inputJson['Authority'],Id = Id[0])
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return "001"
    except:
        db.rollback()
        db.close()
        return "006"   
        
def deleteGroupMember(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if 'authId' not in keys:
        return "0048"
    if 'groupId' not in keys:
        return "0049"
    if 'Useable' in keys :
        return '0046'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from GroupMember where Useable = true and groupId = \'{groupId}\' and accountId = \'{authId}\' limit 1 ), 0);'.format( groupId = inputJson['groupId'] , authId = inputJson['authId'])
    cursor.execute(sql)
    Id =cursor.fetchone()
    if(Id[0] == 0):
        db.close()
        return "002"
    
    sql = 'update GroupMember set Useable = False where Id = \'{Id}\';'.format(Id = Id[0])
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return "001"
    except:
        db.rollback()
        db.close()
        return "006"   
    
def findName(inputJson):
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from FiestaGroup where Useable = true and groupName=\'%s\' limit 1 ), 0);' % inputJson['groupName']
    cursor.execute(sql)
    result =cursor.fetchone()
    if(result[0] != 0):
        db.close()
        return "005"
    db.close()
    return '001'
  
def selectGroupAct(inputJson):
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select id  from Activity where Useable = true and groupId=\'%s\' limit 1 ), 0);' % inputJson['groupId']
    cursor.execute(sql)
    result =cursor.fetchone()
    if(result[0] == 0):
        db.close()
        return "013"
    sql = 'select Id,act_Name from Activity where Useable = true and groupId=\'%s\';' % inputJson['groupId']
    cursor.execute(sql)
    result =cursor.fetchall()
    data = []
    for i in result:
        data.append({
            'Id' : str(i[0]),
            'act_Name' : str(i[1])
        })
    return data
        