# -*- coding: utf-8 -*

from twisted.python import log

from db_interrogator import *


class DatabaseRemover:
    def __init__(self, dbpool):
        Registry.DBPOOL = dbpool

    def __done_remove_node(self, node):
        logging.debug("node deleted")

    def remove_node(self, node=None, user_id=None):
        if node is None:
            node.delete().addCallbacks(self.__done_remove_node, log.err)
        else:
            Known_node.deleteAll(where=['user_id=?', user_id]).addCallbacks(self.__done_remove_node, log.err)
