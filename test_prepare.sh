#!/bin/sh
./create_tables.sh
export FLASK_APP=tests
flask run
