[![DOI](https://zenodo.org/badge/99953417.svg)](https://zenodo.org/badge/latestdoi/99953417)

![icons](https://github.com/NCBI-Hackathons/GeneExpressionAging/blob/master/screenshots/aging_mouse_all_tissue_icons.png)

# GeneExpressionAging

In a rush?  Check out our [QuickStart](https://github.com/NCBI-Hackathons/GeneExpressionAging/blob/master/QuickStart.md) guide!

## Try it out!
An [interactive ideogram showing gene expression over time](https://ncbi-hackathons.github.io/GeneExpressionAging/ideogram) is one of several modular components included in our template.  Check it out, and then install our other modules to experiment with your own data!

## Overview

The goal of our project is to leverage web technologies to build a modular gene expression viewer for large-scale, complex experiments.  The data included in this repo is just a sample of what can be achieved with this scheme by using [Django](https://www.djangoproject.com/) and [Polymer](https://www.polymer-project.org/) for optimal performace, ease of use, and consistency.

## Screenshots
[Here are some screenshots](https://github.com/NCBI-Hackathons/GeneExpressionAging/blob/master/screenshots.md) of our example app.

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
 - .csv counts file
 - .csv metadata file

### Counts
First column should be a unique list of gene ID's.  subsequent columns should contain normalized counts, having one column per sample.  A header row with sample names is expected.

Example:
```
,M01_Lung_24M_F0_1,M02_Lung_24M_F0_2,M03_Lung_24M_F0_3,M04_Lung_18M_F0_1,M05_Lung_18M_F0_2,M06_Lung_18M_F0_3
ENSMUSG00000000001,6.174532,6.371318,6.344995,6.349766,6.671662,6.131033
ENSMUSG00000000028,4.117880,3.801730,4.066170,3.700697,3.881500,4.213005
ENSMUSG00000000031,5.607145,5.589857,5.510131,5.550341,5.569334,5.652838
ENSMUSG00000000037,3.562216,3.872689,4.099348,3.675672,3.940676,4.227414
ENSMUSG00000000049,7.000757,7.821398,8.292461,7.531357,8.534585,6.471823
ENSMUSG00000000056,5.676189,5.843910,5.796951,5.924107,5.656007,5.631688
```

### Metadata

First column should correspond to the sample names given in the counts csv. Anay additional columns are associated metadata, and can be used to subset the data for visualizations

Example:
```
,animal_id,flu,age,replicate,tissue
M01_Lung_24M_F0_1,1,0,24,1,Lung
M02_Lung_24M_F0_2,2,0,24,2,Lung
M03_Lung_24M_F0_3,3,0,24,3,Lung
M04_Lung_18M_F0_1,4,0,18,1,Lung
M05_Lung_18M_F0_2,5,0,18,2,Lung
M06_Lung_18M_F0_3,6,0,18,3,Lung
```

## A note on annotations
Currently, this is geared for mouse genomic data.  We have included a script,
[get_mouse_geneid_map.R](https://github.com/NCBI-Hackathons/GeneExpressionAging/blob/master/backend/get_mouse_geneid_map.R), to create a mapping file relating Ensembl, Entrez, and common gene names.



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
Suppose you want to generate a figure we haven't sorted out. [Here is our guide](https://github.com/NCBI-Hackathons/GeneExpressionAging/blob/master/contributing.md) if you want to help add it!

# Authors
- [Helio](https://amaral.northwestern.edu/people/heltena/)
- [Ziyou Ren](mailto:ziyou.ren@northwestern.edu)
- [Nicholas Waters](https://github.com/nickp60/)
- [Katrina Kalantar](https://github.com/katrinakalantar)
- [Marcin Domagalski](https://github.com/mdomagalski)
- [Paul Reyfman](mailto:paul.reyfman@northwestern.edu)
- [Shuaicheng "Freeman" Wang](https://github.com/wangtulao)
- [Eric Weitz](https://github.com/eweitz)
