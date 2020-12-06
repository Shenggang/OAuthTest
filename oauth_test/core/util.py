import json


def pprint(content, indent=4):
    print(json.dumps(content, indent=indent))
