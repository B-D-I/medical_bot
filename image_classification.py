import os
import face_recognition
import timeout_decorator
import numpy as np
import tensorflow as tf
from keras.preprocessing import image
from camera import Camera
from voice_control import VoiceControl
from database import Database
from credentials import conditions_hash, lesions_hash
from tflite_runtime.interpreter import Interpreter
speech = VoiceControl()
db = Database()
camera = Camera()


class ImageClassification:
    face_locations = []
    face_encodings = []
    output = np.empty((240, 320, 3), dtype=np.uint8)
    conditions_classes = {0: 'atopic_dermatitis',
                          1: 'chickenpox',
                          2: 'eczema',
                          3: 'measles',
                          4: 'normal_skin',
                          5: 'psoriasis',
                          6: 'rosacea',
                          7: 'vasculitis'}

    def __init__(self):
        self.skin_lesion_model = 'models/converted_lesions_model.tflite'

    @staticmethod
    def set_camera():
        camera.set_camera()

    @staticmethod
    def take_face_photo():
        camera.take_face_photo()

    @staticmethod
    def encode_patient_image(patient_name: str):
        # get user image then learn features
        camera.camera.resolution = (320, 240)
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
                camera.camera.capture(self.output, format="rgb")
                # find all the faces and face encodings in current video
                face_locations = face_recognition.face_locations(self.output)
                print("Found {} faces in image.".format(len(face_locations)))
                face_encodings = face_recognition.face_encodings(self.output, face_locations)
                # loop over each face found in frame to confirm if recognised -> then confirm if match
                for face_encoding in face_encodings:
                    match = face_recognition.compare_faces([patient_face_encoding], face_encoding)
                    if match[0]:
                        print(f'Recognised {patient_name}')
                        login = True
                    else:
                        print('Unknown user')
        except timeout_decorator.timeout_decorator.TimeoutError as error:
            print(error)
        return login

    @staticmethod
    def __return_interpreter(model: str):
        model_path = f'models/converted_{model}_model.tflite'
        interpreter = tf.lite.Interpreter(model_path=model_path)
        interpreter.allocate_tensors()
        return interpreter

    @staticmethod
    def __return_interpreter_details(interpreter, input_or_output: str):
        # retrieve model input and output information, including image dimensions
        if input_or_output == 'input':
            return interpreter.get_input_details()
        elif input_or_output == 'output':
            return interpreter.get_output_details()

    @staticmethod
    def view_model_details(input_details, output_details):
        print('input shape: ', input_details[0]['shape'])
        print('input type: ', input_details[0]['dtype'])
        print('output shape: ', output_details[0]['shape'])
        print('output type: ', output_details[0]['dtype'])

    @staticmethod
    def return_image_dimensions(filename: str, image_path: str):
        img_path = image_path + filename
        img = image.load_img(img_path, target_size=(150, 150))
        images = image.img_to_array(img)
        images = np.expand_dims(images, axis=0)
        return images

    def return_prediction(self, image_path: str, image_type: str, filename: str):
        interpreter = self.__return_interpreter(image_type)
        input_details = self.__return_interpreter_details(interpreter, 'input')
        output_details = self.__return_interpreter_details(interpreter, 'output')

        image = self.return_image_dimensions(filename, image_path)
        interpreter.set_tensor(input_details[0]['index'], image)
        interpreter.invoke()
        tflite_model_predictions = interpreter.get_tensor(output_details[0]['index'])

        max_score = np.max(tflite_model_predictions)
        top_index = np.where(tflite_model_predictions == max_score)
        round_score = round(max_score, 2)
        score_percent = "{:.0%}".format(round_score)
        return [tflite_model_predictions, top_index, round_score, score_percent]

    def prediction(self, image_path: str, image_type: str, filename: str):
        tflite_predict = self.return_prediction(image_path, image_type, filename)[0]
        top_index = self.return_prediction(image_path, image_type, filename)[1]
        score_percent = self.return_prediction(image_path, image_type, filename)[3]

        if image_type == 'conditions':
            for key in self.conditions_classes:
                if top_index[1] == key:
                    print(filename, '\nclass: ', top_index[1], ' - ', self.conditions_classes[key], '', score_percent)
                    return [filename, self.conditions_classes[key], score_percent, top_index]

        if image_type == 'lesions':
            if tflite_predict == 0:
                diagnosed = 'Malignant'
                print('\n', filename, ':  Malignant')
            else:
                diagnosed = 'Benign'
                print('\n', filename, ':  Benign\n')
            return [filename, diagnosed]

    def return_skin_classification(self, image_type: str):
        if db.integrity_check('models/converted_conditions_model.tflite') == conditions_hash and db.integrity_check('models/converted_lesions_model.tflite') == lesions_hash:
            camera.take_image(2, image_type)
            image_path = f'images/{image_type}_images/'
            for filename in os.listdir(image_path):
                diagnosis = self.prediction(image_path, image_type, filename)
                if image_type == 'conditions':
                    return [diagnosis[0], diagnosis[1], diagnosis[2]]
                elif image_type == 'lesions':
                    return [diagnosis[0], diagnosis[1]]
        else:
            print('model integrity check has failed. Diagnosis discontinued')
