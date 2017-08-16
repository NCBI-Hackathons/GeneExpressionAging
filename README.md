# GeneExpressionAging

## Overview

The goal of our project is to leverage web technologies to build a modular gene expression viewer for large-scale, complex experiments.  The data included in this repo is just a sample of what can be achieved with this scheme. By using [Django](https://www.djangoproject.com/) and [Polymer](https://www.polymer-project.org/) for optimal performace, ease of use, and consistency.

## Audience

We want people with little to no bioinformatics experience to be able to set up a custom gene expression viewer for their lab's data. We want to provide an interface that allows biologists to get what they need from the data.  Fast.

## Structure

Django serves the data through API calls, and Polymer builds the front end from nice reusable web components.

## Requirements

- python3
- npm

# Django
##Installation
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

http://127.0.0.1:8000/api/series/detail

    Input: {"dataset": "mouse_aging",
            "serie": <serie-name>}
    Output: {"ok": True/False,
             "values": <list-of-values>,
             "wizard": <wizard-name>}

If the serie has a lot of values, the output will not have "values" field.

http://127.0.0.1:8000/api/series/find

    Input:  {"dataset": "mouse_aging",
             "serie": <serie-name>,
             "text": <search-text>}
    Output: {"ok": True/False,
             "dataset": "mouse_aging",
             "result": [ <result-1>, <result-2>, ...]}

    result: [<ensembl_gene_id>, <external_gene_name>, <entrezgene>]  (yes, an array of three element for each gene)


http://127.0.0.1:8000/api/timeseries

    Input: {"dataset": "mouse_aging",   // We only have this
            "field_values": { "name": <field-value> },
            "xaxis": <dimension-name>,
            "series": <dimension-name>,
            "restrictions": <list-of-restrictions>}

    Field-value: {"truncated": True/False,
                  "values": <list-of-values>}
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
             ["flu", "eq", 150],
             ["gene", "in", ["ENSMUSG00000000088", "ENSMUSG00000000001"]]
             ]}

    Output:
        {"dataset": "mouse_aging",
         "field_values": {
             "flu": {"truncated": False, 
                     "values": [150.0]},
             "gene": {"truncated": False,
                      "values": ["ENSMUSG00000000001", "ENSMUSG00000000088"]},
             "tissue": {"truncated": False, 
                        "values": ["AM"]}
         },
         "xvalues": <list-of-floats>,
         "series": [
             {"values": [ value ],
              "name": <string>}
         ]}

    value: [ <mean>, <stderr> ]

# Polymer


## Installation
```
npm install bower
npm install polymer-cli
bower install
```

##  Building and serving the site
```
./node_modules/.bin/polymer build
./node_modules/.bin/polymer serve
```
