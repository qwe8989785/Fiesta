# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 00:06:33 2020

@author: user
"""
import math
def LLC(km,Lat):
    La_distance = km / 110.574
    Lo_distance = km / (111.320*math.cos(Lat*math.pi/180))
    return(La_distance,Lo_distance)

def test():
    i = 10.153 - 100
    print(i)

def getRecommendAct(inputJson):
    keys = []
    for i in inputJson.keys():
        keys.append(i)
    if "authId" not in keys:
        return '0048'
    db = pymysql.connect(host='localhost', port=3306, user='root', passwd='Skills39', db='Fiesta', charset='utf8mb4')
    cursor = db.cursor()
    sql = 'select Latitude,Longitude,Distance,Tag from FiestaAccount where Id = \'%s\';' % inputJson['authId']
    cursor.execute(sql)
    if len(cursor.fetchone()) == 0:
        return '014'
    Lat = cursor.fetchone()[0]
    Lon = cursor.fetchone()[1]
    Km_Dis = cursor.fetchone()[2]
    Tag = cursor.fetchone()[3]
    sql = 'SHOW COLUMNS FROM Activity'
    cursor.execute(sql)
    title = []
    for i in cursor.fetchall():
        title.append(i[0])
    La_dis = Km_Dis / 110.574
    Lo_dis = Km_Dis / (111.320*math.cos(Lat*math.pi/180))
    sql = 'select * from Activity where Latitude < {bigLat} or Latitude > {smallLat} or Longitude < {bigLon} or Longitude > {smallLon} limit 50;'.format(bigLat=Lat+La_dis,samllLat=Lat-La_dis,bigLon=Lon+Lo_dis,smallLon=Lon-Lo_dis)
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
            else:    
                array[title[j]] = str(result[i][j])
        data.append(array)
    return data

test()
    