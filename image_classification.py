from picamera import PiCamera
from voice_control import VoiceControl
from modules import sleep
# import keras
# from keras.models import load_model
# from keras.utils import load_img
# import numpy as np

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

    # def predict_images(self, image_path):
    #     img = load_img(image_path, target_size=(150, 150))
    #     img = np.array(img)
    #     img = np.expand_dims(img, axis=0)
    #     model = self.skin_lesion_model
    #     prediction = model.predict(img)
    #     if prediction == 0:
    #         print('cancer')
    #     else:
    #         print('not cancer')

# classify = ImageClassification()
# classify.predict_images('images/img1.jpg')