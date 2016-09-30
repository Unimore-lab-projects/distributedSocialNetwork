from uuid import *
from twisted.internet import reactor
from twisted.enterprise import adbapi

dbpool = adbapi.ConnectionPool(
    "pgdb",
    dbname='mydatabase',
    port='5432',
    user='archeffect',
    host='localhost'
)




# user_id = uuid4()
# username = "myusername"
#
# insert_user = ("insert into my_user "
#                "( user_id, username) "
#                "values ( %s, %s )")
# #
# params = ( user_id, username)
# d = dbpool.runOperation(insert_user, params)
#
# # get_my_user = ("select "
# #                "mu.user_id,"
# #                "mu.username "
# #                "from "
# #                "my_user mu;")
#
# from query_loader import *
#
# myquery= "testqueries"
# d = dbpool.runQuery(load_query(myquery))
#
# def gotRows(rows):
#     res = "{0}".format(rows[0])
#     print res
#     return res
#
# def queryError(reason):
#     print 'Problem with the query:', reason
#
# d.addCallbacks(gotRows, queryError)
#
#
# # d.addCallback(got_result)

# manually set up the end of the process by asking the reactor to
# stop itself in 4 seconds time
reactor.callLater(4, reactor.stop)
# start up the Twisted reactor (event loop handler) manually
print('Starting the reactor')
reactor.run()
