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
from random import randint
peer = random.randint(1,4)
dbpool = open_connection(dbname="db_peer%s" % peer, user="peer%s" % peer )
# istanza per i metodi di inserimento nel db
inser = DatabaseInsertor(dbpool)
inter = DatabaseInterrogator(dbpool)
Registry.DBPOOL = dbpool

inser.insert_post(None,text_content="bzfljgsjgjds!")

# def populateNodes():
#     for i in [1, 2, 3, 4]:
#         inter = DatabaseInterrogator(open_connection(user="peer%s" % i, dbname="db_peer%s" % i))
#         print("peer n%s" % i)
#         inter.get_known_nodes()
#
#     # inser.insert_node(user_id="e9ef0227-a8dd-40f5-b3d6-83060f2d3cb6",address="127.0.0.1",port="8001")
#     pass

#
# def ddd(pack):
#     print pack.post.text_content
#     for comment in pack.commentList:
#         print "     %s" % comment.content
#
#
# def done(res):
#     # for r in res:
#     #     r.addCallback(ddd)
#     print res

# inter.get_friend_username('0c0dde54-18f6-48c2-aedc-a01934e4200b').addCallback(done)
# populateNodes()
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
