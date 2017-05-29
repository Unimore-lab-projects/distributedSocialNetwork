

from backend.Peer.node import *
import sys

def main():
    this=node('peer2.config')
    reactor.listenTCP(8001, pb.PBServerFactory(this))
    reactor.run()

if __name__=='__main__':
    main()
