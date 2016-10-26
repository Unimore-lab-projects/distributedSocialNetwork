

from node import *
import sys

def main():
    this=node(sys.argv[1])
    reactor.run()

if __name__=='__main__':
    main()
