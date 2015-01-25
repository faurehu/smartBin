import os, syslog, sys
import pygame
import time
import string
import cv2
import numpy
import face

import urllib
import urllib2


ISPIE = sys.platform != 'darwin' 
RESOLUTION = (320, 240)

print os.getcwd()


def sendImageToServer(img):
    try:
        ret, jpeg = cv2.imencode('.jpg', img)
        jpeg_body = jpeg.tostring()

        url = 'http://10.100.83.132:4454/img'
        req = urllib2.Request(url, jpeg_body)
        response = urllib2.urlopen(req)
        result = response.read()
        return result
    except:
        return ':('

# font colours
colourWhite = (255, 255, 255)
colourBlack = (0, 0, 0)

# update interval
updateRate = 0 # seconds

if (ISPIE):
    os.environ['SDL_VIDEODRIVER'] = 'fbcon'
    os.environ["SDL_FBDEV"] = "/dev/fb1"
    #os.environ["SDL_MOUSEDEV"] = "/dev/input/touchscreen"
    #os.environ["SDL_MOUSEDRV"] = "TSLIB"

class pitft :
    screen = None;
    colourBlack = (0, 0, 0)
 
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        if (ISPIE):
            disp_no = os.getenv("DISPLAY")
            if disp_no:
                print "I'm running under X display = {0}".format(disp_no)

            # Init framebuffer/touchscreen environment variables
            os.putenv('SDL_VIDEODRIVER', 'fbcon')
            os.putenv('SDL_FBDEV'      , '/dev/fb1')

            # Select frame buffer driver
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
        driver = 'fbcon'
        try:
            pygame.display.init()
        except pygame.error:
            print 'Driver: {0} failed.'.format(driver)
            exit(0)
 
        
        #size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        size = RESOLUTION
        if (ISPIE):
            self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(size)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))
        # Initialise font support
        pygame.font.init()
        # Render the screen
        pygame.display.update()
 
    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."
 
# Create an instance of the PyScope class
mytft = pitft()
 
pygame.mouse.set_visible(False)
 
# set up the fonts
# choose the font
fontpath = pygame.font.match_font('dejavusansmono')
# set up 2 sizes
font = pygame.font.Font(fontpath, 20)
fontSm = pygame.font.Font(fontpath, 18)

print('inited')


def opencv_to_surface(img):
    return pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB")

class CameraManager():
    IMAGE_URL = '../data/image.jpg'
    RESOLUTION = (320, 240)
    def init(self):
        if (ISPIE):
            import picamera
            self.cam = picamera.PiCamera()
            self.cam.resolution = self.RESOLUTION
            print('started pi camera')
        else:
            self.cam = cv2.VideoCapture(0)   # 0 -> index of camera
            print('started mac camera')

    def cap(self):
        surf = None
        if (ISPIE):
            self.cam.capture(self.IMAGE_URL)
            surf = cv2.imread(self.IMAGE_URL)
        else:
            s, surf = self.cam.read()
            surf = cv2.resize(surf, self.RESOLUTION) 
        if surf is not None:
            return surf, opencv_to_surface(surf)

def detect_face(image):
    # convert to gray
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # detect face
    result = face.detect_single(image)
    print result
    return result

def main(camera):
    rawimg, image = camera.cap()
    
    faces = detect_face(rawimg)

    for facein in faces:
        pygame.draw.rect(image, colourWhite, facein, 1)

    biggestFace = face.get_largest_face(faces)
    if biggestFace is not None:
        biggestFaceImg = face.crop(rawimg, biggestFace[0], biggestFace[1], biggestFace[2], biggestFace[3])

    mytft.screen.blit(image, (0, 0))

    if biggestFace is not None:
        mytft.screen.blit(opencv_to_surface(biggestFaceImg), (0, 0))
        # has biggest face, try to get text!
        msg = 'sending image to server'
        mytft.screen.blit(font.render(msg, True, colourWhite), (40, 40))
        pygame.display.update()
        print(msg)
        text = sendImageToServer(biggestFaceImg)
        mytft.screen.blit(font.render('%s' % text, True, colourWhite), (100, 100))
        pygame.display.update()
        print('got response!')

        text_surface = font.render(text, True, colourWhite)
        mytft.screen.blit(text_surface, (0, 50))


    for event in pygame.event.get():
        print(event)
        if (event.type is pygame.MOUSEBUTTONDOWN):
            print('mousedown')
            pos = pygame.mouse.get_pos()
            #mytft.screen.blit()
            text_surface = font.render('x %d y %d' % (pos[0], pos[1]), True, colourWhite)
            mytft.screen.blit(text_surface, (0, 0))


    # refresh the screen with all the changes
    pygame.display.update()

    # Wait
    #time.sleep(updateRate)

if __name__ == '__main__':
    camera = CameraManager()
    camera.init()
    while True:
        main(camera)
