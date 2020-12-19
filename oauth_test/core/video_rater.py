from .video_list import VideoList
from .credential_store import *
from .util import handle_http_exception
from .quota import QuotaCounter

import googleapiclient.discovery
import googleapiclient.errors as google_errors


class VideoRater:

    def print(self, *args):
        print(*args)

    def rate_videos(self, video_list, credential_store):
        for cred in credential_store:
            youtube = googleapiclient.discovery.build("youtube", "v3", credentials=cred.credential)
            self.print("Processing ", cred.account_name)
            for vid in video_list:
                client_index = cred.client_index
                quota = QuotaCounter.get_quota_of(client_index)
                if quota < 51:
                    self.print("Client %d has run out of quota" % client_index)
                    break
                QuotaCounter.reduce_quota_of(client_index, 1)
                request = youtube.videos().getRating(
                    id=vid
                )
                try:
                    rate = request.execute()
                except google_errors.HttpError as e:
                    handle_http_exception(e, self.print)
                    break
                self.print("Video = ", vid, "is ", rate['items'][0]['rating'])
                if rate['items'][0]['rating'] != "dislike":
                    request = youtube.videos().rate(
                        id=vid,
                        rating="dislike"
                    )
                    QuotaCounter.reduce_quota_of(client_index, 50)
                    try:
                        response = request.execute()
                        if response == "":
                            self.print(vid, " Done")
                    except google_errors.HttpError as e:
                        handle_http_exception(e, self.print)
                        break
        self.print("Rating process finished")

