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
mycursor.execute("SELECT yearID, HR, AB, G, RBI, H from batting where playerID='bondsba01'")
myresult = mycursor.fetchall()




table = BeautifulTable()
table.set_style(BeautifulTable.STYLE_COMPACT)
table.column_headers = ["Year", "HR", "AB", "G", "RBI", "H"]

for x in myresult:
    table.append_row(x)
print(table)



df = pd.DataFrame(myresult, columns=['Year', 'HR', 'AB', 'G', 'RBI', 'H'])

fig, ax1 = plt.subplots()

years = df['Year'].values
hr = df['HR'].values
ab = df['AB'].values
g = df['G'].values
rbi = df['RBI'].values
h = df['H'].values

ax1.plot(years, hr, label='HR', marker='o', color='blue', alpha=0.5)

ax1.set_xticks(np.arange(min(years), max(years)+1, 1))
ax1.set_xticklabels(np.arange(min(years), max(years)+1, 1), rotation=45)


ax2 = ax1.twinx()
ax2.plot(years, ab, label='AB', marker='o', color='red', alpha=0.5)

ax3 = ax1.twinx()
ax3.plot(years, g, label='G', marker='o', color='green', alpha=0.5)

ax4 = ax1.twinx()
ax4.plot(years, rbi, label='RBI', marker='o', color='gold', alpha=0.5)

ax5 = ax1.twinx()
ax5.plot(years, h, label='H', marker='o', color='purple', alpha=0.5)


plt.yticks([])


fig.legend()
fig.suptitle('Hank Aaron Batting Stats')
plt.show()























































# eof
