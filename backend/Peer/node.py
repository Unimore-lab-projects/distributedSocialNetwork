from twistar.dbconfig.base import InteractionBase
from twisted.internet.defer import Deferred
from twisted.internet.defer import DeferredList

from backend.DbManagement.db_insertor import *
from backend.DbManagement.db_interrogator import *
from backend.DbManagement.db_openConnection import open_connection
from backend.DbManagement.debug_messages import *


class postPackageReceivedCopy(PostPackage, pb.RemoteCopy):
    pass


class nodeReceivedCopy(Known_node, pb.RemoteCopy):
    pass


class postReceivedCopy(Post, pb.RemoteCopy):
    pass


class commentReceivedCopy(Comment, pb.RemoteCopy):
    pass


pb.setUnjellyableForClass(PostPackage, postPackageReceivedCopy)
pb.setUnjellyableForClass(Known_node, nodeReceivedCopy)
pb.setUnjellyableForClass(Post, postReceivedCopy)
pb.setUnjellyableForClass(Comment, postReceivedCopy)


def start_logging():
    enable_logging()
    InteractionBase.LOG = True
    log.startLogging(sys.stdout)
    pass


def getDictFromFile(filename, separator):
    in_file = open(filename, "r")
    text = in_file.read()
    in_file.close()
    text = text.split('\n')
    text.pop()
    resultDict = dict()
    for line in text:
        couple = line.split(separator)
        # print(couple)
        resultDict[couple[0]] = couple[1]
    print(resultDict)
    return resultDict
    pass


def getAddressFromNode(node):
    address = node.address
    address = address.split("/")
    return address[0]
    pass


def printNodesDict(nodesDict):
    for i in nodesDict:
        print("user_id: " + str(nodesDict[i].user_id) + " address: " + str(nodesDict[i].address) + " port: " + str(
            nodesDict[i].port))
    pass


def convertReceivedNodeInKnownNode(receivedNode):
    bufNode = Known_node()
    bufNode.user_id = str(receivedNode.user_id)
    # bufNode.username=receivedNode.username
    bufNode.address = receivedNode.address
    bufNode.port = receivedNode.port
    bufNode.last_update = receivedNode.last_update
    return bufNode
    pass


def convertUuid(uuid):
    uuidString = uuid
    if not isinstance(uuidString, basestring):
        uuidString = uuidString.urn
        uuidString = uuidString[9:]
    return uuidString


class remoteConnection:
    def __init__(self, node, clientFactory):
        self.node = node
        reactor.connectTCP(getAddressFromNode(node), int(node.port), clientFactory)
        self.rootRemoteReference = None
        # try
        self.rootDeferred = clientFactory.getRootObject()
        # exception
        pass

    def query(self, method, methodArgs=None, callback=None, callbackArgs=None):
        if self.rootRemoteReference is not None:
            self.__waitForRootCallback(self.rootRemoteReference, method, methodArgs, callback, callbackArgs)
        else:
            self.rootDeferred.addCallback(self.__waitForRootCallback, method, methodArgs, callback, callbackArgs)
            self.rootDeferred.addErrback(self.__Errback, self.node)
        pass

    def __waitForRootCallback(self, rootRemoteRef, method, methodArgs, callback, callbackArgs):
        self.rootRemoteReference = rootRemoteRef
        deferredObj = rootRemoteRef.callRemote(method, *methodArgs)
        if callback is not None:
            deferredObj.addCallback(callback, *callbackArgs)
        deferredObj.addErrback(self.__Errback, self.node)
        return rootRemoteRef
        pass

    def __Errback(self, reason, remoteNode):
        print(
            "Errback called in remoteConnection istance connecting to: " + str(remoteNode.port) + " reason: " + str(
                reason))
        pass


