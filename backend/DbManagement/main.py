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
dbpool = open_connection(dbname="db_peer4", user="peer4")
# istanza per i metodi di inserimento nel db
inser = DatabaseInsertor(dbpool)
inter = DatabaseInterrogator(dbpool)
Registry.DBPOOL = dbpool

def populateNodes():
    for i in range(1, 5):
        # inserisce 4 utenti nei rispettivi db
        inser = DatabaseInsertor(open_connection(user="peer%s" % i, dbname="db_peer%s" % i))
        inser.insert_my_user("peer%s" % i)


def ddd(pack):
    print pack.post.text_content
    for comment in pack.commentList:
        print "     %s" % comment.content


def done(res):
    for r in res:
        r.addCallback(ddd)



# dbpool = open_connecton(dbname="db_peer3",user="peer3")

# inter.get_post_pack('1476291454').addCallback(done)
# inter.get_recents(10).addCallback(done)
# inter.get_recents(10).addCallback(done)
# d = defer.maybeDeferred(inter.get_recents, 10).addCallback(done)
# reactor.callLater(2, d.addCallback, done)
# inser.insert_my_user("peer1").addCallback(done)


# inser.insert_post(None, "post del giorno!")

##reactor. si chiude entro 10 secondi e termina
reactor.callLater(10, reactor.stop)

print('MAIN: Starting the reactor')
reactor.run()
