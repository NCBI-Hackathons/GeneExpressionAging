from fabric.api import cd, env, task, local, run, settings
import json
import requests

@task
def heatmap():
    value = {
        "dataset": "mouse_aging", 
        "restrictions": [
            ["tissue", "in", ["AM", "LUNG"]],
            ["flu", "eq", 150],
            ["gene", "in", ["ENSMUSG00000000088", "ENSMUSG00000000001"]]]}
    r = requests.post("http://127.0.0.1:8000/api/heatmap", json=value)
    print("Result: {}".format(r.json()))
    
@task
def timeseries():
    value = {
        "dataset": "mouse_aging", 
        "xaxis": "age",
        "series": "gene",
        "restrictions": [
            ["tissue", "in", ["AM", "LUNG"]],
            ["flu", "eq", 150],
            ["gene", "in", ["ENSMUSG00000000088", "ENSMUSG00000000001"]]]}
    r = requests.post("http://127.0.0.1:8000/api/timeseries", json=value)
    print("Result: {}".format(r.json()))

@task 
def series_detail(serie_name):
    value = {"dataset": "mouse_aging", "serie": serie_name}
    r = requests.post("http://127.0.0.1:8000/api/series/detail", json=value)
    print("Result: {}".format(r.json()))    
@task
def series_find(text):
    value = {"dataset": "mouse_aging", "serie": "gene", "text": text}
    r = requests.post("http://127.0.0.1:8000/api/series/find", json=value)
    print("Result: {}".format(r.json()))