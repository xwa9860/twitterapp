#!/usr/bin/env fish
psql -U xinwang -f test.sql

rm -rf migrations
python manager.py db init
python manager.py db migrate
python manager.py db upgrade
