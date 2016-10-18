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


def ddd(pack):
    print pack.post.text_content
    for comment in pack.commentList:
        print "     %s" % comment.content


def done(res):
    for r in res:
        r.addCallback(ddd)


# inter.get_post_pack('1476291454').addCallback(done)
# inter.get_recents(10).addCallback(done)
inter.get_recents(10).addCallback(done)
# d = defer.maybeDeferred(inter.get_recents, 10).addCallback(done)
# reactor.callLater(2, d.addCallback, done)

# inser.insert_post(None, "post del giorno!")

##reactor. si chiude entro 5 secondi e termina
reactor.callLater(10, reactor.stop)

print('MAIN: Starting the reactor')
reactor.run()
