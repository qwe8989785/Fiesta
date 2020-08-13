# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 14:10:03 2020

@author: user
"""
import datetime
import pymysql
import re
from . import TagModel,confirmModel
from ..Par import connectDB
import time
from flask_jwt_extended import create_access_token

class FiestaDbModel():
    def __init__(self):
        pass
    
    def getAccountData(self,inputJson):
        db = connectDB.connDB()
        cursor = db.cursor()
        sql = 'select ifnull((select Id from FiestaAccount where Useable = true and userId=\'{userId}\' and userPassword = SHA1(\'{pwd}\') limit 1 ), 0);'.format(userId = inputJson['userId'],pwd = inputJson['userPassword'])
        cursor.execute(sql)
        result =cursor.fetchone()
        if result[0] == 0 :
            db.close()
            return "003"
        sql = 'SHOW COLUMNS FROM FiestaAccount'
        cursor.execute(sql)
        data = cursor.fetchall()
        title = []
        resultDit ={}
        for i in data :
            title.append(i[0])
        sql = 'SELECT * from FiestaAccount WHERE userId =\'%s\''% inputJson['userId']
        cursor.execute(sql)
        result = cursor.fetchone()
        db.close()
        for i in range(len(title)):
            if title[i] == 'Tag' :
                resultDit[title[i]] = TagModel.catchTag(result[i])
            elif title[i] == 'Photo':
                if str(result[i]) == 'None':
                    resultDit[title[i]] = str('https://imgur.com/iNGnle2.jpg')
                else:
                    resultDit[title[i]] = str(result[i])
            elif title[i] != 'userPassword':
                resultDit[title[i]] = str(result[i])
            if title[i] == 'Id' :
                CM = confirmModel.AuthConfirm(result[i])
                expires = datetime.timedelta(days=3)
                resultDit['token'] = create_access_token(identity=result[i], expires_delta=expires)
        return resultDit
    
    def getLoginData(self,Id):
        db = connectDB.connDB()
        cursor = db.cursor()
        sql = 'select ifnull((select Id from FiestaAccount where Useable = true and Id=\'%s\' limit 1 ), 0);' % Id
        cursor.execute(sql)
        result =cursor.fetchone()
        if result[0] == 0 :
            db.close()
            return "002"
        sql = 'SHOW COLUMNS FROM FiestaAccount'
        cursor.execute(sql)
        data = cursor.fetchall()
        title = []
        resultDit ={}
        for i in data :
            title.append(i[0])
        sql = 'SELECT * from FiestaAccount WHERE Id =\'%s\''% Id
        cursor.execute(sql)
        result = cursor.fetchone()
        db.close()
        for i in range(len(title)):
            if title[i] == 'Tag' :
                resultDit[title[i]] = TagModel.catchTag(result[i])
            elif title[i] == 'Photo':
                if str(result[i]) == 'None':
                    resultDit[title[i]] = str('https://imgur.com/iNGnle2.jpg')
                else:
                    resultDit[title[i]] = str(result[i])
            elif title[i] != 'userPassword':    
                resultDit[title[i]] = str(result[i])
            
            if title[i] == 'Id' :
                #CM = confirm.AuthConfirm(result[i]) 
                #resultDit['loginToken'] = str(CM.create_Login_token())
                expires = datetime.timedelta(days=3)
                resultDit['token'] = create_access_token(identity=result[i], expires_delta=expires)
        return resultDit
        
    #上傳會員資料(需填必填欄位)
    def postUploadData(self,inputJson):
        keys = []
        values = []
        for i in inputJson.keys():
            keys.append(i)
        if 'userName' not in keys:
            return "0041"
        if 'userId' not in keys:
            return "0042"
        if 'userPassword' not in keys:
            return "0043"
        if 'Mail_1' not in keys:
            return "0044"
        if 'Useable' not in keys:
            return "0045"
        
        for i in inputJson.values():
            values.append('null' if i is None or i == "" else '\'%s\''%i)
        values[keys.index("userPassword")] = "SHA1(%s)" %values[keys.index("userPassword")]
        if 'Tag' in keys:
            values[keys.index("Tag")] = TagModel.setTag(inputJson['Tag'])

        db = connectDB.connDB()
        cursor = db.cursor()
        sql = 'select ifnull((select id  from FiestaAccount where Useable = true and userId="%s" limit 1 ), 0);' % inputJson['userId']
        cursor.execute(sql)
        result =cursor.fetchone()
        if(result[0] != 0):
            db.close()
            return "005"
        else:
            Id = inputJson['userId']

        #確認為學校信箱才可註冊
        rule = '^[a-zA-Z0-9]([._\\-]*[a-z0-9])*@([a-zA-Z0-9]*\.)*([a-z0-9][a-z0-9]*[a-z0-9].)edu.tw$'
        result = re.match(rule,inputJson['Mail_1'])
        if result == None:
            db.close()
            return '008'

        sql = 'insert into FiestaAccount({keys})values({values})'.format(
            keys = ','.join(map(str,keys)),
            values = ','.join(map(str,values))
        )
        try:
            cursor.execute(sql)
            db.commit()
            db.close()
            return '001'
        except:
            print("error: faild to execute sql@ " + sql)
            db.rollback()
            db.close()
            return '006'
        
    #更新會員資料(需填帳號)   
    def postUpdateData(self,inputJson):
        keys = []
        values = []
        for i in inputJson.keys():
            keys.append(i)
        for i in inputJson.values():
            values.append('null' if i is None or i == "" else '\'%s\''%i)
        if 'Tag' in keys:
            values[keys.index("Tag")] = TagModel.setTag(inputJson['Tag'])
        if 'userId' not in keys :
            return "0042"
        if 'Useable' in keys:
            return "0046"
        values[keys.index("userPassword")] = "SHA1(%s)" %values[keys.index("userPassword")]

        db = connectDB.connDB()
        cursor = db.cursor()
        sql = 'select ifnull((select id  from FiestaAccount where Useable = true and userId="%s" limit 1 ), 0);' % inputJson['userId']
        cursor.execute(sql)
        result =cursor.fetchone()
        if(result[0] == 0):
            db.close()
            return "002"
        Id = result[0]
        keys.remove('userId')
        values.remove('\''+inputJson['userId']+'\'')

        sql = 'update FiestaAccount SET {data} where Id = {id}'.format(
            data = ','.join(a+ '='+ str(b) for a,b in zip(keys,values)),
            id = Id
        )
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            db.close()
            return "006" 

        if 'Mail_1' in keys:
            sql = 'select Id from ReviewStatus where accountId = \'%s\''% Id
            cursor.execute(sql)
            reviewId = cursor.fetchone()
            sql = 'update ReviewStatus set Mail = \'{mail}\' where Id = \'{Id}\''.format(mail=inputJson['Mail_1'],Id=reviewId[0])
        try:
            cursor.execute(sql)
            db.commit()
            db.close()
            return '001'
        except:
            db.rollback()
            db.close()
            return "006" 

    #刪除會員資料(需填帳號)
    def postDeleteData(self,inputJson):
        keys = []
        for i in inputJson.keys():
            keys.append(i)
        if 'userId' not in keys:
            return "0042"
        db = connectDB.connDB()
        cursor = db.cursor()
        sql = 'select ifnull((select id  from FiestaAccount where Useable = true and userId="%s" limit 1 ), 0);' % inputJson['userId']
        cursor.execute(sql)
        Id =cursor.fetchone()
        if(Id[0] == 0):
            db.close()
            return "002"
        sql = 'update FiestaAccount set Useable = false where Id = \'%s\'' % Id[0]
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            db.close()
            return "006"
        sql = 'select Id from ReviewStatus where accountId = \'%s\''% Id[0]
        cursor.execute(sql)
        reviewId = cursor.fetchone()
        sql = 'update ReviewStatus set Useable = false where Id = \'%s\'' % reviewId[0]
        try:
            cursor.execute(sql)
            db.commit()
            db.close()
            return "001"
        except:
            db.rollback()
            db.close()
            return "006"
            
    #寄出驗證信
    def Confirm_Id(self,inputJson):
        updateDict = inputJson
        keys = []
        for i in updateDict.keys():
            keys.append(i)
        if 'userId' not in keys:
            return "0042"
        if 'type' not in keys:
            return "004C"
        db = connectDB.connDB()
        cursor = db.cursor()
        sql = 'select ifnull((select id  from FiestaAccount where Useable = true and userId="%s" limit 1 ), 0);' % updateDict['userId']
        cursor.execute(sql)
        result =cursor.fetchone()
        if(result[0] == 0):
            db.close()
            return "002"
        db.close()
        return result[0]
   
   #驗證信箱
    def Reviewstatus_Update(self,Id):
        db = connectDB.connDB()
        cursor = db.cursor()
        sql = 'select ifnull((select Id from FiestaAccount where Id="%s" limit 1 ), 0);' % Id
        cursor.execute(sql)
        ex = cursor.fetchone()
        if(ex[0] == 0):
            db.close()
            return '002'
        sql = 'select Id from ReviewStatus where accountId = \'%s\''% Id
        cursor.execute(sql)
        reviewId = cursor.fetchone()
        sql = 'update ReviewStatus set reviewStatus = True where Id = \'%s\';' % reviewId[0]
        try:
            cursor.execute(sql)
            db.commit()
            db.close()
            return "001"
        except:
            db.rollback()
            db.close()
            return '006'
        
    def getReviewStatus(self,inputJson):
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
        cursor = db.cursor()
        sql = 'select ifnull((select Id  from FiestaAccount where userId="%s" limit 1 ), 0);' % inputJson['userId']
        cursor.execute(sql)
        ex = cursor.fetchone()
        if(ex[0] == 0):
            db.close()
            return '002'
        sql = 'select reviewStatus from ReviewStatus  where accountId = \'%s\';' % ex[0]
        cursor.execute(sql)
        result = cursor.fetchone()
        db.close()
        return str(result[0])
    
    def getReviewStatusForToken(self,Id):
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
        cursor = db.cursor()
        sql = 'select reviewStatus from ReviewStatus  where accountId = \'%s\';' % Id
        cursor.execute(sql)
        result = cursor.fetchone()
        if result[0] == None or result[0] == False:
            db.close()
            return '020'
        db.close()
        return str(result[0])
    
    
    def getJoinedGroupId(self,inputJson):
        keys = []
        for i in inputJson.keys():
            keys.append(i)
        if 'authId' not in keys:
            return "0048"
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
        cursor = db.cursor()
        sql = 'select groupId,Authority,FiestaGroup.groupName,FiestaGroup.Photo,FiestaGroup.timeStatus from groupMember join FiestaGroup on GroupMember.groupId = FiestaGroup.Id where accountId = \'%s\' and GroupMember.Useable = true and FiestaGroup.Useable = true;' % inputJson['authId']
        cursor.execute(sql)
        result = cursor.fetchall()
        db.close()
        data = []
        for i in result :
            array = {
                'groupId' : str(i[0]),
                'Authority' : str(i[1]),
                'groupName' : str(i[2]),
                'Photo' : str(i[3]),
                'timeStatus' : str(i[4])
            }
            if str(i[3]) == 'None':
                array['Photo'] = str('https://imgur.com/iNGnle2.jpg')
            data.append(array)
        return data
    def getUnexpiredActId(self,inputJson):
        keys = []
        for i in inputJson.keys():
            keys.append(i)
        if 'Id' not in keys:
            return "0048"
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
        cursor = db.cursor()
        sql = 'select act_Id,act.act_Name,act.act_Description,act.startTime,act.Photo,ticketKinds,ticketStatus from unexpiredActivity as unexp join Activity as act on unexp.act_Id = act.Id where unexp.accountId = \'%s\' and unexp.Useable = true;' % inputJson['Id']
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result)==0:
            db.close()
            return '012'
        db.close()
        data = []
        for i in result :
            array = {}
            array['act_Id'] = str(i[0])
            array['act_Name'] = str(i[1])
            array['act_Description'] = str(i[2])
            startTime = time.mktime(time.strptime(str(i[3]),"%Y-%m-%d %H:%M:%S"))
            array['startTime'] = time.strftime("%Y-%m-%d %H:%M", time.localtime(startTime))
            array['Photo'] = str(i[4])
            array['ticketKinds'] = str(i[5])
            array['ticketStatus'] = str(i[6])
            data.append(array)
        return data
    
    def getSimpleData(self,inputJson):
        keys = []
        for i in inputJson.keys():
            keys.append(i)
        if 'Search' not in keys:
            return '004B'
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
        cursor = db.cursor()
        sql = 'select Id,nickName,userId,Photo from FiestaAccount where userId like \'%{search}%\';'.format(search=inputJson['Search'])
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result)==0:
            db.close()
            return '013'
        data = []
        for i in result:
            array = {
                        'Id' : str(i[0]),
                        'nickName' : str(i[1]),
                        'userId' : str(i[2]),
                        'Photo' : str(i[3])
                    }
            if str(i[3]) == 'None':
                array['Photo'] = str('https://imgur.com/iNGnle2.jpg')
            data.append(array)
        return data
    
    def getSimpleDataById(self,inputJson):
        keys = []
        for i in inputJson.keys():
            keys.append(i)
        if 'authId' not in keys:
            return '004B'
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
        cursor = db.cursor()
        sql = 'select Id,nickName,userId,Photo from FiestaAccount where Id like \'{Id}\';'.format(Id=inputJson['authId'])
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result)==0:
            db.close()
            return '013'
        data = []
        for i in result:
            array = {
                        'Id' : str(i[0]),
                        'nickName' : str(i[1]),
                        'userId' : str(i[2]),
                        'Photo' : str(i[3])
                    }
            if str(i[3]) == 'None':
                array['Photo'] = str('https://imgur.com/iNGnle2.jpg')
            data.append(array)
        return data
    
    def getCreateAct(self,inputJson):
        keys = []
        for i in inputJson.keys():
            keys.append(i)
        if 'authId' not in keys:
            return '0048'
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
        cursor = db.cursor()
        sql = 'select groupId from GroupMember where accountId = \'%s\' and Authority = 3;'%inputJson['authId']
        cursor.execute(sql)
        result = cursor.fetchall()
        if len(result)==0:
            db.close()
            return '013'
        groupId = []
        data = []
        for i in result:
            groupId.append(i[0])
        for i in groupId:
            sql = 'select Id,act_Name,groupId,act_Description,Photo,viewStatus from Activity where Useable = true and groupId=\'%s\';' % i
            cursor.execute(sql)
            result =cursor.fetchall()
            for i in result:
                array = {
                            'Id' : str(i[0]),
                            'act_Name' : str(i[1]),
                            'groupId' : str(i[2]),
                            'act_Description' : str(i[3]),
                            'Photo' : str(i[4]),
                            'viewStatus' : str(i[5])
                        }
                if str(i[4]) == 'None':
                    array['Photo'] = str('https://imgur.com/iNGnle2.jpg')
                data.append(array)
        return data
    
    #更改會員密碼
    def changePassword(self,inputJson):
        keys = []
        for i in inputJson.keys():
            keys.append(i)
        if 'userId' not in keys:
            return '0042'
        if 'userPassword' not in keys:
            return '0043'
        db = connectDB.connDB()
        cursor = db.cursor()
        sql = 'select ifnull((select Id from FiestaAccount where Id="%s" limit 1 ), 0);' % inputJson['userId']
        # print(sql)
        cursor.execute(sql)
        Id = cursor.fetchone()
        if Id[0] == 0:
            db.close()
            return '002' 
        sql = 'update FiestaAccount set userPassword = Sha1(\'{passwd}\') where Id = \'{Id}\';'.format(passwd = inputJson['userPassword'],Id = inputJson['userId'])
        try:
            cursor.execute(sql)
            db.commit()
            db.close()
            return "001"
        except:
            db.rollback()
            db.close()
            return '006'