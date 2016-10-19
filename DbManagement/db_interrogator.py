# -*- coding: utf-8 -*
import logging
from collections import namedtuple
from datetime import datetime, timedelta
from twisted.internet import defer
from tables import *
from twisted.python import log


class DatabaseInterrogator:
    def __init__(self, dbpool):
        Registry.DBPOOL = dbpool

    # my_user

    def __done_my_user(self, me):
        logging.debug("my username is %s " % me.username)
        logging.debug("my uuid is %s " % me.user_id)
        return me

    def get_my_user(self):
        """
        ottiene il primo risulato in my_user. non devono esserci altre entry
        :return: oggetto My_user
        """
        me = My_user()
        return me.find(limit=1).addCallback(self.__done_my_user)

    # known_nodes

    def __done_all_nodes(self, nodes, my_user):
        nodesDict = dict()
        for node in nodes:
            logging.debug("Node: %s address: %s port %s last updated %s" % (
                node.user_id, node.address, node.port, node.last_update))
            if my_user is not None:
                if my_user.user_id == node.user_id:
                    continue
            nodesDict[node.user_id] = node
        return nodesDict

    def get_known_nodes(self, my_user=None):
        """
        Ottiene la lista dei nodi conosciuti
        :param my_user: se è None allora ritorna tutti i nodi, altrimenti esclude dal dizionario questo nodo
        :return: un dizionario di nodi conosciuti
        """
        return Known_node().all().addCallback(self.__done_all_nodes, my_user)

    # get a single node from uuid

    def get_node(self, user_id):
        """
        Metodo per ottenere l'oggetto nodo a partire dall'user_id
        :param user_id: uuid del nodo
        :return: ritorna un singolo oggetto Known_node
        """
        return Known_node().find(where=['user_id = ?', user_id], limit=1)

    # friends

    def __done_friends(self, friends):
        if len(friends) == 0:
            logging.debug("empty Friend list. so sad")
            return None
        else:
            for friend in friends:
                logging.debug("Friend: %s username %s " % (friend.user_id, friend.username))
            return friends

    def get_friends(self):
        """
        ottiene tutti gli amici
        :return: lista di deferred contentnte oggetti Friend
        """
        return Friend().all().addCallback(self.__done_friends)

    # controllo se user_id e tra amici

    def check_friend(self, user_id):
        return Friend().exists(where=['user_id = ?', user_id])

    # comments per post

    def __done_post_comments(self, comments, post_id):
        logging.debug("Number of comments for post_id: %s : %s " % (post_id, len(comments)))
        return comments

    def get_post_comments(self, post=None, post_id=None):
        """
        ottiene i commenti di un dato post id
        :param post: oggetto Post. se viene lasciato a None, deve essere presente post_id
        :param post_id: id del post
        :return: ritorna una lista di Deferred contenente i commenti relativi al post
        """
        if (post is None) & (post_id is None):
            logging.error("both arguments are None")
            return False
        if post is not None:
            post_id = post.post_id
        return Comment.find(where=['post_id = ?', post_id]).addCallback(self.__done_post_comments, post_id)

    # posts negli ultimi x giorni

    def get_latets_posts(self, days):
        """
        ottiene la lista di post negli ultimi giorni
        :param days: giornia cui si vuole far risalire la ricerca
        :return: Ritorna una lista di Deferred contententi i post degli ultimo giorni
        """
        delta = datetime.today() - timedelta(days)
        unix_time = delta.strftime("%s")
        return Post.find(where=['post_id > ?', unix_time]) \
            # .addCallbacks(self.__done_latest_posts, log.err)

    # username del friend

    def __done_username(self, result):
        return result.username

    def get_friend_username(self, user_id):
        """
        Ottiene l'username del friend a partire dall'user_id
        :param user_id: uuid utente
        :return: ritorna una stringa contenente l'username
        """
        return Friend.find(where=['user_id = ?', user_id], limit=1).addCallback(self.__done_username)

    # get a single post and his comments

    def __create_package(self, comments, post):
        packa = PostPackage(post, comments)
        # logging.debug(packa)
        return defer.succeed(packa)

    def __get_comments(self, post):
        return self.get_post_comments(post, None).addCallback(self.__create_package, post)

    def get_post_pack(self, post_id):
        """
        ottiene il Post ed i commenti ad esso collegati
        :param post_id: id numerico del post
        :return: ritorna un oggetto PostPackage relativo al post_id immesso
        """
        return Post.find(where=['post_id = ?', post_id], limit=1).addCallback(self.__get_comments)

    # get all post and their comments

    def __process_posts(self, post_list):
        pack_list = []
        for post in post_list:
            pack_list.append(self.get_post_pack(post.post_id))
        logging.debug("returning pack list: %s " % pack_list)
        return pack_list

    def get_recents(self, days):
        """
        ottiene la lista di post e relativi commenti negli ultimi giorni

        :returns una lista di oggetti PostPackage. uno per ogni post e relativi commenti
        """
        return self.get_latets_posts(days).addCallback(self.__process_posts)


class PostPackage(pb.Copyable):
    def __init__(self, post=None, commentList=None):
        self.post = post
        self.commentList = commentList

    def setPost(self, post):
        self.post = post

    def setComments(self, commentList):
        self.commentList = commentList

    def getPost(self):
        return self.post

    def getComments(self):
        return self.commentList
