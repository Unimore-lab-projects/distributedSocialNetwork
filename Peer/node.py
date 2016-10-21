from twisted.python import log
from twisted.spread import pb
from twisted.internet import reactor
from twisted.internet.defer import Deferred


from distributedSocialNetwork.DbManagement.db_insertor import *
from distributedSocialNetwork.DbManagement.db_interrogator import *
from distributedSocialNetwork.DbManagement.db_openConnection import *
from distributedSocialNetwork.DbManagement.debug_messages import *

from random import randint
from datetime import datetime

def start_logging():
    enable_logging()
    InteractionBase.LOG = True
    log.startLogging(sys.stdout)
    pass

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

def getAddressFromNode(node):
    address=node.address
    address=address.split("/")
    return address[0]

class remoteConnection:
    def __init__(self, node):
        self.node=node
        self.clientFactory=pb.PBClientFactory()
        reactor.connectTCP(getAddressFromNode(node), node.port,self.clientFactory)
        self.rootRemoteReference=None
        self.rootDeferred=self.clientFactory.getRootObject()
        pass

    def query(self, method, methodArgs=None, callback=None, callbackArgs=None):
        if not self.rootRemoteReference==None:
            __waitForRootObject(self.rootRemoteReference, method, methodArgs, callback, callbackArgs)
        else:
            self.rootDeferred.addCallback(self.__waitForRootCallback, method, methodArgs, callback, callbackArgs)
        pass

    def __waitForRootCallback(self, rootRemoteRef, method,  methodArgs, callback, callbackArgs):
        deferredObj=rootRemoteRef.callRemote(method, *methodArgs)
        if not callback==None:
            deferredObj.addCallback(callback, *callbackArgs)
#        return self.deferredObj
        pass


class nodeConnections:
    def __init__(self):
        self.connections=dict()
    def connect(self, node):
        if self.connections.has_key(node.user_id):
            return self.connections[node.user_id]
        else:
            self.connections[node.user_id]=remoteConnection(node)
            return self.connections[node.user_id]
    def refresh(self, node):
        self.connections[node.user_id]=remoteConnection(node)
        return self.connections[node.user_id]

