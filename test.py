# -*- coding: utf-8 -*-

# Sample Python code for youtube.channels.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json

import google_auth_oauthlib.flow as gflow
from google.oauth2 import credentials
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_key = 'AIzaSyCxSg3qNKgoA7Nm2pkxu10lNK1NJFuZxV8'


def pprint(content, indent=4):
    print(json.dumps(json.loads(content), indent=indent))


def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    secret = "client_secret.json"

    flow = gflow.InstalledAppFlow.from_client_secrets_file(
        secret, scopes=scopes)
    flow.run_local_server(prot=8080, prompt="consent", authorization_prompt_message="")

    cred_json = flow.credentials.to_json()
    pprint(cred_json)

    cred = credentials.Credentials.from_authorized_user_info(json.loads(cred_json), scopes)

    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials= cred)

    request = youtube.search().list(
        part="snippet",
        channelId="UCS9uQI-jC3DE0L4IpXyvr6w",
        maxResults=50,
        type="video"
    )

    response = request.execute()

    pprint(json.dumps(response))

    find_me = youtube.channels().list(
        part="snippet",
        mine=True
    )

    my_detail = find_me.execute()
    pprint(json.dumps(my_detail))


if __name__ == "__main__":
    main()
