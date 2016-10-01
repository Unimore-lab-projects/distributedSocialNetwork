# -*- coding: utf-8 -*
import time
from uuid import uuid4

from db_interrogator import *


class DatabaseInsertor:
    def __init__(self, dbpool):
        __my_id = None
        Registry.DBPOOL = dbpool
        inter = DatabaseInterrogator(dbpool)
        inter.get_my_user().addCallback(self.__done_my_user)

    def __self_done_my_user(self, me):
        self.__my_id = me.user_id

    def __user_done(self, user):
        if len(user.errors) > 0:
            print '%s errors in user creation' % len(user.errors)
            print user.errors
        else:
            logging.debug("My user created. uuid is %s and username is %s" % (user.user_id, user.username))

    def insert_my_user(self, name):
        """Inserisce il proprio utente con nome dato e uuid randomico"""
        me = My_user(user_id=uuid4(), username=name)
        me.save().addCallback(self.__user_done)

    def __check_post(self, post):
        if len(post.errors) > 0:
            print post.errors
        else:
            logging.debug("Post successfully saved with id %s" % post.post_id)

    def insert_post(self, text=None, image_path=None):
        post = Post
        post.post_id = time.time()
        post.path_to_imagefile = image_path
        post.text_content = text
        post.user_id = self.__my_id
        post.save().addCallback(self.__check_post)


    def insert_node(self, user_id, address, port):
        # TODO se esiste già aggiornare il nodo. prima fare il check della data.
        pass


