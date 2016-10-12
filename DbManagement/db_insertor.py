# -*- coding: utf-8 -*
import time
from uuid import uuid4

from psycopg2 import extras
from twisted.python import log

from db_interrogator import *
from debug_messages import *


class DatabaseInsertor:
    def __init__(self, dbpool):
        self.dbpool = dbpool
        Registry.DBPOOL = dbpool
        # logging necessario
        # enable_logging()
        # InteractionBase.LOG = True
        # log.startLogging(sys.stdout)
        # end logging

    # INSERT USER

    def __user_done(self, user):
        if len(user.errors) > 0:
            logging.error('%s errors in user creation' % len(user.errors))
            logging.error(user.errors)
        else:
            logging.debug("My user created. uuid is %s and username is %s" % (user.user_id, user.username))

    def __check_existence(self, user_exists, name):
        """se non esiste lo crea."""
        if user_exists == 0:
            extras.register_uuid()
            me = My_user(user_id=uuid4(), username=name)
            me.save().addCallbacks(self.__user_done, log.err)
        else:
            logging.debug("user already existing")

    def insert_my_user(self, name):
        """controlla se esiste già un utente"""
        My_user.count().addCallback(self.__check_existence, name)

    # INSERT O UPDATE di un NODE

    def __node_created(self, node):
        if len(node.errors) > 0:
            logging.error('%s errors in node creation' % len(node.errors))
            logging.error(node.errors)
        else:
            logging.debug("Node created. uuid is %s and address is %s : %s" % (node.user_id, node.address, node.port))

    def __node_updated(self, node):
        if len(node.errors) > 0:
            logging.error('%s errors in node update' % len(node.errors))
            logging.error(node.errors)
        else:
            logging.debug("Node updated. uuid is %s and address is %s : %s" % (node.user_id, node.address, node.port))

    def __update_node(self, node, user_id, address, port, last_update):
        if node is None:
            # node doesn't exists
            node = Known_node()
            node.user_id = user_id
            node.address = address
            node.port = port
            node.last_update = datetime.today()
            node.save().addCallback(self.__node_created)
        else:
            if node.last_update < last_update:
                attrs = {'address': address, 'port': port, 'last_update': last_update}
                node.updateAttrs(attrs)
                node.save().addCallback(self.__node_updated)
            else:
                logging.debug("nodo inserito piu vecchio di quello già esistente")

    def insert_node(self, node=None, user_id=None, address=None, port=None, last_update=None):
        if node is None:
            Known_node.find(where=['user_id=?', user_id], limit=1).addCallback(self.__update_node, user_id, address,
                                                                               port,
                                                                               last_update)
        else:
            # if Node != None use it
            Known_node.find(where=['user_id=?', node.user_id], limit=1).addCallback(self.__update_node, node.user_id,
                                                                                    node.address, node.port,
                                                                                    node.last_update)

    def insert_node_list(self, node_list):
        for node in node_list:
            self.insert_node(node)

    # INSERT A FRIEND
    def __done_save_friend(self, result):
        if len(result.errors) > 0:
            logging.error('%s errors adding a friend:' % len(result.errors))
            logging.error(result.errors)
            return False
        else:
            logging.debug("friend added. uuid is %s and username is %s" % (result.user_id, result.username))
            return True

    def __friend_found(self, result, friend):
        if result is None:
            logging.debug("creating friend")
            friend.save().addCallback(self.__done_save_friend)
        else:
            logging.debug("friend already existing. exiting")
            return True

    def __node_found(self, node, friend):
        if node is None:
            # nodo non trovato
            logging.debug("Nodo sconosciuto")
            return False
        else:
            Friend.find(where=['user_id=?'], limit=1).addCallback(self.__friend_found, friend)

    def insert_friend(self, friend):
        """Ritorna False se il nodo non è stato trovato"""
        from twisted.internet import defer
        self.d = defer.Deferred()
        self.d = Known_node.find(where=['user_id=?', friend.user_id], limit=1).addCallback(self.__node_found, friend)
        return self.d

    # INSERT A POST

    def __done_save_post(self, post):
        if len(post.errors) > 0:
            logging.error('%s errors adding a post:' % len(post.errors))
            logging.error(post.errors)
            return False
        else:
            logging.debug("post added. post_id is %s" % post.post_id)
            return True

    def __save_new_post(self, my_user, text_content, path_to_imagefile):
        post = Post()
        post.user_id = my_user.user_id
        post.post_id = int(time.time())
        post.text_content = text_content
        post.path_to_imagefile = path_to_imagefile
        return post.save().addCallback(self.__done_save_post)

    def insert_post(self, post=None, text_content=None, path_to_imagefile=None):
        if post is None:
            if (text_content is None) & (path_to_imagefile is None):
                logging.error("il post non può essere vuoto")
                return False
            else:
                inter = DatabaseInterrogator(self.dbpool)
                return inter.get_my_user().addCallback(self.__save_new_post, text_content, path_to_imagefile)
        else:
            return post.save().addCallback(self.__done_save_post)

    # INSERT A COMMENT

    def __done_save_comment(self, comment):
        if len(comment.errors) > 0:
            logging.error('%s errors adding a comment:' % len(comment.errors))
            logging.error(comment.errors)
            return False
        else:
            logging.debug("comment added. comment_id is %s" % comment.comment_id)
            return True

    def __post_found(self, post, comment):
        if post is None:
            # post non trovato
            logging.debug("Post sconosciuto")
            return False
        else:
            logging.debug("Corresponding post found: %s" % post.post_id)
            return comment.save().addCallback(self.__done_save_comment)

    def __check_comment(self, result, comment):
        if not result:
            print "comment %s is not valid" % comment.comment_id
            return False

    def insert_comment(self, comment):
        comment.isValid().addCallback(self.__check_comment, comment)
        from twisted.internet import defer
        self.d = defer.Deferred()
        self.d = Post.find(where=['post_id=?', comment.post_id], limit=1).addCallback(self.__post_found, comment)
        return self.d
