from twisted.python import log
from twisted.spread import pb
from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.defer import DeferredList

from twistar.dbconfig.base import InteractionBase

from distributedSocialNetwork.DbManagement.tables import *
from distributedSocialNetwork.DbManagement.db_insertor import *
from distributedSocialNetwork.DbManagement.db_interrogator import *
from distributedSocialNetwork.DbManagement.db_openConnection import *
from distributedSocialNetwork.DbManagement.debug_messages import *

from datetime import datetime

from uuid import uuid4

class nodeReceivedCopy(Known_node, pb.RemoteCopy):
    pass

class userReceivedCopy(My_user, pb.RemoteCopy):
    pass

#class uuidReceivedCopy(UUID, pb.RemoteCopy):
#    pass


pb.setUnjellyableForClass(Known_node, nodeReceivedCopy)
pb.setUnjellyableForClass(My_user, userReceivedCopy)
#pb.setUnjellyableForClass(UUID, uuidReceivedCopy)




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
        #print(couple)
        resultDict[couple[0]]=couple[1]
    #print(resultDict)
    return resultDict
    pass

def getAddressFromNode(node):
    address=node.address
    address=address.split("/")
    return address[0]
    pass
    
def printNodesDict(nodesDict):
    for i in nodesDict:
        print("user_id: "+str(nodesDict[i].user_id)+" port: "+str(nodesDict[i].port))
    pass

class remoteConnection:
    def __init__(self, node, clientFactory):
        self.node=node
        reactor.connectTCP(getAddressFromNode(node), node.port,clientFactory)
        self.rootRemoteReference=None
        self.rootDeferred=clientFactory.getRootObject()
        pass

    def query(self, method, methodArgs=None, callback=None, callbackArgs=None):
        if self.rootRemoteReference is not None:
            __waitForRootObject(self.rootRemoteReference, method, methodArgs, callback, callbackArgs)
        else:
            self.rootDeferred.addCallback(self.__waitForRootCallback, method, methodArgs, callback, callbackArgs)
            self.rootDeferred.addCallback(self.__waitForRootErrback)
        pass

    def __waitForRootCallback(self, rootRemoteRef, method,  methodArgs, callback, callbackArgs):
        deferredObj=rootRemoteRef.callRemote(method, *methodArgs)
        if callback is not None:
            deferredObj.addCallback(callback, *callbackArgs)
#        return self.deferredObj
        pass
    
    def __waitForRootErrback(self, reason):
        print("Errback called in remoteConnection istance reason: "+str(reason))
        pass

class nodeConnections:
    def __init__(self):
        self.connections=dict()
        #self.clientFactory=pb.PBClientFactory()
    def connect(self, node):
        if self.connections.has_key(node.user_id):
            return self.connections[node.user_id]
        else:
            self.connections[node.user_id]=remoteConnection(node, pb.PBClientFactory())
            return self.connections[node.user_id]
    def refresh(self, node):
        self.connections[node.user_id]=remoteConnection(node, pb.PBClientFactory())
        return self.connections[node.user_id]

