# Getting some data
The [recount project](http://bowtie-bio.sourceforge.net/recount/) has some nice counts data from a few publicly availible sequencing projects. Perfect!

Clone the repo
```bash
git clone https://github.com/NCBI-Hackathons/GeneExpressionAging.git
```

Now, lets get a counts file:
```
wget http://bowtie-bio.sourceforge.net/recount/countTables/bottomly_count_table.txt -O ./data/norm_data/norm_all.csv
```
and the metadata
```
wget http://bowtie-bio.sourceforge.net/recount/phenotypeTables/bottomly_phenodata.txt  -O ./data/norm_data/norm_metadata.csv
```


Lets take a look
```
nicholas@nicholinux[GeneExpressionAging] head data/norm_data/norm_all.csv                                                               [ 6:29PM]
gene	SRX033480	SRX033488	SRX033481	SRX033489	SRX033482	SRX033490	SRX033483	SRX033476	SRX033478SRX033479	SRX033472	SRX033473	SRX033474	SRX033475	SRX033491	SRX033484	SRX033492	SRX033485	SRX033493	SRX033486	SRX033494
ENSMUSG00000000001	369	744	287	769	348	803	433	469	585	321	301	461	309	374	781	555	820	294	758	419	857
ENSMUSG00000000003	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	000	0	0	0
ENSMUSG00000000028	0	1	0	1	1	1	0	7	6	1	1	1	1	1	1	211	4	1	5
ENSMUSG00000000031	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	000	0	0	0
ENSMUSG00000000037	0	1	1	5	0	4	0	0	0	0	4	1	1	0	1	211	1	1	2
ENSMUSG00000000049	0	1	0	1	0	0	0	0	0	0	0	0	0	0	0	000	0	0	0
ENSMUSG00000000056	21	46	20	36	12	55	27	44	32	47	40	40	30	27	46	2840	21	52	27	45
ENSMUSG00000000058	15	43	12	34	14	32	19	18	44	22	17	24	29	15	34	2338	17	29	12	28
ENSMUSG00000000078	517	874	340	813	378	860	528	401	584	401	331	431	341	480	930	585	1137	490	1079	565	726
```

Nice!  We have counts by sample, and thats exactly what we want.

```
nicholas@nicholinux[GeneExpressionAging] head data/norm_data/norm_metadata.csv                                                          [ 6:32PM]
sample.id num.tech.reps strain experiment.number lane.number
SRX033480 1 C57BL/6J 6 1
SRX033488 1 C57BL/6J 7 1
SRX033481 1 C57BL/6J 6 2
SRX033489 1 C57BL/6J 7 2
SRX033482 1 C57BL/6J 6 3
SRX033490 1 C57BL/6J 7 3
SRX033483 1 C57BL/6J 6 5
SRX033476 1 C57BL/6J 4 6
SRX033478 1 C57BL/6J 4 7
```
And for each sample, we have some associated information.  Not th emost interesting metadata in this case, but moving on!

## Setting up your server
```
cd webcomponents
npm install bower
npm install polymer-cli
./node_modules/.bin/bower install
#  get the most recent versions of stuff, if it asks
./node_modules/.bin/polymer build
```

Nice.  What you just did was build the static components of the site, which are now ready to be rendered into a beautiful visualizer with django.


```
cd ../webapp
python3.6 manage.py runserver
```

If all is well, you should see the following message:

```
Django version 1.11.4, using settings 'core.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

Go ahead and navigate to [http://127.0.0.1:8000/genvis/test](http://127.0.0.1:8000/genvis/test).  You should see your brand new gene expression viewer!
