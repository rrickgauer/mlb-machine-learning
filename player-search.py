import mysql.connector
import json
from os import path
from utilities import Utilities as util
import argparse

# add command line arguments
def setArgs():
    parser = argparse.ArgumentParser(description="Search database for a player ID by first and last name")
    parser.add_argument('-f', '--first', help="First name")
    parser.add_argument('-l', '--last', help="Last name")
    args = parser.parse_args()
    return args

def getResults(first, last):
    mysqlData = getMySqlData()
    mydb = mysql.connector.connect(
      host     = mysqlData['host'],
      user     = mysqlData['user'],
      passwd   = mysqlData['password'],
      database = mysqlData['database']
    )

    sql = "select playerID, nameFirst, nameLast, debut from people where nameFirst like %s and nameLast like %s order by nameLast asc, nameFirst asc limit 50"
    mycursor = mydb.cursor()
    mycursor.execute(sql, (first, last))
    myresult = mycursor.fetchall()
    return myresult

def getMySqlData():
    # create new config file if one does not exist in the local directory
    if not path.exists('.mysql-info.json'): createNewMysqlFile()

    with open(".mysql-info.json") as f:
        mysqlData = json.loads(f.read())

    return mysqlData

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

def getNames(args):
    return (getParameter(args.first), getParameter(args.last))

def getParameter(p):
    return '%' + p + '%' if p != None else '%%'

########################################  MAIN  #####################################################
args = setArgs()


# get the values for first and last
first, last = getNames(args)
results = getResults(first, last)


util.space()
table = util.getTable(results, ['PlayerID', 'First', 'Last', 'Debut'])
print(table)
