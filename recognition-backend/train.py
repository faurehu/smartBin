import numpy as np
import db
import cStringIO
import json
import sys, os
import img
import camera

import cv2

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import face

name = sys.argv[1]
print 'name? %s' % name

global conf_json
conf_json = None
with open('../config/faces.json', 'r') as conf_json_f:
    conf_json = json.loads(conf_json_f.read())

out = -1

cur = db.DB().query('SELECT id from USERS where name = %s', (name, ))
res = cur.fetchone()
if (res is not None and len(res) == 1):
    out = res[0]
else: 
    res = db.DB().query('INSERT IGNORE INTO users (name) VALUES (%s)', (name, ))
    db.DB().db.commit()
    out = res.lastrowid

if __name__ == '__main__':
    while True:
        cam = camera.Camera()
        img = cam.cap_jpeg()
        if (img is not None):
            res = db.DB().query('INSERT INTO user_images (user_id, img) VALUES (%s, %s)', (out, img, ))
            db.DB().db.commit()