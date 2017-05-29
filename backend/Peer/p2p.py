
from twistar.dbconfig.base import InteractionBase
from twisted.python import log
from twisted.spread import pb
from twisted.internet import reactor, defer


from distributedSocialNetwork.DbManagement.db_insertor import *
from distributedSocialNetwork.DbManagement.db_interrogator import *
from distributedSocialNetwork.DbManagement.db_openConnection import *
from distributedSocialNetwork.DbManagement.debug_messages import *
from random import randint
from datetime import datetime

from distributedSocialNetwork.DbManagement.tables import *

import sys

from connection import remoteConnection

class nodeReceivedCopy(Known_node, pb.RemoteCopy):
    pass

class userReceivedCopy(My_user, pb.RemoteCopy):
    pass


pb.setUnjellyableForClass(Known_node, nodeReceivedCopy)
pb.setUnjellyableForClass(My_user, userReceivedCopy)


#attiva il logging
def start_logging():
    enable_logging()
    InteractionBase.LOG = True
    log.startLogging(sys.stdout)
    pass

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
    pass
    
def peerConnection(host, port):
        clientFactory=pb.PBClientFactory()
        reactor.connectTCP(host, port,clientFactory)
        return clientFactory.getRootObject()
        pass
        
def getAddressFromNode(node):
    address=node.address
    address=address.split("/")
    return address[0]

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
        self.interrogator.get_my_user().addCallback(self.initMyNode)
       
        ################################
        
        reactor.listenTCP(int(self.config["peer_port"]), pb.PBServerFactory(self))
        print("listening on port "+str(self.config["peer_port"]))
        pass
    
    def incomingConnection(self, callerNode):
        print("connessione in ingresso: "+str(callerNode.user_id)+" "+
            str(callerNode.address)+" "+str(callerNode.port))
        
        self.insertor.insert_node(callerNode)
       


    def remote_getKnownNodes(self, callerNode):
        self.incomingConnection(callerNode)
        print("Query: Get Known Nodes")

        return self.interrogator.get_known_nodes(callerNode)
        pass
        

    
    def remote_getPostsAndComments(self, callerNode):
        incomingConnection(callerNode)
        print("Query: get Posts and Comments")
        pass
    
    def remote_passNode(self, callerNode, node):
        incomingConnection(callerNode)
        self.insertor.inser_node(node)
    
    def remote_resolveUserID(self, callerNode, user_id, timeToLive):
        self.interrogator.get_node(user_id).addCallback(self.__waitForCheckNode, callerNode, timeToLive, resultDeferred)
        pass
    
    def __waitForCheckNode(self, node, callerNode, timeToLive):

        if(node!=None):
            c=remoteConnection(node)
            c.query("passNode", [callerNode, node])
        else:
            timeToLive=timeToLive-1
            self.interrogator.get_known_nodes(callerNode).addCallback(self.__waitDBGetKnownNodes, 
            callerNode, timeToLive)
        pass
    
    def __waitDBGetKnownNodes(self, knownNodes, callerNode,  user_id,  timeToLive):
        for i in knownNodes:
            remoteConnection(knownNodes[i]).query("resolveUserID", [callerNode, user_id, timeToLive])
            
        
    
    def initMyNode(self, myUser):
        self.myNode=Known_node()
        self.myNode.user_id=myUser.user_id
        self.myNode.username=myUser.username
        self.myNode.address=self.config["peer_address"]
        self.myNode.port=self.config["peer_port"]
        self.myNode.last_update=datetime.today()
        print("User: "+myUser.username+" "+myUser.user_id)
        
        self.interrogator.get_known_nodes().addCallback(self.populateKnownNodes, dict())
        pass
    
    
    def populateKnownNodes(self, nodesDict, visitedNodesDict):
        notVisitedNodesDict=dict()
        
        if(len(nodesDict)<self.config["peer_known_nodes_threshold"]):
            for i in nodesDict:
                if((not visitedNodesDict.has_key(i))):
                    visitedNodesDict[i]=nodesDict[i]
                    notVisitedNodesDict[i]=nodesDict[i]
                    self.insertor.insert_node(nodesDict[i])
            
            for i in notVisitedNodesDict:
#                address=notVisitedNodesDict[i].address
#                address=address.split("/")
#                deferredObject=peerConnection(address[0], int(notVisitedNodesDict[i].port))
                address=getAddressFromNode(notvisitedNodesDict[i])
                deferredObject=peerConnection(address, int(notVisitedNodesDict[i].port))
                deferredObject.addCallback(self.knownNodesQuery, i, visitedNodesDict)
                print("visiting "+str(i))
        
        pass

    def knownNodesQuery(self, rootObject, nodeUuid, visitedNodesDict):
        print("ottenuto oggetto remoto "+str(nodeUuid))
        remoteKnownNodesDeferred=rootObject.callRemote("getKnownNodes", self.myNode)
        remoteKnownNodesDeferred.addCallback(self.populateKnownNodes, visitedNodesDict)
        pass
  
  
  
#sintassi: pyton p2p.py config
p=peer(sys.argv[1])
reactor.run()















