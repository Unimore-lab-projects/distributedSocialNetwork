from twisted.internet import reactor

from twistar.dbconfig.base import InteractionBase
from db_insertor import *
from db_openConnection import *

from twisted.enterprise import adbapi
from twistar.registry import Registry

# logging necessario
enable_logging()
# InteractionBase.LOG = True
log.startLogging(sys.stdout)
# end logging


# apre la connessione
dbpool = open_connecton()
# istanza per i metodi di inserimento nel db
inser = DatabaseInsertor(dbpool)
inter = DatabaseInterrogator(dbpool)

Registry.DBPOOL = dbpool


def done(result):
    print result

inter.get_post_and_comments(5).addCallback(done)

##reactor. si chiude entro 5 secondi e termina
reactor.callLater(10, reactor.stop)

print('MAIN: Starting the reactor')
reactor.run()
