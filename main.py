from twistar.dbconfig.base import InteractionBase
from twisted.internet import reactor
from twisted.python import log

from db_insertor import *
from db_openConnection import *
from debug_messages import *


# generic callback
# def printData(node):
#     pass


# logging
enable_logging()
InteractionBase.LOG = True
log.startLogging(sys.stdout)
# end logging

# dbpool = open_connecton()
# inter = DatabaseInterrogator(dbpool)
inser = DatabaseInsertor(open_connecton())
inser.insert_my_user("myusername")


# inter.get_my_user().addCallback(printData)

reactor.callLater(2, reactor.stop)

print('MAIN: Starting the reactor')
reactor.run()
