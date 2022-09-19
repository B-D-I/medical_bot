import face_recognition
import timeout_decorator
from picamera import PiCamera
from voice_control import VoiceControl
from modules import sleep
from tflite_runtime.interpreter import Interpreter
import numpy as np

speech = VoiceControl()


class ImageClassification:
    face_locations = []
    face_encodings = []
    output = np.empty((240, 320, 3), dtype=np.uint8)

    def __init__(self):
        self.camera = PiCamera()
        self.skin_lesion_model = '/models/converted_model.tflite'

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
        login = False
        try:
            patient_face_encoding = self.encode_patient_image(patient_name)
            while not login:
                print("Capturing image.")
                # get a single frame of video from camera as numpy array
                self.camera.capture(self.output, format="rgb")
                # find all the faces and face encodings in current video
                face_locations = face_recognition.face_locations(self.output)
                print("Found {} faces in image.".format(len(face_locations)))
                face_encodings = face_recognition.face_encodings(self.output, face_locations)
                # loop over each face found in frame to confirm if recognised
                for face_encoding in face_encodings:
                    # confirm if face is a match
                    match = face_recognition.compare_faces([patient_face_encoding], face_encoding)
                    if match[0]:
                        print(f'Recognised {patient_name}')
                        login = True
                    else:
                        print('Unknown user')
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
