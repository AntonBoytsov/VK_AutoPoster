import datetime
import os

import vk_api


class ImportContentError(Exception): pass


class Post():
    def __init__(self, path):
        self.__path = path
        self.__photos = []
        self.__docs = []
        self.__message = ''
        self.__message_file = None
        self.__attachments = ''
        self.__attachments_file = None
    

    def __len__(self):
        return len(self.__photos) + len(self.__docs)


    def __eq__(self, other):
        return self.__path == other.__path
    

    def __lt__(self, other):
        return self.__path < other.__path


    def import_content(self):
        files = os.listdir(self.__path)

        if files:
            for file_ in files:
                if file_.endswith('.jpg') or file_.endswith('.png') or file_.endswith('.jpeg'):
                    self.__photos.append(file_)
                elif file_.endswith('.gif'):
                    self.__docs.append(file_)
                elif file_.endswith('.txt') and self.__message_file is None:
                    self.__message_file = file_
                elif file_.endswith('.att') and self.__attachments_file is None:
                    self.__attachments_file = file_
        else:
            raise ImportContentError('Folder "{}" is empty'.format(self.__path.split('/')[-1]))
    

    def upload_content(self, vk_session, user_id, group_id):
        upload = vk_api.VkUpload(vk_session)
        self.__attachments = ''
        self.__message = ''
        if self.__photos:
            photos_path = [self.__path + '/' + photo for photo in self.__photos]
            photos = upload.photo_wall(photos_path, user_id, group_id)
            atcms = ['photo' + str(photo['owner_id']) + '_' + str(photo['id']) for photo in photos]
            atcms = ','.join(atcms)
            self.__attachments = ','.join( (self.__attachments, atcms) )

        if self.__docs:
            for doc in self.__docs:
                path = self.__path + '/' + doc
                dct = upload.document_wall(path, doc[:-4])
                atcmt = 'doc' + str(dct[0]['owner_id']) + '_' + str(dct[0]['id'])
                self.__attachments = ','.join( (self.__attachments, atcmt) )

        if self.__attachments_file:
            with open(self.__path + '/' + self.__attachments_file, 'rb') as f:
                for line in f:
                    self.__attachments = ','.join( (self.__attachments, line.decode('utf-8')) )

        if self.__message_file:
            with open(self.__path + '/' + self.__message_file, 'rb') as f:
                for line in f:
                    self.__message += line.decode('utf-8')
            

    def post(self, vk_session, owner_id):
        vk = vk_session.get_api()
        response = vk.wall.post(owner_id=owner_id,
                                from_group=0,
                                message=self.__message,
                                attachments=self.__attachments)        
        return response


def make_posts(posts_path):
    posts = []
    for p in os.listdir(posts_path):
        try:
            post = Post(posts_path + p)
            post.import_content()
            posts.append(post)
        except Exception as err:
            print('Error ({})'.format(err))
    return posts