class nodeConnections:
    def __init__(self):
        self.connections = dict()

    def connect(self, node):
        node = convertReceivedNodeInKnownNode(node)
        if self.connections.has_key(node.user_id):
            return self.connections[node.user_id]
        else:
            self.connections[node.user_id] = remoteConnection(node, pb.PBClientFactory())
            return self.connections[node.user_id]

    def refresh(self, node):
        node = convertReceivedNodeInKnownNode(node)
        self.connections[node.user_id] = remoteConnection(node, pb.PBClientFactory())
        return self.connections[node.user_id]


class node(pb.Root):
    def __init__(self, configFile, port=None):
        # start_logging()

        self.config = getDictFromFile(configFile, '=')
        if port:
            self.config['port'] = port
        # self.dbpool = openConnectionOnDB(self.config["db_name"], self.config["db_port"], self.config["db_user"],
        #                                  self.config["db_password"], self.config["db_address"])
        self.dbpool = open_connection(user=self.config["db_user"], dbname=self.config['db_name'])
        self.insertor = DatabaseInsertor(self.dbpool)
        self.interrogator = DatabaseInterrogator(self.dbpool)
        self.currentConnections = nodeConnections()

        # reactor.listenTCP(int(self.config["peer_port"]), pb.PBServerFactory(self))
        pass

    def get_interrogator(self):
        return self.interrogator

    def incomingConnection(self, callerNode):
        print("connessione in ingresso: " + str(callerNode.user_id) + " " +
              str(callerNode.address) + " " + str(callerNode.port))
        self.insertor.insert_node(callerNode)
        pass

    def getPort(self):
        return int(self.config['peer_port'])
        pass

    def getMyNode(self):
        result = Deferred()
        self.insertor.insert_my_user(self.config["peer_user"]).addCallback(self.__getMyUser, result)
        return result
        pass

    def __getMyUser(self, done, result):
        self.interrogator.get_my_user().addCallback(self.__waitForMyUser, result)
        pass

    def __waitForMyUser(self, myUser, deferred):
        myNode = Known_node()
        myNode.user_id = str(myUser.user_id)
        myNode.username = myUser.username
        myNode.address = self.config["peer_address"]
        myNode.port = self.config["peer_port"]
        myNode.last_update = datetime.today()
        deferred.callback(myNode)
        self.myNode = myNode
        pass

    def remote_getKnownNodes(self, callerNode):
        result = Deferred()
        self.incomingConnection(callerNode)
        self.interrogator.get_known_nodes(callerNode).addCallback(self.__convertKnownNodeUuidType, result)
        return result
        pass

    def __convertKnownNodeUuidType(self, nodesDict, deferred):
        resultNodesDict = dict()
        for i in nodesDict:
            resultNodesDict[str(i)] = nodesDict[i]
            uuidString = resultNodesDict[str(i)].user_id
            if not isinstance(uuidString, basestring):
                uuidString = uuidString.urn
                uuidString = uuidString[9:]
            resultNodesDict[str(i)].user_id = uuidString

        deferred.callback(resultNodesDict)
        pass

    def getPostsAndComments(self, callerNode, days):
        result = Deferred()
        self.incomingConnection(callerNode)
        self.interrogator.get_recents(days).addCallback(self.__waitForPackageList, result)
        return result
        pass

    def remote_getPostsAndComments(self, callerNode, days):
        result = Deferred()
        self.incomingConnection(callerNode)
        self.interrogator.get_recents(days).addCallback(self.__waitForPackageList, result)
        return result
        pass

    def __waitForPackageList(self, postPackageDeferreds, result):
        packageDeferreds = []
        for package in postPackageDeferreds:
            packageDeferreds.append(package)
        packageDeferredList = DeferredList(packageDeferreds)
        packageDeferredList.addCallback(self.__convertPostPackageUuidType, result)

        pass

    def __convertPostPackageUuidType(self, postPackageList, result):

        for package in postPackageList:
            print(package[1].getPost())
            package[1].getPost().user_id = convertUuid(package[1].getPost().user_id)
            comments = package[1].getComments()
            for comment in comments:
                comment.user_id = convertUuid(comment.user_id)

        result.callback(postPackageList)
        pass

    def remote_passNode(self, callerNode, passedNode):
        print("Risposta alla richiesta di risoluzione:")
        self.incomingConnection(callerNode)
        self.insertor.insert_node(passedNode)
        self.currentConnections.refresh(passedNode)
        pass

    def remote_resolveUserID(self, callerNode, solverNode, targetUid, timeToLive):
        callerNode = convertReceivedNodeInKnownNode(callerNode)
        solverNode = convertReceivedNodeInKnownNode(solverNode)
        print("Richiesta di risoluzione inoltrata da:")
        self.incomingConnection(callerNode)
        myNodeDeferred = self.getMyNode()
        checkNodeDeferred = self.interrogator.get_node(targetUid)
        starter = DeferredList([myNodeDeferred, checkNodeDeferred])
        starter.addCallback(self.__isNodeKnown, solverNode, targetUid, timeToLive)
        pass

    def __isNodeKnown(self, result, solverNode, targetUid, timeToLive):
        myNode = result[0][1]
        nodeFound = result[1][1]

        if nodeFound is not None:
            c = self.currentConnections.connect(solverNode)
            c.query("passNode", [myNode, nodeFound])
        elif timeToLive > 0:
            timeToLive = timeToLive - 1
            deferredKnownNodes = self.interrogator.get_known_nodes(myNode)
            deferredKnownNodes.addCallback(self.__forwardToKnownNodes, myNode, solverNode, targetUid, timeToLive)
        pass

    def __forwardToKnownNodes(self, knownNodes, myNode, solverNode, targetUid, timeToLive):
        print("**************************************")
        print("inoltro a:")
        printNodesDict(knownNodes)
        print("**************************************")
        for i in knownNodes:
            c = self.currentConnections.connect(knownNodes[i])
            c.query("resolveUserID", [myNode, solverNode, targetUid, timeToLive])
        pass

    def remote_insertComment(self, callerNode, content, post_id):
        print("remote %s " % content)
        self.insertComment(comment=None, post_id=post_id, content=content,
                           user_id=callerNode.user_id, username=callerNode.username)
        pass

    def insertComment(self, comment=None, post_id=None, user_id=None, username=None, content=None):
        print("insertComment %s " % content)
        self.insertor.insert_comment(comment=comment, post_id=post_id,
                                     user_id=user_id, username=username, content=content)
        pass

    def insertPost(self, post=None, text_content=None, path_to_imagefile=None):
        self.insertor.insert_post(post, text_content, path_to_imagefile)
        print("post with text %s added" % text_content)
        pass

    def sendComment(self, content, post_id, remote_user_id):
        # self.interrogator.get_my_user().addCallback(self._sendCommentCallback,content,post_id)
        myUserDeferred = self.getMyNode()
        remoteNodeDeferred = self.interrogator.get_node(remote_user_id)
        DeferredList([myUserDeferred, remoteNodeDeferred]).addCallback(self._sendCommentCallback,
                                                                       content, post_id)
        pass

    def _sendCommentCallback(self, result, content, post_id):
        myUser = result[0][1]
        remoteNode = result[1][1]

        connection = self.currentConnections.connect(remoteNode)
        connection.query("insertComment", [myUser, content, post_id])

        pass

    def populateKnownNodes(self):
        """
        Chiede ai propri known nodes la lista dei loro known_nodes.
        :return:
        """
        myNodeDeferred = self.getMyNode()
        currentKnownNodesDeferred = Deferred()
        self.interrogator.get_known_nodes().addCallback(self.__convertKnownNodeUuidType,
                                                        currentKnownNodesDeferred).addErrback(self.prov_errback)
        starter = DeferredList([currentKnownNodesDeferred, myNodeDeferred])
        starter.addCallback(self.__waitForStartCondition)
        starter.addErrback(self.prov_errback)
        pass

    def prov_errback(self, e):
        logging.error(e)
        pass

    def __waitForStartCondition(self, starter):
        visitedNodesDict = dict()
        self.getAllKnownNodes(starter[0][1], visitedNodesDict, starter[1][1])
        pass

    def getAllKnownNodes(self, nodesDict, visitedNodesDict, myNode):
        notVisitedNodesDict = dict()

        for i in nodesDict:
            if ((not visitedNodesDict.has_key(i)) and (not nodesDict[i].user_id == myNode.user_id)):
                visitedNodesDict[i] = nodesDict[i]
                notVisitedNodesDict[i] = nodesDict[i]

                self.insertor.insert_node(nodesDict[i])
            pass

        for i in notVisitedNodesDict:
            visitedNodesDict[i] = notVisitedNodesDict[i]
            connection = self.currentConnections.connect(notVisitedNodesDict[i])
            connection.query("getKnownNodes", [myNode], self.getAllKnownNodes, [visitedNodesDict, myNode])
            print("visiting address: " + notVisitedNodesDict[i].address + " port: " + str(
                notVisitedNodesDict[i].port) + " user_id: " + str(notVisitedNodesDict[i].user_id))

    pass

    def buildTimeline(self):
        friendsTimeline = Deferred()
        myNodeDeferred = self.getMyNode()
        myFriendsDeferred = self.interrogator.get_known_nodes()
        myTimelineDeferred = self.interrogator.get_recents()
        starter = DeferredList([myNodeDeferred, myFriendsDeferred])
        starter.addCallback(self.__getAllPostsAndComments,
                            int(self.config["peer_default_timeline_days"]), friendsTimeline)
        result = DeferredList([myTimelineDeferred, friendsTimeline])
        return result
        pass

    def __getAllPostsAndComments(self, starter, days, result):
        myNode = starter[0][1]
        myFriends = starter[1][1]

        rootDeferreds = []

        print("****************************************")
        print("Amici a cui richiedo i post:")
        if myFriends is not None:
            printNodesDict(myFriends)

            for i in myFriends:
                c = self.currentConnections.connect(myFriends[i])
                rootDeferreds.append(c.rootDeferred)
                c.rootDeferred.addErrback(self.__getPostsAndCommentsErrback, myNode, myFriends[i])

            rootDeferredList = DeferredList(rootDeferreds)
            rootDeferredList.addCallback(self.__getPostsAndCommentsCallback, myNode, days, result)
        else:
            print('Nessun amico trovato')
        print("****************************************")

        pass

    def __getPostsAndCommentsCallback(self, remoteReferenceList, myNode, days, result):
        timeline = []
        for i in remoteReferenceList:
            if i[0] and (i[1] is not None):
                timeline.append(i[1].callRemote("getPostsAndComments", myNode, days))

        timelineDeferred = DeferredList(timeline)
        timelineDeferred.addCallback(self.__waitForTimeline, result)
        pass

    def __waitForTimeline(self, timeline, result):
        result_timeline = []

        for postList_tuple in timeline:
            for post_package_tuple in postList_tuple[1]:
                print(post_package_tuple[1]).getPost().text_content
                result_timeline.append(post_package_tuple[1])
        result.callback(result_timeline)
        pass

    def __getPostsAndCommentsErrback(self, reason, myNode, friendNotReachable):
        print(reason)
        timeToLive = int(self.config["peer_time_to_live"])
        deferredKnownNodes = self.interrogator.get_known_nodes(myNode)
        deferredKnownNodes.addCallback(self.__forwardToKnownNodes, myNode, myNode, friendNotReachable.user_id,
                                       timeToLive)
        pass

    def resolve(self, uuid):
        resolvingNode = Known_node()
        resolvingNode.user_id = uuid
        deferred = self.getMyNode()
        deferred.addCallback(self.__gotMyNode, resolvingNode)
        pass

    def __gotMyNode(self, myNode, resolvingNode):
        self.__getPostsAndCommentsErrback("", myNode, resolvingNode)
        pass
