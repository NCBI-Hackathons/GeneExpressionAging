from fabric.api import cd, env, task, local, run, settings
import json
import requests


@task
def gen_find(text):
    value = {'text': text}
    r = requests.post("http://127.0.0.1:8000/api/gen/find", json=value)
    print("Result: {}".format(r.json()))