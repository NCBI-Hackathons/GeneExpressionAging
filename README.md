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

http://127.0.0.1:8000/api/gen/find

    Input:  {"text": <search-text>}
    Output: {"ok": True/False,
             "result": [ <gene-id-1>, <gene-id-2>, ...]}

http://127.0.0.1:8000/api/timeseries

    Input: {"xaxis": <dimension-name>,
            "series": <dimension-name>,
            "restrictions": <list-of-restrictions>}

    Restriction: [<dimension-name>, <operation>, <parameter>]
    Operation: "eq" or "in"
    Parameter: if operation is "eq", parameter should be a string
               if operation is "in", parameter should be a list of strings

    Example:
    
        {"xaxis": "age",
         "series": "gene",
         "restrictions": [
             ["tissue", "in", ["AM", "LUNG"]],
             ["flu", "eq", "F150"],
             ["gene", "in", ["ENSMUSG00000000088", "ENSMUSG00000000001"]]
             ]}    

    Output:
        {"xvalues": <list-of-floats>,
         "series": [
             {"values": <list-of-floats>,
              "name": <string>}
         ]}
    
    