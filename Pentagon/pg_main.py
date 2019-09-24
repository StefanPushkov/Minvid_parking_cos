""" This is the daemon for image grabbing service placed on object pc.
When requested, takes image from ip camera, saves it to disk,
makes request to computational service (http, user data is json encrypted with AES),
finally returns json with path to image and result of recognition"""

import json
import os
import sys
import time
from threading import Thread
import logging
import datetime
from pg_socket_server import PGSocketServer
from pg_camera_driver import PGCameraDriver
from pg_moxa_driver import PGMoxaDriver
from pg_http_client import make_request, make_initial_request
from pg_sqlite import check_plate

import configs.pentagon as config


base_dir = config.get_base_dir_by_name('carplates_server')
sys.path.append(base_dir)


class PGMain:
    def __init__(self):
        self.camera_driver = PGCameraDriver()
        #self.server = PGSocketServer(self.make_shots_and_get_plate)
        self.moxa = PGMoxaDriver(self.on_car_detected)

    # def stop(self):
        # self.server.stop()

    def on_car_detected(self, entrance):
        #make_initial_request()
        time.sleep(0.2)
        Thread(target=lambda: self.on_car_detected_t(entrance)).start()

    def on_car_detected_t(self, entrance):
                                                                                    # TODO: Исправить кал
        plate = self.make_shots_and_get_plate(entrance)

        if plate:
            logging.info('Recognition done! Plate: ' + plate)
            #if check_plate(plate):
            #    logging.info('Plate found in whitelist, opening border.')           #Момент с проверкой вайт-Листа
            #else:
            #    logging.info('Plate not in whitelist.')
        else:
            logging.error('Recognition error! Check Godfather logs for details.')

    def make_shots_and_get_plate(self, entrance):
        plate = None

        image = self.camera_driver.get_image_by_ip(entrance)                            #list of images act
        daytime: str = str(datetime.datetime.now())
        daytime = daytime[:19]
        for i in range(0, config.PHOTO_SERIES_SIZE - 1):
            if image[i] is None:
                json_obj = {'status': -2,
                            'error': 'Error communicating with camera'}
                return json.dumps(json_obj)

            if i == config.PHOTO_SERIES_SIZE - 2:
                plate = make_request(image[i], i, daytime, is_last=True)
            else:
                make_request(image[i], i, daytime,)
                time.sleep(config.SHOT_INTERVAL / 1000)
        logging.info('We gor imgs')
        return plate


if __name__ == '__main__':
    os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
    fh = logging.FileHandler(config.LOG_FILE)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch = logging.StreamHandler(sys.stdout)

    logging.basicConfig(level=config.LOG_LEVEL, handlers=[ch, fh])

    logging.getLogger('urllib3.connec   tionpool').setLevel(logging.WARNING)

    PGMain()

    while 1:
        time.sleep(1)
