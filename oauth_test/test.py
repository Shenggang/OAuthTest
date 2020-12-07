# noinspection PyUnresolvedReferences
from core import video_list

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


def main():
    # vl_search_test()
    vl_dump_test()
    vl_load_test()


if __name__ == "__main__":
    main()
