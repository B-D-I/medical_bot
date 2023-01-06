from picamera import PiCamera
from time import sleep


class Camera:
    """
    Camera class provides piCamera instantiation and all camera functions
    """
    def __init__(self):
        self.camera = PiCamera()

    def take_image(self, amount: int, image_name: str):
        self.camera.start_preview()
        sleep(10)
        for i in range(1, amount+1):
            self.camera.capture(f'images/{image_name}_images/{image_name}{i}.jpg')
            sleep(1)
            self.camera.stop_preview()

    def set_camera(self):
        self.camera.start_preview()
        sleep(30)
        self.camera.stop_preview()



