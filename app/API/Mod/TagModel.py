import pymysql
import re


def catchTag(tag):
    if tag == None :
        return 'None'
    digArray = re.split(r',',tag)
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    chArray = []
    for i in digArray:
        sql = 'select TagName from TagList where Id =\'%s\';' % i
        cursor.execute(sql)
        result = cursor.fetchone()
        if result == None:
            chArray.append('None')
        else:
            chArray.append(result[0])
    db.close()
    return chArray

def getTagName():
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select TagName from TagList;'
    cursor.execute(sql)
    result = []
    for i in cursor.fetchall():
        result.append(i[0])
    db.close()
    return result
def createTag(inputJson):
    key = []
    for i in inputJson.keys():
        key.append(i)
    if "TagName" not in key:
        return '004F'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select ifnull((select Id from TagList where Useable = true and TagName="%s" limit 1 ), 0);' % inputJson['TagName']
    cursor.execute(sql)
    result = cursor.fetchone()
    if result[0] != 0 :
        db.close()
        return '005'
    sql = 'insert into TagList(TagName,Useable) values(\'%s\',True);' %inputJson['TagName']
    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return '001'
    except:
        db.rollback()
        db.close()
        return '006'

#tag 轉 數字
#input " 展覽,快閃,公益 "
#return " '1,2,3' "
def setTag(tag):
    if tag == None or tag == "":
        return 'null'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    chArray = re.split(r',',tag)
    digArray = ''
    for i in range(len(chArray)):
        sql = 'select Id from TagList where TagName =\'%s\';' % chArray[i]
        cursor.execute(sql)
        if i == len(chArray)-1:
            digArray = digArray + str(cursor.fetchone()[0]) 
        else:
            digArray = digArray + str(cursor.fetchone()[0]) + ','
    db.close()
    return '\'%s\''%digArray
    
