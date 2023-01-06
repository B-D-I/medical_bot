from modules import usb, json, random
from device_voice_control import VoiceControl
from diagnosis_bot import DiagnosisBot
from patient import Patient
from scratch_assistance_alert import AssistanceAlert
from camera import Camera
speech = VoiceControl()
patient = Patient()
alert = AssistanceAlert()
camera = Camera()

"""
Medical Bot: Home Diagnosis Device
"""
__author__ = "Nathan Hewett"

# patient_details_response = []
patient_details_response = ['nathan', 'male', 1989, 175.0, 90.0, 1, 0]   # test list


def get_patient_info():
    patient_account_questions = ['name', 'gender', 'birth year', 'height in centimetres', 'weight in kilos',
                                 'do you exercise', 'do you smoke']
    try:
        speech.speak('please respond to the following')
        speech.speak('what is your:')
        for item in patient_account_questions:
            speech.speak(f'{item}')
            response = speech.receive_command()

            # validate responses
            if item == 'name':
                patient_details_response.append(response.lower())
            elif item == 'gender':
                patient_details_response.append(patient.check_gender(response))
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
    patient.name = patient_details_response[0]
    patient.gender = patient_details_response[1]
    patient.birth_year = patient_details_response[2]
    patient.height = patient_details_response[3]
    patient.weight = patient_details_response[4]
    patient.is_exercise = patient_details_response[5]
    patient.is_smoker = patient_details_response[6]


def start_diagnosis():
    # instantiate med bot with new patient -> start conversation function
    # get_patient_info()
    set_patient_attributes()
    bot = DiagnosisBot(patient, camera)
    usb.write(b'alert_off')
    # speech.speak(f'starting diagnosis, {patient.name}')
    bot.start_diagnosis('MPXV')


def require_assistance():
    speech.speak('please wait for assistance')
    usb.write(b'alert')


def set_camera():
    camera.set_camera()


func_dict = {
            "require_assistance": require_assistance,
            "diagnosis": start_diagnosis,
            "set_camera": set_camera,
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












