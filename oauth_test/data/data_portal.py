import json
import io
import os

from core import credential_store
from core.GUI.gui import GuiCredentialStore


class DataPortal:

    client_list = []
    with open("client_secret.json", 'r') as file:
        strings = file.read().split('\n,\n')
        for i in range(len(strings)):
            s = strings[i]
            cs = json.loads(s)
            cs['client_index'] = i
            client_list.append(cs)

    @staticmethod
    def _produce_none_gui_cs(filename):
        c_store = credential_store.CredentialStore(DataPortal.client_list)
        if not filename:
            return c_store
        if not os.path.isfile(filename):
            return
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
    def _produce_gui_cs(filename, callback):
        c_store = GuiCredentialStore(DataPortal.client_list, callback)
        if not filename:
            return c_store
        if not os.path.isfile(filename):
            return
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
    def load_from_plain_text(filename="credential_store.data", callback=None):
        if not callback:
            return DataPortal._produce_none_gui_cs(filename)
        else:
            return DataPortal._produce_gui_cs(filename, callback)

    @staticmethod
    def dump_into_plain_text(c_store,
                             filename="credential_store.data"):
        if not c_store:
            return
        with io.open(filename, 'w', encoding='utf-8') as file:
            for cred in c_store:
                file.write(json.dumps(cred.to_dict()))
                file.write("\n,\n")
