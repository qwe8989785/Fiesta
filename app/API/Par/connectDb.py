from pymysql import connect

dbHost = 'localhost'
dbPort = 3306
dbPassword = 'kmslab'
dbName = 'Fiesta'
dbCharset = 'utf8mb4'

def connDB():
    return connect(host=dbHost, port=dbPort, user='root', passwd=dbPassword, db=dbName, charset=dbCharset)