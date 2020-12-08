from googleapiclient import discovery
import io


class VideoList:

    def __init__(self,
                 api_key):
        self._api_key = api_key
        self._api_service_name = "youtube"
        self._api_version = "v3"
        self._video_list = []

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

    @property
    def video_list(self):
        return self._video_list

    def add_entry(self, key, arg):
        self.video_list[key] = arg

    def load_from_list(self, ll):
        self._video_list = ll

    def load_from_file(self, file="video_list.data"):
        self._video_list.clear()
        with io.open(file, "r", encoding="utf-8") as stream:
            self._video_list = stream.read().split(",")

    def dump_list(self, file="video_list.data"):
        with io.open(file, "w", encoding="utf-8") as stream:
            stream.write(",".join(self._video_list))

    def load_next_page(self,
                       next_page=None):
        youtube = discovery.build(self.api_service_name, self.api_version, developerKey=self.api_key)
        request = youtube.search().list(
            part="snippet",
            channelId="UCS9uQI-jC3DE0L4IpXyvr6w",
            fields='items/id/videoId,nextPageToken,pageInfo/totalResults',
            maxResults=50,
            type="video",
            pageToken=next_page
        )
        response = request.execute()
        for vid in response['items']:
            self.video_list.append(vid['id']['videoId'])
        token = response.get('nextPageToken')
        if token:
            self.load_next_page(next_page=token)

    def load_all_pages(self):
        self.video_list.clear()
        self.load_next_page()

    def update(self):
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
        response = request.execute()
        if response['pageInfo']['totalResults'] != len(self.video_list):
            # if length not equal, reconstruct
            self.load_all_pages()