class node(pb.Root):
    def __init__(self, configFile):
        #start_logging()
        
        #inizializzazione delle variabili di istanza:
        self.config=getDictFromFile(configFile, '=')
        self.dbpool=openConnectionOnDB(self.config["db_name"],self.config["db_port"],self.config["db_user"],self.config["db_password"],self.config["db_address"])
        
        self.insertor=DatabaseInsertor(self.dbpool)
        self.interrogator=DatabaseInterrogator(self.dbpool)
        self.currentConnections=nodeConnections()
        #----------------------------------------------------------------
        
        #self.insertor.insert_my_user(self.config["peer_user"])
        #-----------------------------------------------------------------
        reactor.listenTCP(int(self.config["peer_port"]), pb.PBServerFactory(self))
        pass
    
    def incomingConnection(self, callerNode):
        print("connessione in ingresso: "+str(callerNode.user_id)+" "+
            str(callerNode.address)+" "+str(callerNode.port))
        self.insertor.insert_node(callerNode)
        pass

    def getMyNode(self):
        result=Deferred()
        self.insertor.insert_my_user(self.config["peer_user"]).addCallback(self.__getMyUser,  result)
        return result
        pass
    
    def __getMyUser(self,done, result):
        self.interrogator.get_my_user().addCallback(self.__waitForMyUser, result)
        pass
    
    def __waitForMyUser(self, myUser, deferred):
        myNode=Known_node()
        myNode.user_id=str(myUser.user_id)
        myNode.username=myUser.username
        myNode.address=self.config["peer_address"]
        myNode.port=self.config["peer_port"]
        myNode.last_update=datetime.today()
        deferred.callback(myNode)
        pass

    def remote_getKnownNodes(self, callerNode):
        result=Deferred()
        self.incomingConnection(callerNode)
        self.interrogator.get_known_nodes(callerNode).addCallback(self.__convertUuidType, result)
        return result
        pass
    
    def __convertUuidType(self, nodesDict, deferred):
        resultNodesDict=dict()
        for i in nodesDict:
            resultNodesDict[str(i)]=nodesDict[i]
            uuidString=resultNodesDict[str(i)].user_id
            if not isinstance(uuidString, basestring):
                uuidString=uuidString.urn
                uuidString=uuidString[9:]
            resultNodesDict[str(i)].user_id=uuidString
        
        deferred.callback(resultNodesDict)
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
        #currentKnownNodesDeferred=self.interrogator.get_known_nodes()
        currentKnownNodesDeferred=Deferred()
        self.interrogator.get_known_nodes().addCallback(self.__convertUuidType, currentKnownNodesDeferred)
        starter=DeferredList([currentKnownNodesDeferred,  myNodeDeferred])
        starter.addCallback(self.__waitForStartCondition)
        currentKnownNodesDeferred.addErrback(self.__printErrorErrback)
        pass
    
    def __waitForStartCondition(self, starter):
        visitedNodesDict=dict()
        self.getAllKnownNodes(starter[0][1], visitedNodesDict, starter[1][1])
    
    def __printErrorErrback(self, result):
        print("errback: "+result)
        pass
    
    def getAllKnownNodes(self,nodesDict, visitedNodesDict, myNode):
        notVisitedNodesDict=dict()
        
        if(len(nodesDict)<int(self.config["peer_known_nodes_threshold"])):
            for i in nodesDict:
                if((not visitedNodesDict.has_key(i)) and (not nodesDict[i].user_id==myNode.user_id)):
                    visitedNodesDict[i]=nodesDict[i]
                    notVisitedNodesDict[i]=nodesDict[i]
                    #print(nodesDict[i])
                    
                    self.insertor.insert_node(nodesDict[i])
                pass
            
            print("nodi ricevuti:")
            printNodesDict(nodesDict)
            print("nodi visitati:")
            printNodesDict(visitedNodesDict)
            print("nodi da visitare:")
            printNodesDict(notVisitedNodesDict)
            
            for i in notVisitedNodesDict:
                connection=self.currentConnections.connect(notVisitedNodesDict[i])
                connection.query("getKnownNodes",[myNode],  self.getAllKnownNodes, [visitedNodesDict, myNode])
                print("visiting address: "+notVisitedNodesDict[i].address+" port: "+str(notVisitedNodesDict[i].port)+" user_id: "+str(notVisitedNodesDict[i].user_id))
        
    pass
    
    def buildTimeline(self):
        timeline=DeferredList([])
        myNodeDeferred=self.getMyNode()
        myFriendsDeferred=self.interrogator.get_friends()
        starter=DeferredList([myNodeDeferred, myFriendsDeferred])
        starter.addCallback(__getAllPostsAndComments, timeline)
        return timeline
        pass
    
    def __getAllPostsAndComments(self, starter, timeline):
        myNode=starter[0]
        myFriends=starter[1]
        
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
        
        

        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
    
    
