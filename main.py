from modules import usb
from voice_control import VoiceControl
from med_bot import MedBot
from patient import Patient
from emergency_alert import EmergencyAlert
from diagnosis import DiagnosisAPI
speech = VoiceControl()
patient = Patient()
alert = EmergencyAlert()
diagnose = DiagnosisAPI()
"""
Medical Bot: Home Diagnosis Device

"""
__author__ = "Nathan Hewett"


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


if __name__ == "__main__":
    while True:
        if speech.receive_command() == 'log in':
            speech.speak('to login, face the camera for facial recognition')
            face_login()













