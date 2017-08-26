#!/bin/bash

#sudo source ~/.bashrc
pip3 install virtualenv virtualenvwrapper
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
source `which virtualenvwrapper.sh`
mkvirtualenv -p `which python3` GeneExpressionAging
cd /opt/GeneExpressionAging/
pip3 install -r requirements.txt

cd data
mkdir norm_data
cd norm_data
cp ../norm_data.zip .
unzip norm_data.zip
cd ../../

cd webapp
workon GeneExpressionAging
python3 manage.py runserver 0.0.0.0:8000
