from picamera import PiCamera
from device_voice_control import VoiceControl
from modules import sleep
speech = VoiceControl()


class Camera:
    """
    Camera class provides piCamera instantiation and all camera functions
    """

    def __init__(self):
        self.camera = PiCamera()

    def take_image(self, amount: int, image_name: str):
        # speech.speak(f'in ten seconds {amount} images will be taken, ensure you adjust the focus')
        self.camera.start_preview()
        sleep(10)
        for i in range(1, amount+1):
            self.camera.capture(f'images/{image_name}_images/{image_name}{i}.jpg')
            sleep(1)
            self.camera.stop_preview()

    def set_camera(self):
        # speech.speak('camera will preview for one minute')
        self.camera.start_preview()
        sleep(60)
        self.camera.stop_preview()

    def take_face_photo(self, username):
        speech.speak(f'in ten seconds your image will be taken, ensure you adjust the focus')
        self.camera.start_preview()
        sleep(10)
        self.camera.capture(f'images/face_rec_images/{username}.jpg')
        self.camera.stop_preview()



