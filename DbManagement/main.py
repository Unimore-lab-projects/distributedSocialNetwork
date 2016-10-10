from twistar.dbconfig.base import InteractionBase
from twisted.internet import reactor
from twisted.python import log

from db_insertor import *
from db_openConnection import *
from debug_messages import *
from random import randint
from datetime import datetime

# generic callback
def done(nodes):
    pass


# logging necessario
enable_logging()
InteractionBase.LOG = True
log.startLogging(sys.stdout)
# end logging

# apre la connessione
dbpool = open_connecton()

# istanza per i metodi di inserimento nel db
inser = DatabaseInsertor(dbpool)

# # esempio di inserimento di un nuovo nodo nel db con un uuid gia esistente e un timestamp piu vecchio di quello attuale
# timest = datetime.today() - timedelta(minutes=15)
# # necessario per inserire un uuid
# extras.register_uuid()
# my_uuid = '4fb2fd7d-5985-4490-a9b8-ffd6a21166c5'
# inser.insert_node(None, my_uuid, '127.0.0.1', '1232', timest)

# list = []
# for i in range(0,5):
#     extras.register_uuid()
#     node = Known_node()
#     node.user_id = uuid4()
#     node.address = '127.0.0.1'
#     node.port = randint(1200, 1300)
#     node.last_update = datetime.today()
#     list.append(node)
#
# inser.insert_node_list(list)
# istanza per i metodi di interrogazione del db
inter = DatabaseInterrogator(dbpool)
# ottiene i nodi. stampa nella console la lista dei nodi presenti. per manipolare la lista di oggetti Known_nodes usare
# una callback al posto di done
inter.get_known_nodes().addCallback(done)

##reactor. si chiude entro 5 secondi e termina
reactor.callLater(5, reactor.stop)

print('MAIN: Starting the reactor')
reactor.run()
