from modules import usb
from voice_control import VoiceControl
from med_bot import MedBot
from patient import Patient
from emergency_alert import EmergencyAlert
from diagnosis import DiagnosisAPI
from database import Database
from image_classification import ImageClassification
image = ImageClassification()
speech = VoiceControl()
patient = Patient()
alert = EmergencyAlert()
diagnose = DiagnosisAPI()
db = Database()
"""
Medical Bot: Home Diagnosis Device
"""
__author__ = "Nathan Hewett"

# TEST create account and TIDY
# TEST full diagnosis (medbot) and TIDY
# camera take face photo func TIDY
# move convert_smoker_ex function
# add more unit test
# secure sqlite
# docstrings and final TIDY



def face_login():
    speech.speak('what is your username')
    name = speech.receive_command().lower()
    try:
        bot = MedBot(patient)
        if bot.login_recognition(name):
            usb.write(b'alert_off')
            patient.name = name
            speech.speak(f'logged in as {patient.name}')
            bot.conversation()
    except FileNotFoundError as error:
        print(error)

def convert_smoker_exercise_value(col_type: str):
    if col_type in speech.confirmation:
        return 1
    else:
        return 0

def create_account():
    speech.speak('what is your username')
    name = speech.receive_command().lower()
    speech.speak('what is your gender')
    gender = speech.receive_command().lower()
    speech.speak('what year were you born')
    year_birth = int(speech.receive_command())
    speech.speak('what is your height')
    height = float(speech.receive_command().lower())
    speech.speak('what is your weight')
    weight = float(speech.receive_command().lower())
    speech.speak('do you exercise regularly')
    exercise = speech.receive_command().lower()
    exercise = convert_smoker_exercise_value(exercise)
    speech.speak('do you smoke')
    smoke = speech.receive_command().lower()
    smoke = convert_smoker_exercise_value(smoke)
    db.create_patient('patients', name, gender, year_birth, height, weight, exercise, smoke)
    image.take_face_photo()



if __name__ == "__main__":
    while True:
        if speech.receive_command() == 'log in':
            speech.speak('to login, face the camera for facial recognition')
            face_login()
        elif speech.receive_command() == 'create account':
            speech.speak('beginning account creation')
            create_account()














