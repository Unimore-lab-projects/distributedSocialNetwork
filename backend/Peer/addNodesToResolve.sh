#!/bin/bash


psql -d db_peer4 -U peer4 -h 127.0.0.1 -c "insert into Known_nodes values('83c2e8bb-317d-4a68-b441-e14756439a74','127.0.0.1',8005,NOW(),3)"
psql -d db_peer4 -U peer4 -h 127.0.0.1 -c "insert into Known_nodes values('4d3da9b3-ec1f-4628-90e5-dba04603331f','127.0.0.1',8006,NOW(),1)"
psql -d db_peer4 -U peer4 -h 127.0.0.1 -c "insert into Known_nodes values('54b8dffd-8011-4c1a-9614-77b25c1e44c7','127.0.0.1',8007,NOW(),4)"
