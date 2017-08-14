from django.shortcuts import render
from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from api.tags import method

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


all_data = pd.DataFrame.from_csv("../data/all_data.csv")
column_components = pd.DataFrame.from_csv("../data/column_components.csv")

def generate_data(xaxis, series, restrictions):
    data = all_data
    columns = column_components
    for field, op, value in restrictions:
        if field == "gene":
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

    if xaxis == "gene":
        xvalues = list(data.index)
        yaxes = sorted(set(columns[series]))
        result = []
        for current in yaxes:
            yindices = columns[columns[series]==current].index
            values = data[yindices]
            mean = list(values.mean(axis=1))
            std = list(values.std(axis=1))
            result.append((mean, std))
        return xvalues, list(zip(yaxes, result))
    
    if series == "gene":
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
        return xvalues, list(zip(yaxes, result))
    
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
        return xvalues, list(zip(yaxes, result))


@method(allowed=['POST'])
def time_series(request):
    body = json.loads(request.body.decode("utf-8"))
    xaxis = body["xaxis"]
    series = body["series"]
    restrictions = body["restrictions"]
    xvalues, series_values = generate_data(xaxis, series, restrictions)
    result = {"xvalues": xvalues,
              "series": [{"name": v[0], "values": v[1]} for v in series_values]}
    return JsonResponse(result, encoder=NumpyEncoder)


MAX_GEN_RESULT = 10

@csrf_exempt
@method(allowed=['POST'])
def gen_find(request):
    body = json.loads(request.body.decode("utf-8"))
    text = body.get("text", "")

    result_values = all_data[[text in s for s in all_data.index]].index.values[0:MAX_GEN_RESULT]

    result = {"ok": True,
              "result": [s for s in result_values]}
    return JsonResponse(result)
