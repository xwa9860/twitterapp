#!/usr/bin/env fish

rm -rf migrations
python manager.py db init
python manager.py db migrate
python manager.py db upgrade
