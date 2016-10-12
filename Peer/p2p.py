
from twistar.dbconfig.base import InteractionBase
from twisted.python import log
from twisted.spread import pb
from twisted.internet import reactor


from distributedSocialNetwork.DbManagement.db_insertor import *
from distributedSocialNetwork.DbManagement.db_openConnection import *
from distributedSocialNetwork.DbManagement.debug_messages import *
from random import randint
from datetime import datetime

from distributedSocialNetwork.DbManagement.tables import *

import sys

class peer(pb.Root):
    
    uid=""
    address=""
    port=0
    knownHosts=dict()
    
    def __init__(self,  portNumber, filename, uid, address, port):
        self.uid=uid
        self.address=address
        self.port=port
        self.populateKnownHosts(filename)
        reactor.listenTCP(portNumber, pb.PBServerFactory(self))
        print("listening on port "+str(portNumber))
        self.queryKnownHosts(self.knownHosts, dict())

    def populateKnownHosts(self, filename):
        in_file = open(filename,"r")
        text = in_file.read()
        in_file.close()
        text=text.split('\n')
        text.pop()
        for line in text:
            couple=line.split(',')
            print(couple)
            self.knownHosts[couple[0]]=couple[1]
        print(self.knownHosts)
        
    def remote_getKnownHosts(self, uid, address, port):
        print("connessione in ingresso, indirizzo: "+address+" porta: "+port)
        if not self.knownHosts.has_key(uid):
            self.knownHosts[uid]=address+":"+port
        return self.knownHosts
    
    def connect(self, ipAddress, remotePortNumber):
        clientFactory=pb.PBClientFactory()
        reactor.connectTCP(ipAddress, remotePortNumber,clientFactory)
        return clientFactory.getRootObject()
    
    
    def queryKnownHosts(self, hosts, visitedHosts):
        
        notVisitedHosts=dict()
        
        for i in hosts:
            if((not visitedHosts.has_key(i))and(not i==self.uid)) :
                visitedHosts[i]=hosts[i]
                notVisitedHosts[i]=hosts[i]
                self.knownHosts[i]=hosts[i]
        
        for i in notVisitedHosts:
            value=notVisitedHosts[i].split(':')
            address=value[0]
            port=value[1]
            deferredObject=self.connect(address, int(port))
            deferredObject.addCallback(self.getHostsList, i, visitedHosts)
            print("visiting "+str(i))
        
    def getHostsList(self, rootObject, hostUid,  visitedHosts):
        print("ottenuto oggetto remoto"+str(hostUid))
        remoteKnownHosts=rootObject.callRemote("getKnownHosts", self.uid, self.address, self.port)
        remoteKnownHosts.addCallback(self.queryKnownHosts, visitedHosts)
    
    def queryKnownHostsErrback(self, obj):
        print("host non raggiungibile")

        
        

#sintassi: pyton p2p.py uid address port filename
p=peer(int(sys.argv[3]), sys.argv[4], sys.argv[1], sys.argv[2], sys.argv[3])
reactor.run()
