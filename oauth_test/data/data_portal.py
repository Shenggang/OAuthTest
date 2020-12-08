import json
import io

from core import credential_store


class DataPortal:

    def __init__(self):
        with open("client_secret.json") as file:
            strings = file.read().split('\n,\n')
            self._client_list = []
            for i in range(len(strings)):
                s = strings[i]
                cs = json.loads(s)
                cs['client_index'] = i
                self._client_list.append(cs)
        self._credential_store = credential_store.CredentialStore(self._client_list)

    @property
    def credentials(self):
        return self._credential_store

    def load_from_plain_text(self,
                             filename="credential_store.data"):
        with io.open(filename, 'r', encoding='utf-8') as file:
            cred_list = file.read().split("\n,\n")
            for cred in cred_list:
                if not cred:
                    break
                cred_json = json.loads(cred)
                credential = credential_store.NamedCredential(cred_json['refresh_token'],
                                                              self._client_list[cred_json['client_index']],
                                                              acc_id=cred_json['account_id'],
                                                              acc_name=cred_json['account_name'],
                                                              profile_image=cred_json['thumbnail'])
                self._credential_store.append(credential)

    def dump_into_plain_text(self,
                             filename="credential_store.data",
                             c_store=None):
        if not c_store:
            c_store = self._credential_store
        with io.open(filename, 'a', encoding='utf-8') as file:
            for cred in c_store:
                file.write(json.dumps(cred.to_dict()))
                file.write("\n,\n")
