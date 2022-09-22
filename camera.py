from picamera import PiCamera
from voice_control import VoiceControl
from modules import sleep
speech = VoiceControl()


class Camera:

    def __init__(self):
        self.camera = PiCamera()

    def take_image(self, amount: int, image_name: str):
        speech.speak(f'in ten seconds {amount} images will be taken, ensure you adjust the focus')
        self.camera.start_preview()
        sleep(10)
        for i in range(1, amount+1):
            self.camera.capture(f'images/{image_name}_images/{image_name}{i}.jpg')
            self.camera.stop_preview()

    def set_camera(self):
        speech.speak('camera will preview for one minute')
        self.camera.start_preview()
        sleep(60)
        self.camera.stop_preview()

    def take_face_photo(self):
        speech.speak('please confirm your first name')
        username = speech.receive_command()
        self.take_image(2, username)