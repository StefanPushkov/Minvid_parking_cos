import logging
import os


def build_image_path(rel_path):
    return '/var/www/parking/var/media/{}'.format(rel_path)


def get_base_dir_by_name(name):
    path = os.getcwd()
    lastchar = path.find(name) + len(name)
    return os.getcwd()[0:lastchar]


def http_server_url():
    return 'http://' + HTTP_SERVER_ADDRESS + ":" + str(HTTP_SERVER_PORT)


# [HTTP Settings]
HTTP_SERVER_ADDRESS = '127.0.0.1'
HTTP_SERVER_PORT = 741
HTTP_COOKIE = "KfFdxguMgver6kI"
AES_PASSPHRASE = "The magic words are squeamish ossifrage"

# [Project Directory]
PROJECT_DIR = get_base_dir_by_name('carplates_server')

# [Multithreading]
WORKER_AMOUNT = 3

# [Database]
ENABLE_DB = True
DB_PATH = '/opt/carplates_server/data/shots.db'
IMAGE_ROOT_FOLDER = '/opt/carplates_server/data/media'

# [Hungarian DB]
#POSTGRES_DB_URL = '10.1.129.201'
#POSTGRES_DB_USER = 'postgres'
#POSTGRES_DB_PASSWORD = 'postgres'
#POSTGRES_IMAGE_ROOT_FOLDER = '/var/www/parking/var/media'

# [Logging]
LOG_FILE = '/var/log/carplates_server/godfather.log'
LOG_LEVEL = logging.DEBUG
