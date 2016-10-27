

from node import *
import sys



def main():
    this=node(sys.argv[1])
    #this.populateKnownNodes()
    this.resolve('83c2e8bb-317d-4a68-b441-e14756439a74')
    reactor.run()

if __name__=='__main__':
    main()
