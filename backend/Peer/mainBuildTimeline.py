

from node import *
import sys


def gotTimeline(timeline):
    print("sono arrivato alla callback")
    for postList in timeline:
	for post in postList[1]:
	    print(post[1])
	    pass
    pass

def main():
    this=node(sys.argv[1])
    timeline=this.buildTimeline()
    timeline.addCallback(gotTimeline)
    reactor.run()


if __name__=='__main__':
    main()
