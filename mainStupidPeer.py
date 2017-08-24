from backend.Peer.node import *
import sys
from twisted.internet import reactor


def main():
    this = node(sys.argv[1])
    reactor.listenTCP(this.getPort(), pb.PBServerFactory(this))
    reactor.run()


if __name__ == '__main__':
    main()
