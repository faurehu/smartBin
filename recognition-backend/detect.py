import cv2
import img
import camera
import json
import db

class Detector:
	def __init__(self):
		self.conf_json = None
		with open('../config/faces.json', 'r') as conf_json_f:
		    self.conf_json = json.loads(conf_json_f.read())
		self.model = cv2.createEigenFaceRecognizer()
		self.model.load(self.conf_json['training_path'])

	def detect_face(self, image, show = False):
		small_img = img.resize_training(image)
		if (small_img is not None):
			#small_img = cv2.cvtColor(small_img,cv2.COLOR_BGR2GRAY)
			small_img = cv2.equalizeHist(small_img)
			if show: cv2.imshow('test', small_img)
			uid, conf = self.model.predict(small_img)
			return db.DB().query('SELECT name, id from users WHERE id = %s' % uid).fetchone()
		else:
			return "bad image"

	def setup_cam(self):
		self.cam = camera.Camera()

	def run(self):
		raw_img = self.cam.cap()
		if (raw_img is not None):
			return self.detect_face(raw_img)
		else:
			return None

if __name__ == '__main__':
	detector = Detector()
	detector.setup_cam()
	while True:
		detector.run()
		