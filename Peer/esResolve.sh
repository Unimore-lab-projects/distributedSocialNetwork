#!/bin/bash



psql -d db_peer1 -U peer1 -h 127.0.0.1 -c "insert into Known_nodes values('9c634463-e6d7-4be6-a267-6e7e22adab86','127.0.0.1',8001,NOW(),3)"
psql -d db_peer3 -U peer3 -h 127.0.0.1 -c "insert into Known_nodes values('5e242f4c-a1cb-45bc-bb79-2d4b28228663','127.0.0.1',8001,NOW(),4)"
psql -d db_peer4 -U peer4 -h 127.0.0.1 -c "insert into Known_nodes values('7b2546bf-0f33-4453-a2af-78df06808c88','127.0.0.1',8001,NOW(),5)"
