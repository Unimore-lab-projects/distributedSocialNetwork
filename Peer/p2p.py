
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

class nodeSendCopy(Known_node, pb.Copyable):
    pass

class nodeReceivedCopy(Known_node, pb.RemoteCopy):
    pass

pb.setUnjellyableForClass(nodeSendCopy, nodeReceivedCopy)

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
    print(self.knownHosts)
    return resultDict

class peer(pb.Root):
    
    def __init__(self,configFile):
        start_logging()
        
        #inizializzazione delle variabili d'istanza di Peer:
        #self.knownHosts=getDictFromFile(knownHostsFile, ',')
        self.config=getDictFromFile(configFile, '=')
        self.dbpool=openConnectionOnDB(self.config["db_name"],self.config["db_port"],self.config["db_user"],
        self.config["db_password"],self.config["db_address"])
        self.insertor=DatabaseInsertor(self.dbpool)
        self.interrogator=DatabaseInterrogator(self.dbpool)
        #################################
        
        self.insertor.insert_my_user(self.config["peer_user"])
        self.interrogator.get_my_user().addCallback('__loadMyUser')
        ################################
        
        reactor.listenTCP(self.config["peer_port"], pb.PBServerFactory(self))
        print("listening on port "+str(self.config["peer_port"]))
        
        
        #query per popolare la tabella dei known nodes
        self.interrogator.get_known_nodes().addCallback('__queryKnownHosts', dict())
        #self.queryKnownHosts(self.knownHosts, dict())
    
    def __loadMyUser(self, myUser):
        self.myUser=myUser
    
    
#    def remote_getKnownHosts(self, uid, address, port):
#        print("connessione in ingresso, indirizzo: "+address+" porta: "+port)
#        if not self.knownHosts.has_key(uid):
#            self.knownHosts[uid]=address+":"+port
#        return self.knownHosts

    def remote_getKnownHosts(self, node):
        print("connessione in ingresso, indirizzo: "+node.address+" porta: "+node.port)
        self.insertor.insert_node(node)
        return self.interrogator.get_known_nodes()
    
    
    def peerConnection(self, ipAddress, remotePortNumber):
        clientFactory=pb.PBClientFactory()
        reactor.connectTCP(ipAddress, remotePortNumber,clientFactory)
        return clientFactory.getRootObject()
    
    
#    def queryKnownHosts(self, hosts, visitedHosts):
#        
#        notVisitedHosts=dict()
#        
#        for i in hosts:
#            if((not visitedHosts.has_key(i))and(not i==self.uid)) :
#                visitedHosts[i]=hosts[i]
#                notVisitedHosts[i]=hosts[i]
#                self.knownHosts[i]=hosts[i]
#        
#        for i in notVisitedHosts:
#            value=notVisitedHosts[i].split(':')
#            address=value[0]
#            port=value[1]
#            deferredObject=self.peerConnection(address, int(port))
#            deferredObject.addCallback(self.getHostsList, i, visitedHosts)
#            print("visiting "+str(i))
#        
#    def getHostsList(self, rootObject, hostUid,  visitedHosts):
#        print("ottenuto oggetto remoto"+str(hostUid))
#        remoteKnownHosts=rootObject.callRemote("getKnownHosts", self.uid, self.address, self.port)
#        remoteKnownHosts.addCallback(self.queryKnownHosts, visitedHosts)
    
    def __queryKnownHosts(self, hostsDict, visitedHostsDict):
        notVisitedHosts=dict()
        
        for i in hosts:
            if((not visitedHosts.has_key(i))and(not i==self.myUser.user_id)) :
                visitedHosts[i]=hosts[i]
                notVisitedHosts[i]=hosts[i]
                self.knownHosts[i]=hosts[i]
        
        for i in notVisitedHosts:
            deferredObject=self.peerConnection(notVisitedHosts[i].address, int(notVisitedHosts[i].port))
            deferredObject.addCallback(self.getHostsList, i, visitedHosts)
            print("visiting "+str(i))
        
        pass

    def __getHostsList(self):
        print("ottenuto oggetto remoto"+str(hostUid))
        node=nodeSendCopy()
        node.user_id=self.myUser.user_id
        node.username=self.myUser.username
        node.address=self.config["peer_address"]
        node.port=self.config["peer_port"]
        remoteKnownHosts=rootObject.callRemote("getKnownHosts", self.myUser.user_id, node)
        remoteKnownHosts.addCallback(self.queryKnownHosts, visitedHosts)
        pass
  
  
  
#sintassi: pyton p2p.py uid address port filename
p=peer(sys.argv[1])
reactor.run()















