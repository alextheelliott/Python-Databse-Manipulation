from database import *
import configparser as cParse
import os

#
# TODO
# Learn to host SQL server on docker: https://hub.docker.com/_/mysql -- done
# Then test csv methods -- done
# gitignore password ini -- not done
# create a wipe script
#

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
dataFold = dbConfig['DATA_FOLD']

#ESATBLISH CONNECTION TO THER SERVER
connection = createServerConnection(srvHost, port, "root", password)

#CREATE THE DATABASE ON THE SERVER
createDatabaseQuery = "CREATE DATABASE " + dbName
createDatabase(connection, createDatabaseQuery)

#ESTABLISH CONNECTION WITH THE DATABASE
connection = createDBConnection(srvHost, port, "root", password, dbName)

#GET THE DIR OF ALL THE DATA NEEDING TO BE PUSHED
curDir = os.getcwd();
headFiles = os.listdir(curDir + '//' + headFold);
dataFiles = os.listdir(curDir + '//' + dataFold);

#SETUP THE DATA BY EXECUTING QUARIES
for headFile in headFiles:
    createTableQuery = createTableQueryFromCSV(headFold + '\\' + headFile, headFile.split('.')[0])
    executeQuery(connection, createTableQuery)

for dataFile in dataFiles:
    popTableQuery = createPopQueryFromCSV(dataFold + '\\' + dataFile, dataFile.split('.')[0])
    executeQuery(connection, popTableQuery)