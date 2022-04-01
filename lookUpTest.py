from database import *
import configparser as cParse
import os

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
headFold = dbConfig['HEAD_FOLD']

#ESTABLISH CONNECTION WITH THE DATABASE
connection = createDBConnection(srvHost, port, "root", password, dbName)

#GET THE DIR OF ALL THE DATA NEEDING TO BE PUSHED
curDir = os.getcwd();
headFiles = os.listdir(curDir + '//' + headFold);

#SETUP THE DATA BY EXECUTING QUARIES
for headFile in headFiles:
    print(readQuery(connection, 'SELECT * FROM ' + headFile.split('.')[0] + " WHERE breed1='Husky';"))