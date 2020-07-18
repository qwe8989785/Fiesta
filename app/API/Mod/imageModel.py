import requests
import pymysql
from imgurpython import ImgurClient
from io import BytesIO
clientId = '7a079904d23239a'
clientSecret = 'c29ce278d7c884058ff83d77182c25148c979bab'
accessToken = '52c58567ee1a5109e5f0765b3c0c0fe65f82051e'
refreshToken ='516c9ed14c2dc7dbe37df03dca82f2e17e3eba6c'

def uploadAuthImg(img,authId):
    client = ImgurClient(clientId, clientSecret, accessToken, refreshToken)
    config = {
        'album': '2ZZsszJ',
        'name': 'auth',
        'title': 'auth',
        'description': 'auth'
    }
    config['name'] = config['name'] +'_' + str(authId)
    imgIo = BytesIO()
    imgIo.write(img.read())
    imgIo.seek(0)
    image = client.upload(imgIo, config=config, anon=False)
    if image != None:
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
        cursor = db.cursor()
        sql = 'update FiestaAccount set Photo =\'{url}\' where Id = {Id};'.format(url = image['link'],Id = authId)
        try:
            cursor.execute(sql)
            db.commit()
            db.close()
            return "001"
        except:
            db.rollback()
            db.close()
            return '006'
    else:
        return '015'
    

def uploadActImg(img,actId):
    client = ImgurClient(clientId, clientSecret, accessToken, refreshToken)
    config = {
        'album': 'qIc3rOk',
        'name': 'act',
        'title': 'act',
        'description': 'act'
    }
    config['name'] = config['name'] +'_' + str(actId)
    imgIo = BytesIO()
    imgIo.write(img.read())
    imgIo.seek(0)
    image = client.upload(imgIo, config=config, anon=False)
    if image != None:
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
        cursor = db.cursor()
        sql = 'update Activity set Photo =\'{url}\' where Id = {Id};'.format(url = image['link'],Id = actId)
        try:
            cursor.execute(sql)
            db.commit()
            db.close()
            return "001"
        except:
            db.rollback()
            db.close()
            return '006'
    else:
        return '015'


def uploadGroupImg(img,groupId):
    client = ImgurClient(clientId, clientSecret, accessToken, refreshToken)
    config = {
        'album': 'OBabzii',
        'name': 'group',
        'title': 'group',
        'description': 'group'
    }
    config['name'] = config['name'] +'_' + str(groupId)
    imgIo = BytesIO()
    imgIo.write(img.read())
    imgIo.seek(0)
    image = client.upload(imgIo, config=config, anon=False)
    if image != None:
        db = pymysql.connect(host='localhost', port=3306, user='root', passwd='kmslab', db='Fiesta', charset='utf8mb4')
        cursor = db.cursor()
        sql = 'update FiestaAccount set Photo =\'{url}\' where Id = {Id};'.format(url = image['link'],Id = groupId)
        try:
            cursor.execute(sql)
            db.commit()
            db.close()
            return "001"
        except:
            db.rollback()
            db.close()
            return '006'
    else:
        return '015'
    
