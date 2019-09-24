import os
import logging
import threading
import time
import sys
from socketserver import ThreadingMixIn

import configs.pentagon as config

from http.server import BaseHTTPRequestHandler, HTTPServer
from queue import Queue

from pg_main import PGMain


LOCAL_IP = '127.0.0.1'


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


class MockupCameraHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/scapture':
            img_path = self.server.queue.get_nowait()
            with open(img_path, 'rb') as infile:
                img = infile.read()

            self.send_response(200)
            self.send_header('Content-Type', 'image/jpeg')
            self.end_headers()

            self.wfile.write(bytes(img))
            return


def start_server(srv):
    thread = threading.Thread(target=srv.serve_forever)
    thread.daemon = True
    thread.start()


if __name__ == '__main__':
    os.makedirs(os.path.dirname(config.LOG_FILE), exist_ok=True)
    fh = logging.FileHandler(config.LOG_FILE)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch = logging.StreamHandler(sys.stdout)

    logging.basicConfig(level=config.LOG_LEVEL, handlers=[ch, fh])

    logging.getLogger('urllib3.connectionpool').setLevel(logging.WARNING)

    server = ThreadingSimpleServer((LOCAL_IP, 80), MockupCameraHandler)
    test_images = [os.path.join('test_images', image) for image in os.listdir('test_images') if os.path.isfile(os.path.join('test_images', image))]
    img_queue = Queue()
    for image in test_images:
        img_queue.put_nowait(image)
    server.queue = img_queue
    start_server(server)

    time.sleep(2)

    config.PHOTO_SERIES_SIZE = 4
    main_obj = PGMain()
    main_obj.on_car_detected(LOCAL_IP)
