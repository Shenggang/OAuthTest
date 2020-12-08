class VideoRater:

    def __init__(self,
                 v_list=None,
                 c_store=None):
        """
        Args:
            v_list (VideoList object): Stores the id of videos to be rated.
            c_store (Credential_Store object): Store the list of credentials.
        """
        self._v_list = v_list
        self._c_store = c_store

    @property
    def video_list(self):
        return self._v_list

    @video_list.setter
    def video_list(self, value):
        self._v_list = value

    @property
    def credential_store(self):
        return self._c_store

    @credential_store.setter
    def credential_store(self, value):
        self._c_store = value




