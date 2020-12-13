import requests
import PIL.ImageTk
import PIL.Image
from io import BytesIO
from threading import Thread

from core.GUI.gui import *
from data.data_portal import DataPortal

from tkinter import *
from tkinter import ttk


def ctrlEvent(event):
    # binds every input key to break unless it's ctrl+c
    if 12 == event.state and event.keysym == 'c':
        return
    else:
        return "break"


class MainWindow:

    def __init__(self, root):
        root.title("桐生可可应援器")
        root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
        self._mainframe.grid(column=0, row=0, sticky=(N, S, W, E))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        for i in range(5):
            self._mainframe.columnconfigure(i, weight=1)
        self._mainframe.rowconfigure(0, weight=1)

        style = ttk.Style(root)
        style.configure('Treeview', rowheight=44)

        self.__initialize_account_entries()
        self._image_list = []
        self.__initialize_log_display()
        self.__initialize_utils()
        self.__initialize_buttons()
        self.__populate_entries()

    def __initialize_account_entries(self):
        self._account_list = ttk.Treeview(self._mainframe, column=('User name', 'User ID', 'Client Index'))
        self._account_list.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, W, E), padx=5, pady=10)

        self._account_list.column('#0', width=60)
        self._account_list.column('User name', anchor='center', width=80)
        self._account_list.heading('User name', text='用户名')
        self._account_list.column('User ID', anchor='center', width=100)
        self._account_list.heading('User ID', text='账号ID')
        self._account_list.column('Client Index', anchor='center', width=50)
        self._account_list.heading('Client Index', text='客户端')

    def __initialize_log_display(self):
        self._log_display = Text(self._mainframe, width=40, height=15)
        self._log_display.grid(column=3, row=0, columnspan=2, sticky=(N, S, W, E), padx=5, pady=10)
        ys = ttk.Scrollbar(self._mainframe, orient='vertical', command=self._log_display.yview)
        self._log_display['yscrollcommand'] = ys.set
        ys.grid(column=5, row=0, sticky=(N, S, W))
        self._log_display.insert('1.0', '============ Initialized =============\n')

        # make widget read-only
        self._log_display.bind("<Key>", lambda e: ctrlEvent(e))

    def __initialize_utils(self):
        with open("api_key.txt") as file:
            api_key = file.read()
            self._video_list = GuiVideoList(api_key, self._log_display.insert)
            self._video_list.load_from_file()
        with open("client_secret.json") as file:
            self._c_store = DataPortal.load_from_plain_text(callback=self._log_display.insert)
        self._rater = GuiVideoRater(self._log_display.insert)

    def __initialize_buttons(self):
        # authenticate
        self._auth_btn = Button(self._mainframe, text="登录", command=self._authenticate)
        self._auth_btn.grid(column=0, row=2)
        # deselect account
        deselect_btn = Button(self._mainframe, text="取消选中", command=self._deselect)
        deselect_btn.grid(column=1, row=2)
        # delete account
        delete_btn = Button(self._mainframe, text="移除账号", command=self._remove_acc)
        delete_btn.grid(column=2, row=2)
        # update video list
        upd_btn = Button(self._mainframe, text="更新视频列表", command=Thread(target=self._video_list.update).start)
        upd_btn.grid(column=3, row=2)
        # rate video
        rate_btn = Button(self._mainframe, text="应援", command=Thread(target=self._rate_vids).start)
        rate_btn.grid(column=4, row=2)

    def __populate_entries(self):
        for cred in self._c_store:
            self._add_entry(cred)

    def _remove_acc(self):
        selected = self._account_list.selection()
        if len(selected) == 0:
            return
        idx = self._account_list.index(selected)
        self._c_store.delete_at(idx)
        self._account_list.delete(selected)

    def _rate_vids(self):
        self._rater.rate_videos(self._video_list, self._c_store)

    def _deselect(self):
        for item in self._account_list.selection():
            self._account_list.selection_remove(item)

    def _authenticate(self):
        self._auth_btn.config(state='disabled')
        if self._c_store.authenticate() == 1:
            self._add_entry(self._c_store[-1])
        self._auth_btn.after(4000, lambda: self._auth_btn.config(state='active'))

    def _add_entry(self, credential):
        response = requests.get(credential.profile_image)
        thumbnail = PIL.Image.open(BytesIO(response.content))
        img = PIL.ImageTk.PhotoImage(thumbnail.resize((44, 44)))
        values = (credential.account_name, credential.account_id, credential.client_index)
        self._image_list.append(img)
        self._account_list.insert('', 'end', credential.account_id, image=img, values=values)

    def _on_close(self):
        # save video list
        self._video_list.dump_list()
        # save credential data
        dp = DataPortal()
        dp.dump_into_plain_text(self._c_store)
        # close window
        self._mainframe.master.destroy()













