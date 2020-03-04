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


mydb = dbConnect()
mycursor = mydb.cursor()
mycursor.execute("select distinct yearID, sum(HR), sum(AB), sum(HR) / sum(AB) as 'rate' from batting where yearID > 1970 group by yearID")
myresult = mycursor.fetchall()


table = BeautifulTable()
table.set_style(BeautifulTable.STYLE_COMPACT)
table.column_headers = ["Year", "HR", "AB", "rate"]

for x in myresult:
    table.append_row(x)
print(table)



df = pd.DataFrame(myresult, columns=['Year', 'HR', 'AB', 'rate'])

fig, ax1 = plt.subplots()

years = df['Year'].values
hr = df['rate'].values


plt.plot(years, hr, marker='o', color='red')


plt.show()























































# eof
