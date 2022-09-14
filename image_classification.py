from picamera import PiCamera
from voice_control import VoiceControl
from modules import sleep
# import keras
# from keras.models import load_model

speech = VoiceControl()


class ImageClassification:

    def __init__(self):
        self.camera = PiCamera()
        # self.skin_lesion_model = keras.models.load_model('converted_model.tflite')

    def take_image(self, amount: int):
        for i in range(1, amount+1):
            self.camera.capture(f'images/img{i}.jpg')
            self.camera.stop_preview()

    def start_camera(self):
        self.camera.start_preview()
        sleep(10)
        self.take_image(3)

    def classify_lesion_images(self):
        pass