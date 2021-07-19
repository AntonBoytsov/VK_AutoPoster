import time

from config import *

import vk_api

def two_factor():
    code = input('Enter Two-factor Auth code: ')
    remember_device = True
    return code, remember_device

def main():
    vk_session = vk_api.VkApi(LOGIN, PASSWORD,
                              auth_handler=two_factor,
                              scope=PERMISSIONS)
    vk_session.auth()
    vk = vk_session.get_api()

    file = open('links.txt', 'r')
    result = open('ids.txt', 'w')

    ids = ''
    for line in file.readlines():
        name = line.split('/')[-1]
        id = vk.utils.resolveScreenName(screen_name=name)['object_id']
        print(id, end=',')
        ids += '-' + str(id) + ','
        time.sleep(10)
    result.writelines(ids[:-1])

    file.close()
    result.close()

if __name__ == '__main__':
    main()