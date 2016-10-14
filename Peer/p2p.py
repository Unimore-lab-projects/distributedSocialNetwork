
from twistar.dbconfig.base import InteractionBase
from twisted.python import log
from twisted.spread import pb
from twisted.internet import reactor


from distributedSocialNetwork.DbManagement.db_insertor import *
from distributedSocialNetwork.DbManagement.db_interrogator import *
from distributedSocialNetwork.DbManagement.db_openConnection import *
from distributedSocialNetwork.DbManagement.debug_messages import *
from random import randint
from datetime import datetime

from distributedSocialNetwork.DbManagement.tables import *

import sys

class nodeReceivedCopy(Known_node, pb.RemoteCopy):
    pass

pb.setUnjellyableForClass(Known_node, nodeReceivedCopy)

#attiva il logging
def start_logging():
    enable_logging()
    InteractionBase.LOG = True
    log.startLogging(sys.stdout)

#popola un dizionario a partire dal contenuto di un file
#interpreta ogni linea del file come una coppia chiave[separator]valore
def getDictFromFile(filename, separator):
    in_file = open(filename,"r")
    text = in_file.read()
    in_file.close()
    text=text.split('\n')
    text.pop()
    resultDict=dict()
    for line in text:
        couple=line.split(separator)
        print(couple)
        resultDict[couple[0]]=couple[1]
    print(resultDict)
    return resultDict



class peer(pb.Root):
    
    def __init__(self,configFile):
        start_logging()
        
        #inizializzazione delle variabili d'istanza di Peer:
        self.config=getDictFromFile(configFile, '=')
        self.dbpool=openConnectionOnDB(self.config["db_name"],self.config["db_port"],self.config["db_user"],
        self.config["db_password"],self.config["db_address"])
        self.insertor=DatabaseInsertor(self.dbpool)
        self.interrogator=DatabaseInterrogator(self.dbpool)
        #################################
        
        self.insertor.insert_my_user(self.config["peer_user"])
        self.interrogator.get_my_user().addCallback(self._loadMyUser)
        ################################
        
        reactor.listenTCP(int(self.config["peer_port"]), pb.PBServerFactory(self))
        print("listening on port "+str(self.config["peer_port"]))
    
    def remote_getKnownHosts(self, node):
        print("connessione in ingresso, indirizzo: "+node.address+" porta: "+node.port)
        self.insertor.insert_node(node)
        return self.interrogator.get_known_nodes()
    
    
    def peerConnection(self, ipAddress, remotePortNumber):
        clientFactory=pb.PBClientFactory()
        reactor.connectTCP(ipAddress, remotePortNumber,clientFactory)
        return clientFactory.getRootObject()
    
    
    def _loadMyUser(self, myUser):
        self.myUser=myUser
        print("myUser: "+myUser.username+" "+myUser.user_id)
        self.interrogator.get_known_nodes().addCallback(self._queryKnownHosts, dict())
    
    
    def _queryKnownHosts(self, hostsDict, visitedHostsDict):
        notVisitedHostsDict=dict()
        
        for i in hostsDict:
            if((not visitedHostsDict.has_key(i))and(not i==self.myUser.user_id)) :
                visitedHostsDict[i]=hostsDict[i]
                notVisitedHostsDict[i]=hostsDict[i]
                self.insertor.insert_node(hostsDict[i])
        
        for i in notVisitedHostsDict:
            address=notVisitedHostsDict[i].address
            address=address.split("/")
            deferredObject=self.peerConnection(address[0], int(notVisitedHostsDict[i].port))
            deferredObject.addCallback(self._getHostsList, i, visitedHostsDict)
            print("visiting "+str(i))
        
        pass

    def _getHostsList(self, rootObject, hostUuid, visitedHostsDict):
        print("ottenuto oggetto remoto"+str(hostUuid))
        node=Known_node()
        node.user_id=self.myUser.user_id
        node.username=self.myUser.username
        node.address=self.config["peer_address"]
        node.port=self.config["peer_port"]
        node.last_update=datetime.today()
        remoteKnownHostsDeferred=rootObject.callRemote("getKnownHosts", node)
        remoteKnownHostsDeferred.addCallback(self._queryKnownHosts, visitedHostsDict)
        pass
  
  
  
#sintassi: pyton p2p.py uid address port filename
p=peer(sys.argv[1])
reactor.run()















