
from twisted.enterprise import adbapi
from DbManagement.db_insertor import *

def open_connection(database,port,username,password,host):
    args=[database,port,username,password,host]
    arg_string="dbname="+str(database)+" port="+str(port)+" password="+str(password)+" host="+str(host)
    print(args)
    dbpool = adbapi.ConnectionPool("psycopg2",arg_string)

    d=DatabaseInsertor(dbpool)
    d.insert_my_user(username)
