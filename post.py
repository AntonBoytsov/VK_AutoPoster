import datetime
import os


class ImportContentError(Exception): pass


class Post():
    def __init__(self, time, path):
        self.time = time
        self.__path = path
        self.__photos = []

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        assert isinstance(time, datetime.datetime), "Invalid post time"
        self.__time = time
    
    @property
    def photos(self):
        return self.__photos

    @property
    def path(self):
        return self.__path

    def import_photos(self):                # import content
        files = os.listdir(self.__path)
        if files:
            for file_ in files:
                if file_.endswith('.jpg') or file_.endswith('.png'):
                    self.__photos.append(file_)
        else:
            raise ImportContentError('Folder "{}" is empty'.format(self.__path.split('\\')[-1]))


def get_time(folder):
        try:
            dt = datetime.datetime.strptime(folder, "%d.%m.%y %H.%M")
            return dt
        except:
            raise ValueError('Can not convert "{}" folder to post time'.format(folder))


def make_posts(posts_path):
    posts = []
    for p in os.listdir(posts_path):
        try:
            post = Post( get_time(p), posts_path + p )
            post.import_photos()
            print( 'post in {} - {} objects'.format(post.time, len(post.photos)) )
            posts.append(post)
        except ImportContentError as err:
            print('post in {} - error ({})'.format(post.time, err))
    return posts