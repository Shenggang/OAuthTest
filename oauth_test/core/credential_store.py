import requests

import google.auth.transport.requests as g_requests
import google_auth_oauthlib.flow as gflow
from google.oauth2 import credentials
from googleapiclient import discovery


class NamedCredential:

    def __init__(self,
                 refresh_token,
                 client_info,
                 cred=None,
                 acc_id=None,
                 acc_name=None,
                 profile_image=None
                 ):
        self._refresh_token = refresh_token
        self._client_info = client_info
        self._acc_id = acc_id
        self._acc_name = acc_name
        self._cred = cred
        self._pf_image = profile_image

    @property
    def refresh_token(self):
        return self._refresh_token

    @property
    def client_info(self):
        return self._client_info

    @property
    def account_id(self):
        return self._acc_id

    @property
    def account_name(self):
        return self._acc_name

    @property
    def credential(self):
        if not self._cred:
            client_info = self._client_info['web']
            token_uri = client_info['token_uri']
            client_id = client_info['client_id']
            client_secret = client_info['client_secret']
            cred = credentials.Credentials(None, refresh_token=self._refresh_token, token_uri=token_uri,
                                           client_id=client_id, client_secret=client_secret)
            cred.refresh(g_requests.Request())
            self._cred = cred
        elif not self._cred.valid:
            self.refresh()
        return self._cred

    @property
    def profile_image(self):
        return self._pf_image

    def revoke(self):
        if self._refresh_token:
            payload = {"token": self._refresh_token}
            requests.post("https://accounts.google.com/o/oauth2/revoke", data=payload)
        self._refresh_token = None
        self._cred = None

    def refresh(self):
        if self._cred:
            self._cred.refresh(g_requests.Request())

    def to_dict(self):
        mydict = dict()
        mydict['refresh_token'] = self._refresh_token
        mydict['client_index'] = self._client_info['client_index']
        mydict['account_id'] = self._acc_id
        mydict['account_name'] = self._acc_name
        mydict['thumbnail'] = self._pf_image
        return mydict


class CredentialStore:

    def __init__(self,
                 client_list=None):
        self._credentials = []
        self._client_list = client_list
        self._scopes = ["https://www.googleapis.com/auth/youtube"]

    def __getitem__(self, index):
        return self._credentials[index]

    def __len__(self):
        return len(self._credentials)

    @property
    def scopes(self):
        return self._scopes

    @property
    def client_list(self):
        return self._client_list

    @client_list.setter
    def client_list(self, value):
        self._client_list = value

    def append(self, named_cred):
        self._credentials.append(named_cred)

    def delete_at(self, idx):
        self._credentials.remove(self._credentials[idx])

    def authenticate(self, file_number=0):
        flow = gflow.InstalledAppFlow.from_client_config(self._client_list[file_number],
                                                         scopes=self._scopes)
        flow.run_local_server(prot=8080, prompt="consent", authorization_prompt_message="")
        youtube = discovery.build("youtube", "v3", credentials=flow.credentials)

        # find my details
        find_me = youtube.channels().list(
            part="snippet",
            mine=True,
        )
        my_detail = find_me.execute()
        if 'items' not in my_detail:
            return
        my_items = my_detail['items'][0]
        my_id = my_items['id']
        my_name = my_items['snippet']['title']
        my_thumbnail = my_items['snippet']['thumbnails']['default']['url']
        cred = NamedCredential(flow.credentials.refresh_token, self._client_list[file_number],
                               cred=flow.credentials, acc_id=my_id, acc_name=my_name, profile_image=my_thumbnail)
        self.append(cred)
