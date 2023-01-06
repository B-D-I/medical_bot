import json
import statistics
import random
from device_voice_control import VoiceControl
from diagnosis_bot import Diagnosis
from patient import Patient
from scratch_assistance_alert import AssistanceAlert
from camera import Camera
# Arduino
import serial
USB_PORT = "/dev/ttyACM0"
usb = serial.Serial(USB_PORT, 9600, timeout=2)
usb.flush()         # avoids receiving or sending not useful / complete data

speech = VoiceControl()
patient = Patient()
alert = AssistanceAlert()
camera = Camera()

"""
Medical Bot: Home Diagnosis Device
"""
__author__ = "Nathan Hewett"

patient_details_response = []
# patient_details_response = ['nathan', 'male', 1989, 175.0, 90.0, 1, 0]   # test list


def get_patient_info():
    """
    This function receives patient information required for diagnosis and appends to patient_details_response list
    :return: calls set_patient_attributes function, which instantiates a patient object with received data
    """
    patient_account_questions = ['name', 'gender', 'birth year', 'height in centimetres', 'weight in kilos',
                                 'do you exercise', 'do you smoke']
    try:
        speech.speak('please respond to the following')
        speech.speak('what is your:')
        for item in patient_account_questions:
            speech.speak(f'{item}')
            response = speech.receive_command()

            # validate responses
            if item == 'name' or item == 'gender':
                patient_details_response.append(response.lower())
            # elif item == 'gender':
            #     patient_details_response.append(patient.check_gender(response))
            elif item == 'birth year':
                patient_details_response.append(int(response))
            elif item in ['height in centimetres', 'weight in kilos']:
                patient_details_response.append(float(response))
            elif item in ['do you exercise', 'do you smoke']:
                patient_details_response.append(speech.return_confirmation_binary(response))
        # update patient attributes
        set_patient_attributes()
    except ValueError as error:
        speech.speak('incorrect answer format, please start again')
        print(error)


def set_patient_attributes():
    # instantiate patient object
    patient.name = patient_details_response[0]
    patient.gender = patient_details_response[1]
    patient.birth_year = patient_details_response[2]
    patient.height = patient_details_response[3]
    patient.weight = patient_details_response[4]
    patient.is_exercise = patient_details_response[5]
    patient.is_smoker = patient_details_response[6]


def start_diagnosis():
    # instantiate med bot with new patient -> start conversation function
    get_patient_info()
    bot = Diagnosis(patient, camera)
    usb.write(b'alert_off')
    bot.start_diagnosis('MPXV')


def require_assistance():
    # alert function
    speech.speak('please wait for assistance')
    usb.write(b'alert')


def set_camera():
    # activate camera for adjustment
    camera.set_camera()


def heart_rate():
    """
    This function initiates the heart_rate function from the Arduino. First a green led will light to inform the user
    to place finger on the sensor. Once a pulse is recognised, the green led turn off and a red led will flash
    intermittently until the function is complete. Numerous bpm readings will be appended to a list, and an average
    BPM will be spoken.
    :return: the average beats per minute of the user
    """
    heart_rate_limit = 0
    heart_rates = []
    # heart_rate_limit to ensure a suitable amount of heart rate readings
    while heart_rate_limit < 20:
        # call the arduino heart_rate function
        usb.write(b'heart_rate')
        # convert the bytes into data type
        line = usb.readline().decode('utf-8').rstrip()
        print(line)
        # slice the required information
        heart_rates.append(line[-3:])
        heart_rate_limit += 1
    print(heart_rates)
    for rates in heart_rates:
        # remove non-required data
        if rates == 'tly' or rates == 'ted':
            heart_rates.remove(rates)
            try:
                av_heart_rate = int(statistics.median(heart_rates))
                speech.speak(f'your heart rate is {str(av_heart_rate)} beats per minute')
                return av_heart_rate
            except TypeError or ValueError as error:
                print('Error: ', error)


func_dict = {
            "require_assistance": require_assistance,
            "diagnosis": start_diagnosis,
            "set_camera": set_camera,
            "heart_rate": heart_rate
        }


def device_start():
    """
       This function opens the 'chat_conv' json file, and listens to voice commands from the user.
       If a query is recognised from the input array in the json file, an output from the relevant
       output list will be randomly selected, and spoken. If the input query has a function allocated,
       these will be included in the 'func_dict' dictionary, and called if queried, using the 'call_func'
       function.
    """
    with open("chat_conv.json", "r") as chat_file:
        chat_dict = json.load(chat_file)
    while True:
        query = speech.receive_command()
        for i in chat_dict["conversation"]:  # for items in dict
            if query in i['inputs']:  # if query found
                if i['outputs'] != "":
                    speech.speak(random.choice(i['outputs']))
                    func = i['conv_name']
                    call_func(func)
                    continue


def call_func(func):  # parameter given from conversation func
    for key in func_dict:  # if the key is same as func query, call function
        if func == key:
            func_dict[key]()


if __name__ == "__main__":
    while True:
        device_start()












