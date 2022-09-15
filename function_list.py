from credentials import *
from modules import usb
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


def update_weight():
    speech.speak(f'your current weight is {patient.weight} kilos')
    patient.update_weight()


def start_camera():
    speech.speak('in ten seconds three images will be taken, ensure you adjust the focus')
    image.start_camera()


def start_diagnosis():
    speech.speak('starting diagnosis, please state your symptom')
    query = speech.receive_command()
    symptom_dict = diagnose.symptom_dict
    if query in symptom_dict.keys():
        symptom_id = symptom_dict.get(query)
        evidence = [{'id': f'{symptom_id}', 'choice_id': 'present', 'source': 'initial'}]
        d = diagnose.diagnosis(evidence, patient.get_age(), patient.gender)
        print(d['question'])
        speech.speak(d['question']['text'])
        items = d['question']['item']


# get symptoms:
# symp = diagnose.get_symptom_list(age)
# print(symp[5])
def get_symptoms(symptom_str: str):
    symptoms = diagnose.search_symptoms(symptom_str, patient.get_age())
    return symptoms


def get_confirmed_symptom(symptom_str: str):
    symptoms = get_symptoms(symptom_str)
    for symptom in symptoms:
        speech.speak(symptom['label'])
    confirmed_symptom = speech.receive_command()
    return confirmed_symptom


# symp = 'chest'
# print(get_symptoms(symp))
# get_confirmed_symptom(symp)
# start_diagnosis()
# get_symptom_id('symp')