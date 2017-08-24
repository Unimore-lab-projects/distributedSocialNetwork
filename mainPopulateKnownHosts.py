from backend.Peer.node import *
import sys



def main():
    this = node(sys.argv[1])
    # time.sleep(4)
    this.populateKnownNodes()
    # reactor.listenTCP(this.getPort(), pb.PBServerFactory(this))
    reactor.run()


if __name__ == '__main__':
    main()
