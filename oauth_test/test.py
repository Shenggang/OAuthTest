import json

from core.util import pprint
import core.video_list as video_list
import core.credential_store as credential_store
from core.video_rater import VideoRater
import data.data_portal as data_portal

import googleapiclient.discovery

api_key = 'AIzaSyCxSg3qNKgoA7Nm2pkxu10lNK1NJFuZxV8'


def vl_search_test():
    vl = video_list.VideoList(api_key)
    vl.update()
    print(len(vl.video_list))
    print(vl.video_list[0:4])


def vl_dump_test():
    vl = video_list.VideoList(api_key)
    vl.update()
    vl.dump_list()


def vl_load_test():
    vl = video_list.VideoList(api_key)
    vl.load_from_file()
    print(len(vl.video_list))
    print(vl.video_list[0:4])


def load_client_secret_test():
    with open("client_secret.json") as file:
        strings = file.read().split('\n,\n')
        for s in strings:
            cs = json.loads(s)
            print(cs)


def auth_save_test():
    dp = data_portal.DataPortal()
    c_store = dp.load_from_plain_text(None)
    c_store.authenticate()
    dp.dump_into_plain_text(c_store)


def auth_load_test():
    dp = data_portal.DataPortal()
    credentials = dp.load_from_plain_text()
    for cred in credentials:
        pprint(cred.to_dict())


def multi_cred_test():
    dp = data_portal.DataPortal()
    credentials = dp.load_from_plain_text()
    for cred in credentials:
        youtube = googleapiclient.discovery.build("youtube", "v3", credentials=cred.credential)
        find_me = youtube.channels().list(
            part="snippet",
            mine=True,
        )
        my_detail = find_me.execute()
        pprint(my_detail)


def rater_test():
    dp = data_portal.DataPortal()
    credentials = dp.load_from_plain_text()
    vl = video_list.VideoList(api_key)
    vl.load_from_file()
    VideoRater.rate_videos(vl, credentials)



def main():
    #vl_search_test()
    # vl_dump_test()
    # vl_load_test()
    #load_client_secret_test()
    #auth_save_test()
    #auth_load_test()
    #multi_cred_test()
    rater_test()


if __name__ == "__main__":
    main()
