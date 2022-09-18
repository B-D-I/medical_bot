import infermedica_api.exceptions
from credentials import *
from modules import usb, json, random
from voice_control import VoiceControl
from med_bot import MedBot
from patient import Patient
from image_classification import ImageClassification
from emergency_alert import EmergencyAlert
from diagnosis import DiagnosisAPI


speech = VoiceControl()
image = ImageClassification()
patient = Patient('nathan')
alert = EmergencyAlert(patient.name)
bot = MedBot()
diagnose = DiagnosisAPI()


def tell_time():
    bot.tell_time()


def tell_day():
    bot.tell_day()


def search(query):
    bot.search(query, False)


def send_all_alerts():
    speech.speak('are you sure you wish to send alerts? ')
    response = speech.receive_command().lower()
    if response in speech.confirmation:
        alert.alexa_alert(access_code_alexa)
        alert.twitter_alert(api_key, api_secret, access_token, access_token_secret)
        # self.email_alert(smtp_server, port, sender_email, receiver_email, password)
        speech.speak('alerts have been sent')
        usb.write(b'alert')
        print('alerts sent')
    else:
        speech.speak('alerts have not been sent')


def get_bmi():
    body_mass = patient.body_mass
    bmi = patient.bmi
    speech.speak(f'Your BMI is: {body_mass[:5]}. You are {bmi}, {patient.name}')
    speech.speak('would you like some advice regarding these results')
    query = speech.receive_command()
    if query in speech.confirmation:
        search(f'healthy weight')


def get_heart_rate():
    av_heart_rate = patient.heart_rate()
    speech.speak(f'your heart rate is {str(av_heart_rate)} beats per minute {patient.name}')
    if int(av_heart_rate) < 60:
        speech.speak('this is a low resting heart rate')
    elif int(av_heart_rate) > 100:
        speech.speak('this is a high resting heart rate')
    else:
        speech.speak('this is an average resting heart rate')


def update_weight():
    speech.speak(f'your current weight is {patient.weight} kilos')
    patient.update_weight()


def take_face_photo():
    speech.speak('please confirm your first name')
    username = speech.receive_command()
    image.take_image(2, username)


def take_skin_photo():
    image.take_image(3, 'skin')


def confirm_symptom():
    symptom = patient.symptom
    symptoms = diagnose.search_symptoms(symptom, patient.get_age())
    speech.speak('please confirm the symptom you are experiencing')
    for symptom in symptoms:
        speech.speak(symptom['label'])
    confirmed_symptom = speech.receive_command()
    for symp in symptoms:
        if symp['label'].lower().replace(',', '') == confirmed_symptom:
            return symp['id']

