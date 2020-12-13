from ..credential_store import CredentialStore
from ..video_list import VideoList
from ..video_rater import VideoRater


class GuiCredentialStore(CredentialStore):

    def __init__(self,
                 client_list,
                 callback):
        super(GuiCredentialStore,self).__init__(client_list)
        self.callback = callback

    def print(self, *args):
        # print to listener
        self.callback('end', ''.join([*args, '\n']))


class GuiVideoList(VideoList):

    def __init__(self,
                 api_key,
                 callback):
        super(GuiVideoList, self).__init__(api_key)
        self.callback = callback

    def print(self, *args):
        # print to listener
        self.callback('end', ''.join([*args, '\n']))


class GuiVideoRater(VideoRater):

    def __init__(self,
                 callback):
        self.callback = callback

    def print(self, *args):
        # print to listener
        self.callback('end', ''.join([*args, '\n']))