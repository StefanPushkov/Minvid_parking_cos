# Client that makes request to a production server

import base64
import random
import string

import requests
import json
import logging

import configs.pentagon as config
from aes_cipher import AESCipher

cipher = AESCipher(config.AES_PASSPHRASE)


def make_request(image, id, daytime, is_last=False):
    img_path = '/root/Projects/Final_Final/Godfather/cars/' + '{}'.format(daytime) + '_{}'.format(id) + '.jpg'

    with open(img_path, 'wb') as imgfile:
        imgfile.write(image)

    image_string = base64.b64encode(image).decode('utf-8')

    json_request = {'cookie': config.HTTP_COOKIE, 'image': image_string, 'img_path': img_path}
    if is_last:
        json_request['last_image'] = True
    json_string = json.dumps(json_request)
    encr_request = cipher.encrypt(json_string)

    try:
        r = requests.post(config.http_server_url(), data=encr_request, timeout=10)
    except Exception as e:
        logging.error('Error communicating with Godfather, ERR: %s' % str(e))
        return None

    try:
        if r.text == '':
            return
        response = cipher.decrypt(r.content)

        response_json = json.loads(response)
        if response_json['cookie'] != config.HTTP_COOKIE:
            raise ValueError('HTTP cookie invalid!')

        return response_json['plate']
    except Exception as e:
        logging.error('Error parsing response, ERR: %s' % str(e))
        return None


def make_initial_request():
    json_request = {'cookie': config.HTTP_COOKIE}
    json_string = json.dumps(json_request)
    encr_request = cipher.encrypt(json_string)

    try:
        r = requests.put(config.http_server_url(), data=encr_request, timeout=10)
    except Exception as e:
        logging.error('Error communicating with Godfather, ERR: %s' % str(e))