class node(pb.Root):
    def __init__(self, configFile):
        start_logging()
        
        #inizializzazione delle variabili di istanza:
        self.config=getDictFromFile(configFile, '=')
        self.dbpool=openConnectionOnDB(self.config["db_name"],self.config["db_port"],self.config["db_user"],
        self.config["db_password"],self.config["db_address"])
        
        self.insertor=DatabaseInsertor(self.dbpool)
        self.interrogator=DatabaseInterrogator(self.dbpool)
        self.remoteInterface=remoteNodeInterface(self.insertor, self.interrogator, self.config["peer_port"])
        self.currentConnections=nodeconnections()
        #----------------------------------------------------------------
        
        #inserimento di un record my_user nel database (se la tabella my_user è vuota)
        self.insertor.insert_my_user(self.config["peer_user"])
        #-----------------------------------------------------------------
        pass
    
    def incomingConnection(self, callerNode):
        print("connessione in ingresso: "+str(callerNode.user_id)+" "+
            str(callerNode.address)+" "+str(callerNode.port))
        self.insertor.insert_node(callerNode)
        pass

    def getMyNode(self):
        result=Deferred()
        self.interrogator.get_known_nodes().addCallback(self.__waitForMyUser,  result)
        return result
        pass
    
    def __waitForMyUser(self, myUser, deferred):
        myNode=Known_node()
        myNode.user_id=myUser.user_id
        myNode.username=myUser.username
        myNode.address=self.config["peer_address"]
        myNode.port=self.config["peer_port"]
        myNode.last_update=datetime.today()
        deferred.callback(myNode)
        pass

    def remote_getKnownNodes(self, callerNode):
        self.incomingConnection(callerNode)
        #print("Query: Get Known Nodes")
        return self.interrogator.get_known_nodes(callerNode)
        pass
        
    def remote_getPostsAndComments(self, callerNode, days):
        self.incomingConnection(callerNode)
        return interrogator.get_recents(days)
        pass
        
    def remote_passNode(self, callerNode,  passedNode):
        self.incomingConnection(callerNode)
        self.insertor.insert_node(passedNode)
        self.currentConnections.refresh(passedNode)
        pass

    def remote_resolveUserID(self, callerNode,  targetUid,  timeToLive):
        self.incomingConnection(callerNode)
        myNodeDeferred=self.getMyNode()
        checkNodeDeferred=self.interrogator.get_node(targetUid)
        starter=DeferredList([myNodeDeferred, checkNodeDeferred])
        starter.addCallback(self.__isNodeKnown, callerNode, targetUid, timeToLive)
        pass
    
    def __isNodeKnown(self, result, callerNode, targetUid, timetoLive):
        myNode=result[0]
        nodeChecked=node[1]
        
        if not nodeChecked == None:
            c=self.currentConnections.connect(callerNode)
            c.query("passNode",myNode, nodeChecked )
        elif timeToLive>0:
            timeToLive=timeToLive-1
            deferredKnownNodes=self.interrogator.get_known_nodes(callerNode)
            deferredKnownNodes.addCallback(self.__forwardToKnownNodes, callernode, targetUid, timeToLive)
        pass
    
    def __forwardToKnownNodes(self, knownNodes,callerNode, targetUid, timeToLive ):
        for i in knownNodes:
            c=currentConnections.connect(knownNodes[i])
            c.query("resolveUserID", [callerNode, targetUid, timeToLive])
        pass
    
    def populateKnownNodes(self):
        myNodeDeferred=self.getMyNode()
        currentKnownNodesDeferred=self.interrogator.get_known_nodes()
        starter=DeferredList([currentKnownNodesDeferred,  myNodeDeferred])
        starter.addCallback(__waitforStartCondition)
        pass
    
    def __waitForStartCondition(self, starter):
        self.getAllKnownNodes(starter[0], dict(), starter[1])
    
    
    def getAllKnownNodes(self,nodesDict, visitedNodesDict, myNode):
        notVisitedNodesDict=dict()
        
        if(len(nodesDict)<self.config["peer_known_nodes_threshold"]):
            for i in nodesDict:
                if((not visitedNodesDict.has_key(i))):
                    visitedNodesDict[i]=nodesDict[i]
                    notVisitedNodesDict[i]=nodesDict[i]
                    self.insertor.insert_node(nodesDict[i])
            
            for i in notVisitedNodesDict:
                connection=self.currentConnections.connect(notvisitedNodesDict[i])
                connection.query("getKnownNodes",[self.myNode],  self.populateKnownNodes, [visitedNodesDict])
                print("visiting "+str(i))
        
    pass
    
    def buildTimeline(self):
        myNodeDeferred=self.getMyNode()
        myFriendsDeferred=self.interrogator.get_friends()
        starter=DeferredList([myNodeDeferred, myFriendsDeferred])
        starter.addCallback(__getPostsAndComments)
        pass
    
    def __getAllPostsAndComments(self, starter):
        myNode=starter[0]
        myFriends=starter[1]
        
        timeline=DeferredList([])
        for i in myFriends:
            c=self.currentConnections.connect(myFriends[i])
            c.rootDeferred.addCallback(__getPostsAndCommentsCallback, timeline)
            c.rootDeferred.addErrback(__getPostsAndCommentsErrback, myNode, myFriends[i])
        pass
    
    def __getPostsAndCommentsCallback(self, remoteReference, timeline):
        timeline.append(remoteReference.callRemote("getPostsAndComments"))
        pass
    
    def __getPostsAndCommentsErrback(self, reason, myNode, friendNotReachable):
        timeToLive=self.config["peer_time_to_live"]
        deferredKnownNodes=self.interrogator.get_known_nodes(callerNode)
        deferredKnownNodes.addCallback(self.__forwardToKnownNodes, myNode, friendNotReachable.user_id, timeToLive)
        pass
        
        

        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    
