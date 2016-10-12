import logging
from datetime import datetime, timedelta
from twistar.registry import Registry

from DbManagement.tables import *


class DatabaseInterrogator:
    def __init__(self, dbpool):
        Registry.DBPOOL = dbpool

    # my_user

    def __done_my_user(self, me):
        """Ritorna un oggetto my_user contente il proprio usename e user_id"""
        logging.debug("my username is %s " % me.username)
        logging.debug("my uuid is %s " % me.user_id)
        return me

    def get_my_user(self):
        """ottiene il primo risulato in my_user. non dovrebbero esserci altre entry"""
        me = My_user()
        return me.find(limit=1).addCallback(self.__done_my_user)

    # known_nodes

    def __done_all_nodes(self, nodes):
        """callback per get_known_nodes. Ritorna una lista di oggetti Known_node"""
        nodesDict = dict()
        for node in nodes:
            logging.debug("Node: %s address: %s port %s last updated %s" % (
                node.user_id, node.address, node.port, node.last_update))
            nodesDict[node.user_id] = node
        return nodesDict

    def get_known_nodes(self):
        """Ottiene la lista dei known nodes dal database"""
        return Known_node().all().addCallback(self.__done_all_nodes)

    # friends

    def __done_friends(self, friends):
        """ritorna una lista di oggetti Friend"""
        if len(friends) == 0:
            logging.debug("empty Friend list. so sad")
            return None
        else:
            for friend in friends:
                logging.debug("Friend: %s username %s " % (friend.user_id, friend.username))
            return friends

    def get_friends(self):
        """ottiene tutti gli amici"""
        return Friend().all().addCallback(self.__done_friends)

    # comments per post

    def __done_post_comments(self, comments, post_id):
        """ritorna un Deferred contenente la lista di commenti relativa ad un post id"""
        logging.debug("Number of comments for post_id: %s : %s " % (post_id, len(comments)))
        return comments

    def get_post_comments(self, post=None, post_id=None):
        if (post is None) & (post_id is None):
            logging.error("both arguments are None")
            return False
        if post is not None:
                post_id = post.post_id
        """ottiene i commenti di un dato post id"""
        return Comment.find(where=['post_id = ?', post_id]).addCallback(self.__done_post_comments, post_id)

    # posts negli ultimi x giorni

    def get_latets_posts(self, days):
        """ottiene la lista di post negli ultimi giorni"""
        delta = datetime.today() - timedelta(days)
        unix_time = delta.strftime("%s")
        from twisted.python import log
        return Post.find(where=['post_id > ?', unix_time])\
            # .addCallbacks(self.__done_latest_posts, log.err)

    # username del friend

    def __done_username(self, result):
        return result.username

    def get_friend_username(self, user_id):
        return Friend.find(where=['user_id = ?', user_id], limit=1).addCallback(self.__done_username)