import json


def pprint(content, indent=4):
    print(json.dumps(content, indent=indent))


def handle_http_exception(e):
    print("Error met ", e)
    if "quota" in e.error_details:
        print("Quota exceeded for current client, changing to another client file")
