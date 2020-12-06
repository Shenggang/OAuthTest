
class VideoList:

    def __init__(self,
                 api_key):
        self._api_key = api_key
        self.video_list = dict()

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    def add_entry(self, key, arg):
        self.video_list[key] = arg

    def load_from_dict(self, d):
        self.video_list = d

    def update(self):
        # build request

        # check for length

        # if length not equal, reconstruct