#!/bin/bash

dropdb db_peer1
dropdb db_peer2
dropdb db_peer3
dropdb db_peer4


createdb -O peer1 db_peer1
createdb -O peer2 db_peer2
createdb -O peer3 db_peer3
createdb -O peer4 db_peer4


psql -d db_peer1 -U peer1 -h 127.0.0.1 -f $1
psql -d db_peer2 -U peer2 -h 127.0.0.1 -f $1
psql -d db_peer3 -U peer3 -h 127.0.0.1 -f $1
psql -d db_peer4 -U peer4 -h 127.0.0.1 -f $1


psql -d db_peer2 -U peer2 -h 127.0.0.1 -c "insert into My_user values('e9ef0227-a8dd-40f5-b3d6-83060f2d3cb6','peer2',1)"

psql -d db_peer1 -U peer1 -h 127.0.0.1 -c "insert into Known_nodes values('e9ef0227-a8dd-40f5-b3d6-83060f2d3cb6','127.0.0.1',8001,NOW(),2)"
psql -d db_peer3 -U peer3 -h 127.0.0.1 -c "insert into Known_nodes values('e9ef0227-a8dd-40f5-b3d6-83060f2d3cb6','127.0.0.1',8001,NOW(),2)"
psql -d db_peer4 -U peer4 -h 127.0.0.1 -c "insert into Known_nodes values('e9ef0227-a8dd-40f5-b3d6-83060f2d3cb6','127.0.0.1',8001,NOW(),2)"
