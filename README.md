# GeneExpressionAging

## Installation

In order to install, you should create a virtual env using Python 3 and install the requirements listed on 'requirements.txt':

    $ mkvirtualenv -p `which python3` GeneExpressionAging
    $ pip install -r requirements.txt

To run the server:

    $ cd webapp
    $ workon GeneExpressionAging
    $ python manage.py runserver

You can browse:

    http://127.0.0.1:8000/genvis/test


## REST API

http://127.0.0.1:8000/api/