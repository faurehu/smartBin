import cv2

import detect
import camera, img
import cStringIO
import numpy as np


detector = detect.Detector()

def process_image(image):
	opencv_img = img.create_opencv_image_from_stringio(image)
	if (opencv_img is None):
		return ':('
	face = detector.detect_face(opencv_img)
	return face

def app(environ, start_response):
	try:
		request_body_size = int(environ.get('CONTENT_LENGTH', 0))
	except (ValueError):
		request_body_size = 0

	print 'req size: %d' % request_body_size

	request_body = environ['wsgi.input'].read(request_body_size)

	resp = process_image(cStringIO.StringIO(request_body))

	data = "%s" % resp

	start_response("200 OK", [
	  ("Content-Type", "text/plain"),
	  ("Content-Length", str(len(data)))
	])
	return iter([data])

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('', detector.conf_json['port'], app)
    print('running on port %d' % detector.conf_json['port'])
    srv.serve_forever()
