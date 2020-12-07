import requests
import google.auth.transport.requests as g_requests
from google.oauth2 import credentials


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
            token_uri = self._client_info['token_uri']
            client_id = self._client_info['client_id']
            client_secret = self._client_info['client_secret']
            cred = credentials.Credentials(None, refresh_token=self._refresh_token, token_uri=token_uri,
                                           client_id=client_id, client_secret=client_secret)
            cred.refresh(requests.Request())
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


class CredentialStore:

    def __init__(self):
        self._credentials = []
        self._id_list = []

    def __getitem__(self, index):
        return self._credentials[index]

    def __len__(self):
        return len(self._credentials)

    def append(self, named_cred):
        idx = self.find_id(named_cred.account_id)
        if idx > -1:
            self._credentials[idx].revoke()
            self._credentials[idx] = named_cred
        else:
            self._credentials.append(named_cred)
            self._id_list.append(named_cred.account_id)

    def find_id(self, acc_id):
        try:
            idx = self._id_list.index(acc_id)
        except ValueError:
            return -1
        return idx

