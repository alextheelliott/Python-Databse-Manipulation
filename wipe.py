from database import *
import configparser as cParse

#LOAD CONFIG
config = cParse.ConfigParser()
config.read('settings.ini')
dbConfig = config['DATABASE']

pwc = cParse.ConfigParser()
pwc.read('password.ini')
pwConfig = pwc['DEFAULT']

dbName   = dbConfig['DBNAME']
srvHost  = dbConfig['SERVER_HOST']
port     = dbConfig['PORT']
password = pwConfig['PASSWORD']

#ESATBLISH CONNECTION TO THER SERVER
connection = createServerConnection(srvHost, port, "root", password)

#DROP DB
dropDatabase(connection, dbName)