import matplotlib as plt
import mysql.connector
import json
from os import path
import getpass

def createNewMysqlFile():
    configFileUserInput = getUserMysqlInfoDict()

    # convert to json
    y = json.dumps(configFileUserInput)

    # write data to the config file
    with open(".mysql-info.json", "w") as newConfigFile:
        newConfigFile.write(y)

def getUserMysqlInfoDict():
    configFileUserInput = {
        "user"     : input('User: '),
        "host"     : input('Host: '),
        "database" : input('Database: '),
        "password" : getpass.getpass(),
    }

    return configFileUserInput

def dbConnect():
    # create new config file if one does not exist in the local directory
    if not path.exists('.mysql-info.json'):
        createNewMysqlFile()

    with open(".mysql-info.json") as f:
        mysqlData = json.loads(f.read())

    mydb = mysql.connector.connect(
      host     = mysqlData['host'],
      user     = mysqlData['user'],
      passwd   = mysqlData['password'],
      database = mysqlData['database']
    )

    return mydb


mydb = dbConnect()
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM people where playerID='aaronha01'")
myresult = mycursor.fetchall()

for x in myresult:
  print(x)



































































# eof
