
import cv2
import numpy as np
import db
import cStringIO
import json
import img

global conf_json
conf_json = None
with open('../config/faces.json', 'r') as conf_json_f:
    conf_json = json.loads(conf_json_f.read())
    conf_json['data_path']

images = []
labels = []

res = db.DB().query('SELECT ui.img, u.id, ui.id FROM user_images as ui INNER JOIN users as u ON u.id = ui.user_id')
print 'Found %d training file' % res.rowcount

for row in res.fetchall():
	file_like=cStringIO.StringIO(row[0])
	image = img.resize_training(img.create_opencv_image_from_stringio(file_like))
	image = cv2.equalizeHist(image)
	images.append(image)
	labels.append(int(row[1]))

model = cv2.createEigenFaceRecognizer()
model.train(np.asarray(images), np.asarray(labels))

model.save(conf_json['training_path'])
print 'Training data saved to', conf_json['training_path']

# Save mean and eignface images which summarize the face recognition model.
mean = model.getMat("mean").reshape(images[0].shape)
cv2.imwrite('../data/trainingfile.jpg', img.normalize(mean, 0, 255, dtype=np.uint8))
eigenvectors = model.getMat("eigenvectors")

