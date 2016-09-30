# -*- coding: utf-8 -*

from datetime import datetime
from uuid import uuid4

from query_loader import load_query


class DBinsertor:
    dbpool = None

    def __init__(self, dbpool):
        self.dbpool = dbpool
        if dbpool is None:
            # ERROR
            pass

        pass
        # TODO get my_id
        # my_id =

    def insert_my_user(self, username):
        user_id = uuid4()
        params = (user_id, username)
        # il nome del file sql con la query è uguale al nome della funzione.
        self.dbpool.runOperation(load_query(__name__), params)

    def insert_post(self, text, image):
        # TODO scegliere come gestire le immagini

        # check dei valori inseriti
        if len(text) > 512:
            # TODO error
            pass

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

