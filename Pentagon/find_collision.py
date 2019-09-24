from threading import Thread
import time
import requests
import logging

import configs.pentagon as config


class Entrance:
    name = None
    moxa_ip = None
    # moxa_dis & cam_ips correspond with each other
    moxa_di_names = None
    moxa_dis = None
    cam_ips = None

    was_pins_active = None

    def __init__(self, moxa_ip, moxa_di_names, moxa_dis, cam_ips, name='EMPTY'):
        self.name = name
        self.moxa_ip = moxa_ip
        self.moxa_di_names = moxa_di_names
        self.moxa_dis = moxa_dis
        self.cam_ips = cam_ips

        self.was_pins_active = [False] * len(moxa_dis)

    def __str__(self):
        return str({'name': self.name, 'moxa_ip': self.moxa_ip,
                    'moxa_di_names': self.moxa_di_names, 'moxa_dis': self.moxa_dis,
                    'cam_ips': self.cam_ips, 'was_pins_active': self.was_pins_active
                    })


ENTRANCES = [Entrance(name='A1', moxa_ip='10.1.129.51',
                      moxa_di_names=['IN', 'OUT'], moxa_dis=[0, 2],
                      cam_ips=['192.168.60.17', '192.168.60.15']),
             Entrance(name='A2', moxa_ip='10.1.129.52',
                      moxa_di_names=['IN', 'OUT'], moxa_dis=[0, 2],
                      cam_ips=['192.168.60.14', '192.168.60.11']),
             Entrance(name='K1', moxa_ip='10.1.129.53',
                      moxa_di_names=['OUT_BACK', 'OUT'], moxa_dis=[0, 1],
                      cam_ips=['192.168.60.16', '192.168.60.13'])
            ]


class PGMoxaDriver:
    def __init__(self, car_detected_callback):
        self.car_detected_callback = car_detected_callback
        self._start()

    def _start(self):
        self.thread = Thread(target=self._loop)
        self.isActive = True
        self.thread.start()

    def stop(self):
        self.isActive = False

    def _loop(self):
        while self.isActive:
            logging.debug('START NEW REQUEST CYCLE')
            for moxa_ip in MOXA_IPS:
                moxa_url = config.gen_moxa_url(moxa_ip)
                try:
                    r = requests.get(moxa_url,
                                     timeout=1,
                                     headers={'Content-Type': "application/json",
                                              "Accept": 'vdn.dac.v1'})
                except Exception as e:
                    print('Error requesting moxa with url %s, ERR: %s' % (moxa_url, str(e)))
                    continue

                di = r.json()['io']['di']

                for di_pin in di:
                        if di_pin['diStatus'] == 0:
                            if entrance.was_pins_active[i]:
                                logging.debug('Pin deactivated: %s in ENTRANCE: %s' %
                                             (str(di_pin['diIndex']), str(entrance))
                                             )
                            entrance.was_pins_active[i] = False
                        if di_pin['diStatus'] == 1:
                            if entrance.was_pins_active[i]:
                                continue
                            logging.debug('Pin activated: %s in ENTRANCE: %s' % (str(di_pin), str(entrance)))
                            entrance.was_pins_active[i] = True

                            self.car_detected_callback(entrance.cam_ips[i])

            time.sleep(0.5)