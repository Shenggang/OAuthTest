import json
import io

from core import credential_store


class DataPortal:

    client_list = []
    with open("client_secret.json") as file:
        strings = file.read().split('\n,\n')
        for i in range(len(strings)):
            s = strings[i]
            cs = json.loads(s)
            cs['client_index'] = i
            client_list.append(cs)

    @staticmethod
    def load_from_plain_text(filename="credential_store.data"):
        c_store = credential_store.CredentialStore(DataPortal.client_list)
        if not filename:
            return c_store
        with io.open(filename, 'r', encoding='utf-8') as file:
            cred_list = file.read().split("\n,\n")
            for cred in cred_list:
                if not cred:
                    break
                cred_json = json.loads(cred)
                credential = credential_store.NamedCredential(cred_json['refresh_token'],
                                                              DataPortal.client_list[cred_json['client_index']],
                                                              acc_id=cred_json['account_id'],
                                                              acc_name=cred_json['account_name'],
                                                              profile_image=cred_json['thumbnail'])
                c_store.append(credential)
        return c_store

    @staticmethod
    def dump_into_plain_text(c_store,
                             filename="credential_store.data"):
        with io.open(filename, 'w', encoding='utf-8') as file:
            for cred in c_store:
                file.write(json.dumps(cred.to_dict()))
                file.write("\n,\n")
