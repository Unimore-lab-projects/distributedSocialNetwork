# -*- coding: utf-8 -*
from twistar.dbconfig.base import InteractionBase
from twistar.dbobject import DBObject
from uuid import uuid4
from twistar.registry import Registry
from twisted.enterprise import adbapi
from twisted.python import log
from twisted.internet import reactor
from tables import *
import logging

class DatabaseInsertor:
    def __init__(self, dbpool):
        Registry.DBPOOL = dbpool

    def __user_done(self,user):
        logging.debug("My user created. uuid is %s and username is %s" % (user.user_id, user.username))

    def insert_my_user(self, name):
        """Inserisce il proprio utente con nome dato e uuid randomico"""
        me = My_user(user_id=uuid4(),username=name)
        me.save().addCallback(self.__user_done)


    def insert_post(self, text, image):
        # TODO scegliere come gestire le immagini

        # check dei valori inseriti


        # TODO get image file path
        post_id = datetime.now()
        # params = (post_id, my_id, image_path, text)
        # self.dbpool.runOperation(load_query(__name__), params)

    def insert_new_node(self, user_id, address, port):
        # TODO scrivere i deferred per questa query e spostare tutto in db_interrogator!!!
        d = self.dbpool.runQuery(load_query("check_node"))

        last_update = datetime.now()
        params = (user_id, address, port, last_update)
        self.dbpool.runOperation(load_query(__name__), params)
