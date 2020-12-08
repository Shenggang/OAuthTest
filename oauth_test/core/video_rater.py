from .video_list import VideoList
from .credential_store import *

import googleapiclient.discovery


class VideoRater:

    @staticmethod
    def rate_videos(video_list, credential_store):
        assert isinstance(video_list, VideoList)
        assert isinstance(credential_store, CredentialStore)

        for cred in credential_store:
            youtube = googleapiclient.discovery.build("youtube", "v3", credentials=cred.credential)
            for vid in video_list:
                request = youtube.videos().getRating(
                    id=vid
                )
                rate = request.execute()
                print("Video = ", vid, "is ", rate['items'][0]['rating'])
                if rate['items'][0]['rating'] != "dislike":
                    request = youtube.videos().rate(
                        id=vid,
                        rating="dislike"
                    )
                    print(request.execute())
            print(cred.account_name, "  is Done")

