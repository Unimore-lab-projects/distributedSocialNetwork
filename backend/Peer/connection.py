
from twisted.spread import pb
from twisted.internet import reactor

def getAddressFromNode(node):
    address=node.address
    address=address.split("/")
    return address[0]

class remoteConnection:
    def __init__(self, node):
        self.node=node
        self.clientFactory=pb.PBClientFactory()
        reactor.connectTCP(getAddressFromNode(node), node.port,self.clientFactory)
        pass
    
    def query(self, method, methodArgs=None, callback=None, callbackArgs=None):
        self.rootDeferred=self.clientFactory.getRootObject()
        self.rootDeferred.addCallback(self.__waitForRootObject, method, methodArgs, callback, callbackArgs)
        
        pass
    
    def __waitForRootObject(self, rootRemoteRef, method,  methodArgs, callback, callbackArgs):
        self.deferredObj=rootRemoteRef.callRemote(method, *methodArgs)
        if not callback==None:
            self.deferredObj.addCallback(callback, *callbackArgs)
        return self.deferredObj
        pass
    
#    def getDeferred(self):
#        return self.deferredObj
#        pass
#    
#    def addCallback(self, callback, callbackArgs):
#        self.deferredObj.addCallback(callback, *callbackArgs)
#        pass
