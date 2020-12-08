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
from google.auth.transport import requests

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_key = 'AIzaSyCxSg3qNKgoA7Nm2pkxu10lNK1NJFuZxV8'
client_id = '832759208130-2b9pkngpukri2g7ckathsgnpm2o45bmg.apps.googleusercontent.com'
client_secret = 'iO5itWBlzz213pXsAoxF3kmF'
token_uri = 'https://oauth2.googleapis.com/token'


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

    f2 = gflow.InstalledAppFlow.from_client_secrets_file(
        secret, scopes=scopes)
    f2.run_local_server(prot=8080, prompt="consent", authorization_prompt_message="")

    cred_json = flow.credentials.to_json()
    pprint(cred_json)

    # cred = credentials.Credentials.from_authorized_user_info(json.loads(cred_json), scopes)
    cred = credentials.Credentials(None, refresh_token=flow.credentials.refresh_token,
                                   token_uri=token_uri, client_id=client_id, client_secret=client_secret)
    cred.refresh(requests.Request())

    pprint(cred.to_json())

    youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=cred)

    request = youtube.search().list(
        part="snippet",
        channelId="UCS9uQI-jC3DE0L4IpXyvr6w",
        fields='items/id/videoId,nextPageToken,pageInfo',
        maxResults=3,
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
