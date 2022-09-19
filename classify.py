import os.path
from tflite_runtime.interpreter import Interpreter
import tensorflow as tf
import numpy as np
from keras.preprocessing import image


model_path = 'models/converted_model.tflite'
interpreter = tf.lite.Interpreter(model_path=model_path)
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
interpreter.allocate_tensors()


def print_input_and_output_shape(input_details, output_details):
    print('input shape: ', input_details[0]['shape'])
    print('input type: ', input_details[0]['dtype'])
    print('output shape: ', output_details[0]['shape'])
    print('output type: ', output_details[0]['dtype'])
    print(interpreter.get_input_details())


def predict_images():
    path = 'images/testing_images_cancer/'
    for filename in os.listdir(path):
        img_path = path+filename
        img = image.load_img(img_path, target_size=(150, 150))
        images = image.img_to_array(img)
        # Expand the shape of array:
        images = np.expand_dims(images, axis=0)
        interpreter.set_tensor(input_details[0]['index'], images)
        interpreter.invoke()
        tflite_model_predictions = interpreter.get_tensor(output_details[0]['index'])
        # print('pred', tflite_model_predictions.shape)

        # Returns 0: malignant || 1: benign
        if tflite_model_predictions == 0:
            print('\n', filename, ': Cancer Detected')
        else:
            print('\n', filename, ': No Cancer Detected\n')


# predict_images()