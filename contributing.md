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
