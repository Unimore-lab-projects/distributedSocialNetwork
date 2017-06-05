# -*- coding: utf-8 -*
import random
import time
from uuid import uuid4

from psycopg2 import extras, extensions
from twisted.internet import defer, reactor

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

    def __done(self):
        return My_user.find(limit=1)

    def __user_done(self, user):
        if len(user.errors) > 0:
            logging.error(user.errors)
            return None
        # return My_user.find(limit=1)
        d = defer.Deferred()
        logging.debug("FROM insert_my_user: my user created")
        return reactor.callLater(2, d.addCallback, self.__done)

    def __check_existence(self, my_user, name):
        """se non esiste lo crea."""
        if my_user is None:
            extras.register_uuid()
            uid = uuid4()
            extensions.adapt(uid).getquoted()
            me = My_user(user_id=uid, username=name)
            logging.debug("FROM insert_my_user: my user not existing. creating.")
            return me.save().addCallbacks(self.__user_done, log.err)
        else:
            logging.debug("FROM insert_my_user: user already existing")
            return my_user

    def insert_my_user(self, name):
        """controlla se esiste già un utente"""
        logging.debug("FROM insert_my_user: inserting my username: %s generating uuid" % name)
        return My_user.find(limit=1).addCallback(self.__check_existence, name)

    # INSERT O UPDATE di un NODE

    def __node_created(self, node):
        if len(node.errors) > 0:
            logging.error('FROM insert_node: %s errors in node creation' % len(node.errors))
            logging.error(node.errors)
        else:
            logging.debug("FROM insert_node: Node created. uuid is %s and address is %s : %s" % (
                node.user_id, node.address, node.port))

    def __node_updated(self, node):
        if len(node.errors) > 0:
            logging.error('FROM insert_node: %s errors in node update' % len(node.errors))
            logging.error(node.errors)
        else:
            logging.debug("FROM insert_node: Node updated. uuid is %s and address is %s : %s" % (
                node.user_id, node.address, node.port))

    def __update_node(self, node, username, user_id, address, port, last_update):
        if node is None:
            logging.debug("FROM insert_node: creating a new node")
            # node doesn't exists
            node = Known_node()
            node.username = username
            node.user_id = user_id
            node.address = address
            node.port = port
            node.last_update = datetime.today()
            node.save().addCallback(self.__node_created)
        else:
            if node.last_update < last_update:
                logging.debug(
                    "FROM insert_node: updating existing node %s new timestamp is %s" % (
                        node.user_id, node.last_update))
                attrs = {'address': address, 'port': port, 'last_update': last_update}
                node.updateAttrs(attrs)
                node.save().addCallback(self.__node_updated)
            else:
                logging.debug("FROM insert_node: existing is already the most recent update")

    def insert_node(self, node=None, username=None, user_id=None, address=None, port=None, last_update=None):
        if node is None:
            Known_node.find(where=['user_id=?', user_id], limit=1).addCallback(self.__update_node, username, user_id,
                                                                               address,
                                                                               port,
                                                                               last_update)
        else:
            # if Node != None use it
            Known_node.find(where=['user_id=?', node.user_id], limit=1).addCallback(self.__update_node, node.user_id,
                                                                                    node.username,
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
        post.post_id = int(str(int(time.time())) + str(random.randint(0, 99999)))
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

    def insert_comment(self, comment=None, post_id=None, user_id=None, username=None, content=None):
        if comment is None:
            comment = Comment()
            comment.post_id = post_id
            comment.user_id = user_id
            comment.username = username
            comment.content = content

        comment.isValid().addCallback(self.__check_comment, comment)

        self.d = defer.Deferred()
        self.d = Post.find(where=['post_id=?', comment.post_id], limit=1).addCallback(self.__post_found, comment)
        return self.d
