import os
import random
import sqlite3
import string
import time
from threading import Thread
from queue import Queue
import logging
import datetime
import configs.godfather as config
from openalpr import Alpr
import sys
from locale import setlocale
from gf_sqlite import Database

from Godfather.gf_sqlite import logger

def add_shot_by_creenj(number, image, current_plate):
    setlocale(0, "C")
    db = Database()
    logger.info('So, here we get vals from queue at creenj')
    logger.info(number + '\n' + current_plate + '\n' + image)

    logging.info('from gf_sqlite_creenj, so number is %s' % number)

    if number == '':
        try:
            alpr = Alpr('eu', '/usr/share/openalpr/config/openalpr.defaults.conf',
                        '/usr/share/openalpr/runtime_data')
            print("Camed to ALPR")
            if not alpr.is_loaded():
                print("Error loading OpenALPR")
                sys.exit(1)

            alpr.set_top_n(20)
            alpr.set_default_region("lt")

            results = alpr.recognize_file(image)
            answer = results['results'][0]['plate']
            alpr.unload()
        except Exception as e:
            print('Couldn\'t load ALPR')
            answer = 'Unsolved'
            return

    if answer == '':
        return

    print('creenj Answer is ', answer)

    json_obj = {
        'number': answer,
        'image': image,
        'current_plate': current_plate
    }

    conn = sqlite3.connect(config.DB_PATH)
    c = conn.cursor()

    query = 'INSERT INTO ' + db.SHOTS_TABLE_NAME + ' VALUES (?,?,?)'
    values = [json_obj['number'], json_obj['current_plate'], json_obj['image']]
    values = list(map(str, values))  # conversion of int (values[0]) to str is ok here
    c.executemany(query, [values])  # actually executes only once

    conn.commit()  # apply changes
    c.close()
    conn.close()
    logger.info('So, it should be in DB')
def neiron(img_path):
        try:
            alpr = Alpr('eu', '/usr/share/openalpr/config/openalpr.defaults.conf',
                        '/usr/share/openalpr/runtime_data')
            print("Camed to ALPR")
            if not alpr.is_loaded():
                print("Error loading OpenALPR")
                sys.exit(1)

            alpr.set_top_n(20)
            alpr.set_default_region("lt")

            results = alpr.recognize_file(img_file)
            answer = results['results'][0]['plate']
            alpr.unload()
        except Exception as e:
            print('Couldn\'t load ALPR')
            answer = 'Unsolved'
            return answer

paths_new = []
nr_plt = []
plates = []
paths  = []
nr_plt[0:1601] = '1'
with open('/root/Projects/Final_Final/Godfather/plates_to_down.txt', 'r') as plt:
    content = plt.read()
    plt.close()
    for i in range(1600):
        plates.append(content.split()[i])

with open('/root/Projects/Final_Final/Godfather/paths_to_down.txt', 'r') as pth:
    content = pth.read()
    pth.close()
    for k in range(1600):
        paths.append(content.split()[k])

print(plates)
print(paths)
print(len(plates))
print(len(paths))

time.sleep(2)
wow: str = ''
os.makedirs(os.path.dirname(wow), exist_ok=True)

for t in range(1600):
    if t % 20 == 0:
        rnd = random.randint(-17, -3)
        nr_plt[t - rnd] = neiron(paths[t - rnd])
        nr_plt[t] = plates[t]
    else:
        nr_plt[t] = paths[t]
    paths_new.append(paths)
    pa: str = paths[t]
    paths_new[t] = wow + pa[55:]
    with open(paths[t], 'rb') as opn_img:
        with open(paths_new, 'wb') as imgfile:
            imgfile.write(opn_img.read())

for n in range(1600):
    add_shot_by_creenj(nr_plt[n], str(paths_new[n]), str(plates[n]))
    print('---------------------------------------------------------------------------------------------------------------' + str(n))