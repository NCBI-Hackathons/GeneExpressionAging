[![DOI](https://zenodo.org/badge/99953417.svg)](https://zenodo.org/badge/latestdoi/99953417)

![icons](https://github.com/NCBI-Hackathons/GeneExpressionAging/blob/master/webcomponents/tissue_icons/aging_mouse_all_tissue_icons.png)

# GeneExpressionAging

In a rush?  Check out our [QuickStart](https://github.com/NCBI-Hackathons/GeneExpressionAging/blob/master/QuickStart.md) guide!

## Overview

The goal of our project is to leverage web technologies to build a modular gene expression viewer for large-scale, complex experiments.  The data included in this repo is just a sample of what can be achieved with this scheme by using [Django](https://www.djangoproject.com/) and [Polymer](https://www.polymer-project.org/) for optimal performace, ease of use, and consistency.

## Audience

We want people with little to no bioinformatics experience to be able to set up a custom gene expression viewer for their lab's data. We want to provide an interface that allows biologists to get what they need from the data.  Fast.

## Structure

Polymer builds the front end from nice reusable web components. Django serves the website, and also allows access to the data through API calls.

## Requirements

- python3
- npm

# Django
## Installation
In order to install, you should create a virtual env using Python 3 and install the requirements listed on 'requirements.txt':

    $ mkvirtualenv -p `which python3` GeneExpressionAging
    $ pip install -r requirements.txt
    $ cd data; mkdir norm_data; cd norm_data; cp ../norm_data.zip .; unzip norm_data.zip; cd ../../

## Running the server
To run the server:

    $ cd webapp
    $ workon GeneExpressionAging
    $ python manage.py runserver

You can browse:

    http://127.0.0.1:8000/genvis/ideogram

or:

    http://127.0.0.1:8000/index.html


<!-- ## webserver -->

<!-- The server is running on our development AWS instance (if you need access, open an issue to ). In order to connect, use tunneling. -->

## Using screens for running the visualizer on a remote development server

The easiest way to keep the django running on a remote server is to use the `screen` unix tool.  Create a `screen` window, run the django server directly (django runserver) and to detach the window between SSH sessions:

- Create the window:
  Run 'screen' and run the server

- Detach the window:
  On the screen, type "Ctrl" + a + d

You can now close the ssh connection, and django will keep on serving.  To stop it, just ssh back in, reattach the window, and interupt the command.

- Reatach window:
  On the ssh session, type `screen -r`


# Datasets

Dataset structure:
 - Counts file
 - metadata file

### Counts
First column should be a unique list of gene ID's.  subsequent columns should contain normalized counts, having one column per sample.  A header row with sample names is expected.

### Metadata

First column should correspond to the sample names given in the counts csv. Anay additional columns are associated metadata, and can be used to subset the data for visualizations

## A Note on Annotations
Currently, this is geared for mouse genomic data.  We have included a script,
[get_mouse_geneid_map.R](https://github.com/NCBI-Hackathons/GeneExpressionAging/blob/master/backend/get_mouse_geneid_map.R), to create  a mapping file relating ensembl, entrez, and common gene names.



<!-- - <folder> TODO -->

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
             ["flu", "eq", 150],
             ["gene", "in", ["ENSMUSG00000000088", "ENSMUSG00000000001"]]
             ]}

    Output:
        {"ok": True/False,
         "dataset": "mouse_aging",
         "field_values": { "name": <field-value> },
         "xvalues": <list-of-floats>,
         "series": [
             {"values": [ value ],
              "name": <string>}
         ]}

    Field-value: {"truncated": True/False,
                  "values": <list-of-values>}
    value: [ <mean>, <stderr> ]


# Polymer

## Installation
```
cd webcomponents
npm install bower
npm install polymer-cli
./node_modules/bower/bin/bower install
```

##  Building and serving the site
```
./node_modules/.bin/polymer build
#  for testing, not needed when serving the django site
./node_modules/.bin/polymer serve
```

# Contributing

Suppose you want to generate a figure we haven't sorted out.  Please help us out by following these three easy steps!

1) Create a new POST method in the [views.py](https://github.com/NCBI-Hackathons/GeneExpressionAging/blob/master/webapp/api/) file. See [below](./README.md#creating-a-new-post)

2) Define the plotting parameters in [test.js](https://github.com/NCBI-Hackathons/GeneExpressionAging/blob/master/webapp/genvis/static/js/test.js)

3) Submit a pull request so others can use it too!

## Creating a new POST
Here is a sample of a post method, in this case for the time series data.  In short, it is extracting certain features from the request (what to use for the x axis, what the restrictions are, etc), and returning the subset of data needed for the visualization as an array in JSON, to be used by the plotting scripts.
```python
@method(allowed=['POST'])
def time_series(request):
    body = json.loads(request.body.decode("utf-8"))
    dataset_name = body.get("dataset", None)
    dataset = settings.DATASETS.get(dataset_name, None)
    xaxis = body.get("xaxis", None)
    series = body.get("series", None)
    restrictions = body.get("restrictions", [])

    print("*" * 80)
    print("dataset: {}".format(dataset))
    print("xaxis:   {}".format(xaxis))
    print("series:  {}".format(series))
    print("restr:   {}".format(restrictions))
    print("*" * 80)

    if None in [dataset_name, dataset]:
        result = {"ok": False,
                  "message": "dataset not valid"}
        return JsonResponse(result)

    if xaxis is None:
        result = {"ok": False,
                  "message": "xaxis not valid"}
        return JsonResponse(result)

    if series is None:
        result = {"ok": False,
                  "message": "series not valid"}
        return JsonResponse(result)

    field_values, xvalues, series_values = generate_data(dataset, xaxis, series, restrictions)
    result = {"ok": True,
              "dataset": dataset_name,
              "field_values": field_values,
              "xvalues": xvalues,
              "series": [{"name": v[0], "values": v[1]} for v in series_values]}
    return JsonResponse(result, encoder=NumpyEncoder)

```
