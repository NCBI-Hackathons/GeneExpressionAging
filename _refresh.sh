#!/bin/bash
# to be run from the project root
# update bower and install, forcing most recent
set -e
cd webcomponents
./node_modules/.bin/bower update -F
./node_modules/.bin/bower install -F

./node_modules/.bin/polymer build

# now for django
cd ../webapp
`which python3` manage.py runserver
