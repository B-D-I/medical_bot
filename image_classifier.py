import numpy as np
import tensorflow as tf
from keras.preprocessing import image
from hashlib import sha256


class ImageClassifier:
    """
    This class performs image classification using the TensorFlow Lite interpreter
    """

    def __init__(self):
        self.model_path = f'models/convertedeffnetSVM97.tflite'

    conditions_classes = {
        0: 'MPXV',
        1: 'Normal',
        2: 'Other Skin Condition'
    }

    def __return_interpreter(self, model: str):
        interpreter = tf.lite.Interpreter(model_path=self.model_path)
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
        img = image.load_img(img_path, target_size=(224, 224))
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
        top_index = self.return_prediction(image_path, image_type, filename)[1]
        score_percent = self.return_prediction(image_path, image_type, filename)[3]

        for key in self.conditions_classes:
            if top_index[1] == key:
                print(filename, '\nclass: ', top_index[1], ' - ', self.conditions_classes[key], '', score_percent)
                return [filename, self.conditions_classes[key], score_percent]

    def integrity_check(self):
        # check hash of file
        with open(self.model_path, 'rb') as f:
            file = f.read()
            return sha256(file).hexdigest()
