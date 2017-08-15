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


## webserver

The server is running on the server (ask for the IP). In order to connect, use tunneling.

## screens

The django server is running directly (django runserver) and using 'screen' to detach the window between SSH sessions:

- Create the window:
  Run 'screen' and run the server

- Detach the window:
  On the screen, type "Ctrl" + a + d

- Reatach window:
  On the ssh session, type `screen -r`


## Datasets

Dataset structure:

- <folder> TODO

## REST API

http://127.0.0.1:8000/api/series/find

    Input:  {"dataset": "mouse_aging",
             "serie": <serie-name>,
             "text": <search-text>}
    Output: {"ok": True/False,
             "dataset": "mouse_aging",
             "result": [ <result-1>, <result-2>, ...]}

http://127.0.0.1:8000/api/timeseries

    Input: {"dataset": "mouse_aging",   // We only have this
            "xaxis": <dimension-name>,
            "series": <dimension-name>,
            "restrictions": <list-of-restrictions>}

    Restriction: [<dimension-name>, <operation>, <parameter>]
    Operation: "eq" or "in"
    Parameter: if operation is "eq", parameter should be a string
               if operation is "in", parameter should be a list of strings

    Example:
    
        {"dataset": "mouse_aging",
         "xaxis": "age",
         "series": "gene",
         "restrictions": [
             ["tissue", "in", ["AM", "LUNG"]],
             ["flu", "eq", "F150"],
             ["gene", "in", ["ENSMUSG00000000088", "ENSMUSG00000000001"]]
             ]}    

    Output:
        {"dataset": "mouse_aging",
         "xvalues": <list-of-floats>,
         "series": [
             {"values": <list-of-floats>,
              "name": <string>}
         ]}
    

