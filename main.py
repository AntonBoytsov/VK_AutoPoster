import datetime
import time
import os

import vk_api

from post import make_posts
from config import *


def make_time():
    return datetime.datetime.now().strftime("%H:%M:%S")


def two_factor():
    code = input('Enter Two-factor Auth code: ')
    remember_device = True
    return code, remember_device


def main():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD, auth_handler=two_factor, scope=PERMISSIONS, api_version='5.92')
    vk_session.auth()

    posts_path = os.getcwd() + '/posts/'
    posts = make_posts(posts_path)
    print('=' * 40)

    groups = ZOO_GROUPS.split(',')

    for post in posts:
        for group in groups:
            try:
                print('[{}] Uploading files to server vk...'.format(make_time()))
                post.upload_content(vk_session, USER_ID, group)
                print('[{}] Posting to group {}...'.format(make_time(), group))
                post.post(vk_session, group)
                print('[{}] Success! Sleeping for 2 mins...'.format(make_time()))
                time.sleep(120)
            except Exception as err:
                print('[{}] - Error {}'.format(make_time(), err))
            print('-' * 40)


if __name__ == '__main__':
    main()