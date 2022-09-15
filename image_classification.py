import face_recognition
import timeout_decorator
from picamera import PiCamera
from voice_control import VoiceControl
from modules import sleep, time
from tflite_runtime.interpreter import Interpreter
import numpy as np

speech = VoiceControl()


class ImageClassification:
    face_locations = []
    face_encodings = []
    output = np.empty((240, 320, 3), dtype=np.uint8)

    def __init__(self):
        self.camera = PiCamera()
        self.skin_lesion_model = 'converted_model.tflite'

    def load_tflite_model(self):
        with open(self.skin_lesion_model, 'rb') as f:
            tflite_model = f.read()
            return tflite_model

    def take_image(self, amount: int, image_name: str):
        speech.speak('in ten seconds three images will be taken, ensure you adjust the focus')
        self.camera.start_preview()
        sleep(10)
        for i in range(1, amount+1):
            self.camera.capture(f'images/skin_images/{image_name}{i}.jpg')
            self.camera.stop_preview()

    def show_camera_preview(self):
        self.camera.start_preview()
        sleep(60)
        self.camera.stop_preview()

    def encode_patient_image(self, patient_name: str):
        self.camera.resolution = (320, 240)
        # Load a sample picture and learn how to recognize it.
        print("Loading known face image")
        patient_image = face_recognition.load_image_file(f"images/face_rec_images/{patient_name}.jpg")
        patient_face_encoding = face_recognition.face_encodings(patient_image)[0]
        return patient_face_encoding

    @timeout_decorator.timeout(100)
    def facial_recognition(self, patient_name: str):
        try:
            patient_face_encoding = self.encode_patient_image(patient_name)
            login = False
            while not login:
                print("Capturing image.")
                # Grab a single frame of video from the RPi camera as a numpy array
                self.camera.capture(self.output, format="rgb")
                # Find all the faces and face encodings in the current frame of video
                face_locations = face_recognition.face_locations(self.output)
                print("Found {} faces in image.".format(len(face_locations)))
                face_encodings = face_recognition.face_encodings(self.output, face_locations)
                # Loop over each face found in the frame to see if it's someone we know.
                for face_encoding in face_encodings:
                    # See if the face is a match for the known face(s)
                    match = face_recognition.compare_faces([patient_face_encoding], face_encoding)
                    name = " Unknown Person "
                    if match[0]:
                        print(f"Recognised {patient_name}")
                        login = True
        except timeout_decorator.timeout_decorator.TimeoutError as error:
            print(error)
        return login

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
# classify.predict_images('images/nathan.jpg')
# classify.take_face_images()
# classify.facial_recognition('nathan')