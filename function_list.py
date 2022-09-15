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


def take_face_photo():
    speech.speak('please confirm your first name')
    username = speech.receive_command()
    image.take_image(2, username)


def take_skin_photo():
    image.take_image(3, 'skin')





# get symptoms:
# symp = diagnose.get_symptom_list(age)
# print(symp[5])
def get_symptoms():
    symptom = patient.symptom
    symptoms = diagnose.search_symptoms(symptom, patient.get_age())
    return symptoms


def confirm_symptom():
    symptoms = get_symptoms()
    speech.speak('please confirm the symptom you are experiencing')
    for symptom in symptoms:
        speech.speak(symptom['label'])
    confirmed_symptom = speech.receive_command()
    for symp in symptoms:
        if symp['label'].lower().replace(',', '') == confirmed_symptom:
            return symp['id']


def return_choice(response):
    choice_id = ''
    if response in speech.confirmation:
        choice_id = 'present'
    elif response in speech.negative:
        choice_id = 'absent'
    elif response in speech.unsure:
        choice_id = 'unknown'
    return choice_id


def initial_respond_diagnosis(symptom_id: str):
    evidence = [{'id': f'{symptom_id}', 'choice_id': 'present', 'source': 'initial'}]
    d = diagnose.diagnosis(evidence, patient.get_age(), patient.gender)
    # speech.speak(d['question']['text'])
    # choice = speech.receive_command()
    print(d['question'])
    choice = input(d['question']['text'])
    choice_id = return_choice(choice)
    resp_id = ''
    for i in d['question']['items']:
        resp_id = i['id']
    print(choice_id, ' ', resp_id)
    # respond_diagnosis(resp_id, choice_id)


def respond_diagnosis(symptom_id, choice_id):
    evidence = [{'id': f'{symptom_id}', 'choice_id': f'{choice_id}', 'source': 'initial'}]
    d = diagnose.diagnosis(evidence, patient.get_age(), patient.gender)
    # speech.speak(d['question']['text'])
    # choice = speech.receive_command()
    choice = input(d['question']['text'])
    choice_id = return_choice(choice)
    resp_id = ''
    for i in d['question']['items']:
        resp_id = i['id']
    print(choice_id, ' ', resp_id)
    # respond_diagnosis(resp_id, choice_id)

# seems to repeat in loop?
def read_and_respond(symptom_id, choice_id):
    if choice_id == 'unknown':
        evidence = [{'id': f'{symptom_id}', 'choice_id': 'present', 'source': 'initial'}]
    else:
        evidence = [{'id': f'{symptom_id}', 'choice_id': f'{choice_id}', 'source': 'initial'}]
    d = diagnose.diagnosis(evidence, patient.get_age(), patient.gender)
    # speak
    print(d['question'])
    for item in d['question']['items']:
        # speak
        print(item['name'])
        id = item['id']
        # receive
        response = input('present, absent or unknown: ').lower()
        if response == 'present':
            read_and_respond(id, 'present')



# def start_diagnosis():
#     symptom = patient.symptom
#     symptom_dict = diagnose.symptom_dict
#     if symptom in symptom_dict.keys():
#         symptom_id = symptom_dict.get(symptom)
#         evidence = [{'id': f'{symptom_id}', 'choice_id': 'present', 'source': 'initial'}]
#         d = diagnose.diagnosis(evidence, patient.get_age(), patient.gender)
#         print(d['question'])
#         speech.speak(d['question']['text'])
#         items = d['question']['item']

"""         'fever': 's_98',
            'headache': 's_21',
            'knee_pain': 's_581',
            'colic stomach pain': 's_1848'
    """
# get_confirmed_symptom()
# initial_respond_diagnosis('s_98')
# respond_diagnosis('s_143', 'present')

read_and_respond('s_98', 'unknown')




