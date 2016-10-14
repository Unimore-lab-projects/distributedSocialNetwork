from twisted.internet import reactor

from  twistar.dbconfig.base import InteractionBase
from db_insertor import *
from db_openConnection import *

# logging necessario
enable_logging()
InteractionBase.LOG = True
log.startLogging(sys.stdout)
# end logging


# apre la connessione
dbpool = open_connecton()
# istanza per i metodi di inserimento nel db
inser = DatabaseInsertor(dbpool)
inter = DatabaseInterrogator(dbpool)


# inter.get_friends().addCallback(fillFriendList)
#
# print "My posts:"
# inter.get_latets_posts(3).addCallback(donedone)

def printPostandComments(commentlist, post):
    print post.text_content
    for comment in commentlist:
        print "     %s: %s" % (comment.username, comment.content)


def printList(list):
    for post in list:
        inter.get_post_comments(post).addCallback(printPostandComments, post)


#
# def printComments(commentList):
#     Friend.all().addCallback(printList)


Post.all().addCallback(printList)
# inser.insert_my_user("ilmiousername")
# post = Post()
# inter.get_my_user().addCallback(get_my_user_id_callback).addCallback(save_my_user)
# post.user_id = my_uid
# post.text_content = "ciaociaociaociaociaociao"
# post.post_id = datetime.today()
# inser.insert_post(post).addCallback(donedone)
# inser.insert_post(None, "affanculo le callback", None).addCallback(donedone)
# comment = Comment()
# comment.content = "ciai ragggione zio"
# comment.user_id = 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'
# comment.comment_id = int(time.time())
# comment.post_id = 1476291454
#
# inser.insert_comment(comment)

# inter.get_post_comments(None, 1476291454).addCallback(donedone)

# # esempio di inserimento di un nuovo nodo nel db con un uuid gia esistente e un timestamp piu vecchio di quello attuale
# timest = datetime.today() - timedelta(minutes=15)
# # necessario per inserire un uuid
# extras.register_uuid()
# my_uuid = '4fb2fd7d-5985-4490-a9b8-ffd6a21166c5'
# inser.insert_node(None, my_uuid, '127.0.0.1', '1232', timest)
#
# from random import randint
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
# ottiene i nodi. stampa nella console la lista dei nodi presenti. per manipolare la lista di oggetti Known_nodes usare
# una callback al posto di done
# inter.get_latets_posts(1).addCallback(donedone)
# inter.get_my_user().addCallback(donedone)
##reactor. si chiude entro 5 secondi e termina
reactor.callLater(10, reactor.stop)

print('MAIN: Starting the reactor')
reactor.run()
