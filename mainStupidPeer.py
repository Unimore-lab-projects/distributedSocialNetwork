

from backend.Peer.node import *
import sys

def main():
    this=node(sys.argv[1])
    reactor.listenTCP(8001, pb.PBServerFactory(this))
    reactor.run()

if __name__=='__main__':
    main()
