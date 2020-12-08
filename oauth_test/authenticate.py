import json
import sys

import google_auth_oauthlib.flow as gflow


def auth(index=0,
         secret="client_secret.json"):
    scopes = ["https://www.googleapis.com/auth/youtube"]
    with open(secret) as file:
        strings = file.read().split('\n,\n')
        client_info = json.loads(strings[index])
    flow = gflow.InstalledAppFlow.from_client_config(
        client_info, scopes=scopes)
    flow.run_local_server(prot=8080, prompt="consent", authorization_prompt_message="")

    return flow.credentials.to_json()


def main():
    args = sys.argv[1:]
    if len(args) == 0:
        sys.stdout.write(auth())
    elif len(args) == 1:
        param1 = int(args[0])
        sys.stdout.write(auth(param1))
    elif len(args) > 1:
        param1 = int(args[0])
        param2 = args[1]
        sys.stdout.write(auth(param1, param2))


if __name__ == "__main__":
    main()
    exit(0)