#!/bin/bash


psql -d db_peer1 -U peer1 -h 127.0.0.1 -c "insert into Friends values('cb21a82e-4828-4c80-83cc-a5bdf3efad4e','peer3',1)"
psql -d db_peer1 -U peer1 -h 127.0.0.1 -c "insert into Friends values('6f7cd9bd-31fb-4e7e-9efd-6dc53b0b38b5','peer4',3)"
psql -d db_peer3 -U peer3 -h 127.0.0.1 -c "insert into Posts values('cb21a82e-4828-4c80-83cc-a5bdf3efad4e','','post1',20,to_timestamp(NOW()))"
psql -d db_peer4 -U peer4 -h 127.0.0.1 -c "insert into Posts values('6f7cd9bd-31fb-4e7e-9efd-6dc53b0b38b5','','post2',21,to_timestamp(NOW()))"
psql -d db_peer4 -U peer4 -h 127.0.0.1 -c "insert into Posts values('6f7cd9bd-31fb-4e7e-9efd-6dc53b0b38b5','','post3',22,to_timestamp(NOW()))"
