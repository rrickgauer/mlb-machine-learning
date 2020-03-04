import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mysql.connector
import json
from os import path
import getpass
from beautifultable import BeautifulTable

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

def space(numSpaces = 1):
    for x in range(numSpaces):
        print('')


def getTable(columns, data):
    table = BeautifulTable(max_width=1000)
    # table.set_style(BeautifulTable.STYLE_COMPACT)
    table.column_headers=columns
    for row in data:
        table.append_row(row)

    table.column_alignments = BeautifulTable.ALIGN_LEFT
    return table



mydb = dbConnect()
mycursor = mydb.cursor()
sql = "select people.playerID, people.nameFirst, people.nameLast, sum(pitching.stint) as stint, sum(pitching.W), sum(pitching.L), sum(pitching.G), sum(pitching.H), sum(pitching.ER), sum(pitching.HR), sum(pitching.BB), sum(pitching.SO) from people, pitching, halloffame where people.playerID=halloffame.playerID and people.playerID=pitching.playerID and halloffame.inducted='y' GROUP by people.playerID"
mycursor.execute(sql)
myresult = mycursor.fetchall()


columns = []
columns.append('PlayerID')
columns.append('First')
columns.append('Last')
columns.append('Stint')
columns.append('W')
columns.append('L')
columns.append('G')
columns.append('H')
columns.append('ER')
columns.append('HR')
columns.append('BB')
columns.append('SO')




print(getTable(columns, myresult))





















































# eof
