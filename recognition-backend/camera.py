import cv2
import time
import face 

def crop(image):
    crop = face.get_largest_face(face.detect_single(image))
    if (crop is None or len(crop) == 0):
        return None

    new_img = face.crop(image, *crop)

    return new_img

class Camera:
    IMAGE_URL = '../data/image.jpg'
    RESOLUTION = (320, 240)
    def __init__(self):
        self.cam = cv2.VideoCapture(0)   # 0 -> index of camera
    def cap(self, show = True):
        s, image = self.cam.read()
        new_img = crop(image)

        if show:
            cv2.imshow('asdf', new_img)
            time.sleep(2)

        return new_img


    def cap_jpeg(self):
        img = self.cap()
        if (img is None): return None
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()