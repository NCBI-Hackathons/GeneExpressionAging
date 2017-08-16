from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder

from django.views.decorators.csrf import csrf_exempt
from api.tags import method
from core import settings

import json
import numpy as np
import pandas as pd


class NumpyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyEncoder, self).default(obj)


all_data = pd.DataFrame.from_csv("../data/norm_data/norm_all.csv")
column_components = pd.DataFrame.from_csv("../data/norm_data/norm_metadata.csv")
mouse_genemap = pd.read_csv("../data/mouse_geneid_map_GRCm38_081517.csv", dtype=str)

def generate_data(dataset, xaxis, series, restrictions):
    data = all_data
    columns = column_components
    for field, op, value in restrictions:
        if field == dataset["index_name"]:
            if op == "eq":
                data = data.loc[value]
            elif op == "in":
                data = data.loc[value]
            else:
                raise Exception("op {} is not valid for {}".format(op, field))
        elif op == "eq":
            columns = columns[columns[field]==value]
        elif op == "in":
            columns = columns[columns[field].isin(value)]
        else:
            raise Exception("op {} is not valid for {}".format(op, field))

    def calculate_field_values(values):
        if len(values) > 10:
            return {"truncated": True, "values": values[0:10]}
        else:
            return {"truncated": False, "values": values}            

    field_values = {}
    field_values[dataset["index_name"]] = calculate_field_values(sorted(data.index))
    for serie_name in dataset["series"].keys():
        field_values[serie_name] = calculate_field_values(sorted(columns[serie_name].unique()))

    if xaxis == dataset["index_name"]:
        xvalues = list(data.index)
        yaxes = sorted(set(columns[series]))
        result = []
        for current in yaxes:
            yindices = columns[columns[series]==current].index
            values = data[yindices]
            mean = list(values.mean(axis=1))
            std = list(values.std(axis=1))
            result.append((mean, std))
        return field_values, xvalues, list(zip(yaxes, result))
    
    if series == dataset["index_name"]:
        xvalues = sorted(set(columns[xaxis].dropna()))
        yaxes = sorted(set(data.index))
        result = []
        for current in data.index:
            yvalues = []
            for xvalue in xvalues:
                yindices = columns[columns[xaxis]==xvalue].index
                values = data[yindices].loc[current]
                mean = values.mean()
                std = values.std()
                yvalues.append((mean, std))
            result.append(yvalues)
        return field_values, xvalues, list(zip(yaxes, result))
    
    else:
        xvalues = sorted(set(columns[xaxis].dropna()))
        yaxes = sorted(set(columns[series].dropna()))
        result = []
        for yaxis in yaxes:
            yvalues = []
            for current in xvalues:
                values = data[columns[(columns[series]==yaxis) & (columns[xaxis]==current)].index].stack()
                mean = values.mean()
                std = values.std()
                yvalues.append((mean, std))
            result.append(yvalues)
        return field_values, xvalues, list(zip(yaxes, result))


@csrf_exempt
@method(allowed=['POST'])
def heatmap(request):
    body = json.loads(request.body.decode("utf-8"))
    dataset_name = body.get("dataset", None)
    dataset = settings.DATASETS.get(dataset_name, None)
    restrictions = body.get("restrictions", [])

    if None in [dataset_name, dataset]:
        result = {"ok": False,
                  "message": "dataset not valid"}
        return JsonResponse(result)

    features = all_data.index[0:20]
    values = all_data.loc[features].transpose().corr()

    labels = list(values.index)
    result = []
    for row in values.iterrows():
        _, values = row
        result.append(list(values))

    result = {
        "ok": True,
        "labels": labels,
        "z": result
    }
    return JsonResponse(result)


@csrf_exempt
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


MAX_SERIE_DETAIL_VALUES = 25

@csrf_exempt
@method(allowed=['POST'])
def series_detail(request):
    body = json.loads(request.body.decode("utf-8"))
    dataset_name = body.get("dataset", None)
    dataset = settings.DATASETS.get(dataset_name, None)
    serie = body.get("serie", None)

    if None in [dataset_name, dataset]:
        result = {"ok": False,
                  "message": "dataset not valid"}
        return JsonResponse(result)

    if serie is None:
        result = {"ok": False,
                  "message": "serie not valid"}
        return JsonResponse(result)
    
    if serie == dataset["index_name"]:
        result = {"ok": True,
                  "wizard": "gene_wizard"}
        return JsonResponse(result)

    wizard = dataset["series"][serie]["wizard"]
    result = {"ok": True,
              "values": sorted(column_components[serie].unique())[0:MAX_SERIE_DETAIL_VALUES],
              "wizard": wizard}
    return JsonResponse(result)


MAX_GENE_RESULT = 10

@csrf_exempt
@method(allowed=['POST'])
def series_find(request):
    body = json.loads(request.body.decode("utf-8"))
    dataset_name = body.get("dataset", None)
    dataset = settings.DATASETS.get(dataset_name, None)
    serie = body.get("serie", None)
    text = body.get("text", "")

    if None in [dataset_name, dataset]:
        result = {"ok": False,
                  "message": "dataset not valid"}
        return JsonResponse(result)

    if serie is None:
        result = {"ok": False,
                  "message": "serie not valid"}
        return JsonResponse(result)
    
    if serie == dataset["index_name"]:
        data = mouse_genemap[
            (mouse_genemap["ensembl_gene_id"].notnull() & mouse_genemap["ensembl_gene_id"].str.contains(text)) |
            (mouse_genemap["external_gene_name"].notnull() & mouse_genemap["external_gene_name"].str.contains(text)) |
            (mouse_genemap["entrezgene"].notnull() & mouse_genemap["entrezgene"].str.contains(text))]    
        result_values = []
        for i, row in enumerate(data[["ensembl_gene_id", "external_gene_name", "entrezgene"]].iterrows()):
            if i > MAX_GENE_RESULT:
                break
            index, (ensembl_gene_id, external_gene_name, entrezgene) = row
            result_values.append((ensembl_gene_id, external_gene_name, entrezgene))

        result = {"ok": True,
                  "dataset": dataset_name,
                  "result": [list(s) for s in result_values]}
        print("*" * 80)
        print("result: {}".format(result))
        print("*" * 80)
        return JsonResponse(result)

    else:
        result = {"ok": False,
                  "message": "not implemented"}
        return JsonResponse(result)