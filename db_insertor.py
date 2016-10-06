# -*- coding: utf-8 -*
from uuid import uuid4

from psycopg2 import extras

from db_interrogator import *


class DatabaseInsertor:
    def __init__(self, dbpool):
        Registry.DBPOOL = dbpool

    # INSERT USER

    def __user_done(self, user):
        if len(user.errors) > 0:
            print '%s errors in user creation' % len(user.errors)
            print user.errors
        else:
            logging.debug("My user created. uuid is %s and username is %s" % (user.user_id, user.username))

    def __check_existence(self, userExists, me):
        if userExists == 0:
            me.save().addCallback(self.__user_done)
        else:
            logging.debug("user already existing")

    def insert_my_user(self, name):
        """Inserisce il proprio utente con nome dato e uuid randomico"""
        extras.register_uuid()
        # my_uuid = uuid4()
        # extensions.adapt(my_uuid).getquoted()
        me = My_user(user_id=uuid4(), username=name)
        # controlla se esiste già un utente
        My_user.count().addCallback(self.__check_existence, me)

    # INSERT OR UPDATE A NODE

    def __check_node_exists(self, doExists, address, port):
        if doExists:
            node = Known_node()
        else:
            return False

    def insert_node(self, user_id, address, port):
        Known_node.exists(['user_id = ?', user_id]).addCallback(self.__check_node_exists, address, port)

    # INSERT A POST

    def __check_post(self, post):
        if post.errors.isEmpty():
            logging.debug("Post successfully saved with id %s" % post.post_id)
        else:
            print post.errors

    def insert_post(self, text=None, image_path=None):
        post = Post
        # TODO da rifare la correzione dei tipi
        # post.post_id = time.time()
        post.path_to_imagefile = image_path
        post.text_content = text
        post.user_id = self.__my_id
        post.save().addCallback(self.__check_post)
