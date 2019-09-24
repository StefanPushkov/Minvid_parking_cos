import sqlite3

import configs.pentagon as config


def check_plate(plate):
    conn = sqlite3.connect(config.SHOTS_DB_PATH)
    cur = conn.cursor()

    sql = """SELECT * FROM {}
             WHERE plate = {}""".format(config.SHOTS_DB_PATH, plate)

    cur.execute(sql)
    return cur.fetchone() is not None
