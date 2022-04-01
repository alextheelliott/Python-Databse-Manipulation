from ast import parse
import mysql.connector
from mysql.connector import Error
#import pandas as pd
import csv

#
# https://www.freecodecamp.org/news/connect-python-with-sql/
#

#
# Generates a create table query
#
def createTableQueryFromCSV(file, tbName):
    ret = 'CREATE TABLE ' + tbName + ' ('
    with open(file) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for val in row:
                ret += val + ' '
            ret = ret[:-1] + ', '
    ret = ret[:-2] + ');'
    return ret

#
# Generates a populate table query
#
def createPopQueryFromCSV(file, tbName):
    ret = 'INSERT INTO ' + tbName + ' VALUES '
    with open(file) as csvfile:
        reader = csv.reader(csvfile);
        next(reader) #Skip header
        for row in reader:
            ret += '('
            for val in row:
                #Gross string manpipulation sorry TODO rewrite
                newVal = ''.join(filter(str.isalnum or str == ' ' or str == '/', val))
                newVal = (newVal if newVal!='' else 'NULL').replace('/', '-')
                newVal = (newVal if (newVal.isnumeric() or newVal == 'NULL') else ('\''+newVal.strip()+'\'')) + ','
                ret += newVal
            ret = ret[:-1] + '), '
    ret = ret[:-2] + ';'
    return ret
    # Load CSV from file:
    # ret = 'LOAD DATA LOCAL INFILE \'' + file + '\' INTO TABLE ' + tbName + """ FIELDS TERMINATED BY ',' 
    #     ENCLOSED BY '"' LINES TERMINATED BY '\\n' IGNORE 1 ROWS;"""
    # return ret

#
# MAKE
#
def createReadQuery():
    return

#
# Establishes a connection to an SQL Servor
#
def createServerConnection(host_name, port_num, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            port=port_num
        )
        print("MySQL Server connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

#
# Creates a database on an establised connection
#
def createDatabase(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print('Database: {' + query + '} created successfully')
    except Error as err:
        print(f"Error: '{err}'")

#
# Drops a database on an establised connection
#
def dropDatabase(connection, databaseName):
    cursor = connection.cursor()
    try:
        cursor.execute("DROP DATABASE " + databaseName + ";")
        print("Database dropped successfully")
    except Error as err:
        print(f"Error: '{err}'")

#
# Established a connection to a database on a server (modified create_server_connection())
#
def createDBConnection(host_name, port_num, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            port=port_num
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

#
# Executes a query on an established database connection
#
def executeQuery(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

#
# Reads a query on an established database connection
#
def readQuery(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")