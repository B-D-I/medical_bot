from credentials import *
from modules import usb
from voice_control import VoiceControl
from med_bot import MedBot
from patient import Patient
from image_classification import ImageClassification
from emergency_alert import EmergencyAlert


speech = VoiceControl()
image = ImageClassification()
patient = Patient('nathan')
alert = EmergencyAlert(patient.name)
bot = MedBot()


def tell_time():
    bot.tell_time()


def tell_day():
    bot.tell_day()


def search(query):
    bot.search(query)


def send_all_alerts():
    speech.speak('are you sure you wish to send alerts? ')
    response = speech.receive_command().lower()
    if response in speech.confirmation:
        alert.alexa_alert(access_code_alexa)
        alert.twitter_alert(api_key, api_secret, access_token, access_token_secret)
        # self.email_alert(smtp_server, port, sender_email, receiver_email, password)
        speech.speak("alerts have been sent")
        usb.write(b'alert')
        print('alerts sent')
    else:
        speech.speak('alerts have not been sent')


def get_bmi():
    body_mass = patient.body_mass
    bmi = patient.bmi
    speech.speak(f"Your BMI is: {body_mass[:5]}. You are {bmi}, {patient.name}")
    speech.speak("would you like some advice regarding these results")
    query = speech.receive_command()
    if query in speech.confirmation:
        # web_scrape(bmi_weight)
        speech.speak("no function yet")


def get_heart_rate():
    av_heart_rate = patient.heart_rate()
    speech.speak(f"your heart rate is {str(av_heart_rate)} beats per minute {patient.name}")


def update_weight():
    speech.speak(f'your current weight is {patient.weight} kilos')
    patient.update_weight()


def start_camera():
    speech.speak("in ten seconds three images will be taken, ensure you adjust the focus")
    image.start_camera()



