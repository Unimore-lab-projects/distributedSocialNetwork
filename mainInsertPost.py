

from backend.Peer.node import *
import sys

def main():
    print("launched mainInsertPost")
    this=node(sys.argv[1])
    print("launch insert posts")
    this.insertor.insert_post(None,"Post1")
    this.insertor.insert_post(None,"Post2")
    print("end insert posts")
    reactor.run()

if __name__=='__main__':
    main()
