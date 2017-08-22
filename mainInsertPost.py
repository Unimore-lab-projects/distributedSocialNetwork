from backend.Peer.node import *
import sys


def main():
    print("launched mainInsertPost")
    this = node(sys.argv[1])
    print("launch insert posts")
    this.insertor.insert_post(None, "Post1")
    this.insertor.insert_post(None, "Post2")
    print("end insert posts")

    ##reactor. si chiude entro 10 secondi e termina
    reactor.callLater(4, reactor.stop)

    reactor.run()



if __name__ == '__main__':
    main()
