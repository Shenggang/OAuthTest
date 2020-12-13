import json
import subprocess
import sys
import time
import PIL.ImageTk
import PIL.Image

import app
from core.util import pprint
import core.video_list as video_list
import core.credential_store as credential_store
from core.video_rater import VideoRater
from data.data_portal import DataPortal

from tkinter import *
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


def auth_save_test(number):
    c_store = DataPortal.load_from_plain_text(None)
    for i in range(number):
        c_store.authenticate()
        time.sleep(4)
    DataPortal.dump_into_plain_text(c_store)


def auth_load_test():
    credentials = DataPortal.load_from_plain_text()
    for cred in credentials:
        pprint(cred.to_dict())
    print("--")
    pprint(credentials[-1].to_dict())


def multi_cred_test():
    credentials = DataPortal.load_from_plain_text()
    for cred in credentials:
        youtube = googleapiclient.discovery.build("youtube", "v3", credentials=cred.credential)
        find_me = youtube.channels().list(
            part="snippet",
            mine=True,
        )
        my_detail = find_me.execute()
        pprint(my_detail)


def rater_test():
    credentials = DataPortal.load_from_plain_text()
    vl = video_list.VideoList(api_key)
    vl.load_from_file()
    vr = VideoRater()
    vr.rate_videos(vl, credentials)


def multi_process_auth():
    proc = subprocess.Popen([sys.executable, './authenticate.py'],
                            stdout=subprocess.PIPE)
    stdout = proc.communicate()
    return stdout


def app_test():
    root = Tk()
    app.MainWindow(root)
    root.geometry('800x400')
    root.mainloop()


def image_test():
    root = Tk()
    img = PIL.ImageTk.PhotoImage(PIL.Image.open("unnamed.jpg"))
    panel = Label(root, image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    root.mainloop()


def print_test(*args):
    print(''.join([*args]))


def main():
    #vl_search_test()
    # vl_dump_test()
    # vl_load_test()
    #load_client_secret_test()
    #auth_save_test(6)
    #auth_load_test()
    #multi_cred_test()
    #rater_test()
    #print_test("Let's print", " this ", "out\n")
    app_test()
    #image_test()




if __name__ == "__main__":
    main()
