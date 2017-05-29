

from distributedSocialNetwork.Peer.node import *
import sys

def main():
    this=node(sys.argv[1])
    this.insertor.insert_post(None,"Post1")
    this.insertor.insert_post(None,"Post2")
    reactor.run()

if __name__=='__main__':
    main()
