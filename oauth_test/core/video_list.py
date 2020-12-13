import io
import os

from .util import handle_http_exception

from googleapiclient import discovery
import googleapiclient.errors as google_errors


class VideoList:

    def __init__(self,
                 api_key):
        self._api_key = api_key
        self._api_service_name = "youtube"
        self._api_version = "v3"
        self._video_list = []

    def __getitem__(self, index):
        return self._video_list[index]

    def __len__(self):
        return len(self._video_list)

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value

    @property
    def api_service_name(self):
        return self._api_service_name

    @property
    def api_version(self):
        return self._api_version

    def add_entry(self, key, arg):
        self.video_list[key] = arg

    def load_from_list(self, ll):
        self._video_list = ll

    def load_from_file(self, file="video_list.data"):
        self.print("Loading Video list from save file")
        self._video_list.clear()
        if not os.path.isfile(file):
            return
        with io.open(file, "r", encoding="utf-8") as stream:
            self._video_list = stream.read().split(",")
            if self._video_list[0] == '':
                self._video_list = []
        self.print("Loaded %i videos" % len(self._video_list))

    def dump_list(self, file="video_list.data"):
        with io.open(file, "w", encoding="utf-8") as stream:
            stream.write(",".join(self._video_list))

    def load_next_page_into(self,
                            video_list,
                            next_page=None):
        if not next_page:
            self.print("Loading videos from first page")
        else:
            self.print("Loading videos, page token = ", next_page)

        youtube = discovery.build(self.api_service_name, self.api_version, developerKey=self.api_key)
        request = youtube.search().list(
            part="snippet",
            channelId="UCS9uQI-jC3DE0L4IpXyvr6w",
            fields='items/id/videoId,nextPageToken,pageInfo/totalResults',
            maxResults=50,
            type="video",
            pageToken=next_page
        )
        try:
            response = request.execute()
        except google_errors.HttpError as e:
            handle_http_exception(e, self.print)
            self.print('Loading video list failed.')
            return None
        for vid in response['items']:
            video_list.append(vid['id']['videoId'])
        token = response.get('nextPageToken')
        if token:
            return self.load_next_page_into(video_list, next_page=token)
        return video_list

    def load_all_pages(self):
        self.print("Loading all pages")
        vl = self.load_next_page_into([])
        if not vl:
            self._video_list = vl
        self.print("Loaded %d videos" % len(self._video_list))

    def update(self):
        self.print("Updating Video List")
        # build request
        youtube = discovery.build(self.api_service_name, self.api_version, developerKey=self.api_key)
        request = youtube.search().list(
            part="snippet",
            channelId="UCS9uQI-jC3DE0L4IpXyvr6w",
            fields='items/id/videoId,nextPageToken,pageInfo/totalResults',
            maxResults=1,
            type="video"
        )
        # check for length
        try:
            response = request.execute()
        except google_errors.HttpError as e:
            handle_http_exception(e, self.print)
            self.print('Updating video list failed.')
            return
        if response['pageInfo']['totalResults'] != len(self._video_list):
            # if length not equal, reconstruct
            self.load_all_pages()

