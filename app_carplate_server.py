"""
RUN INTO '/root/Projects/Final_Park_6_05/Pentagon/'
"""


import sqlite3

#from sqlites.check_sqlite import DB

from flask import Flask, render_template, url_for, request, abort, jsonify, send_from_directory

import co_carplate_server as co

app = Flask(__name__)

'''
def get_full_image_path(name):
    return name[36:]
'''



ALLOWED_METHODS = ['new', 'old', 'initial']
'''
def __init__(self):
  self.db = DB()
'''

@app.route('/', methods=['GET'])
def heimdall():
    return render_template('hd_carplate_server.html', jquery=url_for('static', filename='jquery.min.js'))


@app.route('/root/Projects/Final_Final/Godfather/cars/', methods=['GET'])
def photos():
    req_method = request.args.get('method')
    if req_method and req_method in ALLOWED_METHODS:
        conn = sqlite3.connect(co.DB_PATH)
        cur = conn.cursor()

        sql = ""
        if req_method == 'initial':
            sql = """SELECT rowid, * FROM shots
                      ORDER BY rowid DESC
                      LIMIT {};""".format(co.PAGINATE_BY)

        if req_method == 'new':
            last_id = request.args.get('last_id')
            if not last_id:
                return abort(400)

            sql = """SELECT rowid, * FROM shots
                      WHERE rowid > {}
                      ORDER BY rowid DESC;""".format(last_id)

        if req_method == 'old':
            last_id = request.args.get('last_id')
            if not last_id:
                return abort(400)

            sql = """SELECT rowid, * FROM shots
                      WHERE rowid < {}
                      ORDER BY rowid DESC
                      LIMIT {};""".format(last_id, co.PAGINATE_BY)

        cur.execute(sql);
        response = [{'rowid': rowid, 'plateno': plateno, 'plateno_new': plateno_new,
                     'full_image': full_image} for
                    rowid, plateno, plateno_new, full_image in cur.fetchall()]
        conn.close()
        return jsonify(response)
    else:
        return abort(400)
@app.route('/root/Projects/Final_Final/Godfather/cars/<path:filename>')
def serve_photos(filename):
    return send_from_directory(co.IMAGE_ROOT_FOLDER + '/', filename)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port='5000')
