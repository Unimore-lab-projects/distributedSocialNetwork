from twisted.enterprise import adbapi


def open_connection(dbname="db_peer1", port='5432', user='peer1', host='localhost'):
    dbpool = adbapi.ConnectionPool(
        "psycopg2",
        dbname=dbname,
        port=port,
        user=user,
        host=host)

    return dbpool


# def openConnectionOnDB(database, port, username, password, host):
#     args = [database, port, username, password, host]
#     arg_string = "dbname=" + str(database) + " port=" + str(port) + " password=" + str(password) + " host=" + str(host)
#     print(args)
#     dbpool = adbapi.ConnectionPool("psycopg2", arg_string)
#
#     return dbpool
