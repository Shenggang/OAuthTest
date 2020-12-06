# noinspection PyUnresolvedReferences
import core

api_key = 'AIzaSyCxSg3qNKgoA7Nm2pkxu10lNK1NJFuZxV8'


def video_list_test():
    vl = core.video_list.VideoList(api_key)
    vl.update()
    print(len(vl.video_list))
    print(vl.video_list[0:4])


def main():
    video_list_test()


if __name__ == "__main__":
    main()
