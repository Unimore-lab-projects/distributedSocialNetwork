# -*- coding: utf-8 -*
from datetime import datetime
from uuid import uuid4

from psycopg2 import extras

from db_interrogator import *


class DatabaseInsertor:
    def __init__(self, dbpool):
        Registry.DBPOOL = dbpool

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
            me.save().addCallback(self.__user_done)
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

    # INSERT A POST

    def insert_post(self, post=None):
        # TODO
        pass


    # INSERT A FRIEND

    def insert_friend(self, ):
        pass
