import json


def pprint(content, indent=4):
    print(json.dumps(json.loads(content), indent=indent))
