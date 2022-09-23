import infermedica_api
import infermedica_api.exceptions
from image_classification import ImageClassification
from modules import usb, statistics
from credentials import *
from voice_control import VoiceControl
speech = VoiceControl()
image = ImageClassification()


class DiagnosisAPI:
    lesions = ['mole', 'lesions', 'mole check', 'lesion check', 'moles', 'lesion']
    condition = ['skin conditions', 'rash skin', 'other conditions', 'other', 'other skin condition', 'rash']
    diagnosed_cond = ''

    def __init__(self):
        self.BASE_URL = 'https://api.infermedica.com/v3'
        self.api = infermedica_api.APIv3Connector(app_id=app_id, app_key=app_keys)
        # dev_mode=True, model="infermedica-en"
        self.evidence = []

    def return_api_info(self):
        return self.api.info()

    def diagnosis(self, evidence, age: int, gender: str):
        # used for Infermedica api requests
        request = self.api.diagnosis(evidence=evidence, age=age, sex=gender)
        return request

    def search_symptoms(self, symptom_str: str, age: int):
        """
        user provides their symptom for diagnosis. This is sent to Infermedica API and a possible conditions are
        returned for confirmation
        :param symptom_str: patient symptom
        :param age: patient age
        :return: possible conditions to begin diagnosis
        """
        search_res = []
        for i in symptom_str:
            res = self.api.search(i, age=age)
            for k in res:
                res_p = {}
                res_p['id'] = str(k[str('id')])
                res_p['label'] = str(k[str('label')])
                search_res.append(res_p)
                res_p = None
            return search_res

    @staticmethod
    def convert_smoker_exercise_value(col_type: str):
        # convert and return a boolean from user input
        if col_type in speech.confirmation:
            return 1
        else:
            return 0

    @staticmethod
    def return_choice(response: str):
        choice_id = ''
        if response in speech.confirmation:
            choice_id = 'present'
        elif response in speech.negative:
            choice_id = 'absent'
        elif response in speech.unsure:
            choice_id = 'unknown'
        return choice_id

    @staticmethod
    def heart_rate_analysis(heart_rate: float):
        if int(heart_rate) < 60:
            return 'low'
        elif int(heart_rate) > 100:
            return 'high'
        else:
            return 'average'

    @staticmethod
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
                    return av_heart_rate
                except TypeError or ValueError as error:
                    print('Error: ', error)

    def confirm_symptom(self, patient):
        """
        user can check for similar symptom types before starting diagnosis
        :param patient: current patient
        :return: the id of the chosen symptom for diagnosis
        """
        symptom = patient.symptom
        symptoms = self.search_symptoms(symptom, patient.get_age())
        speech.speak('please confirm the symptom you are experiencing')
        for symptom in symptoms:
            speech.speak(symptom['label'])
        confirmed_symptom = speech.receive_command()
        for symp in symptoms:
            if symp['label'].lower().replace(',', '') == confirmed_symptom:
                return symp['id']

    @staticmethod
    def is_exercise_conv(is_exercise: int):
        # converts the boolean to correlate with diagnosis method
        is_ex = None
        if is_exercise == 0:
            is_ex = 1
        if is_exercise == 1:
            is_ex = 0
        return is_ex

    @staticmethod
    def confirm_if_exposed_to_contagious_cont():
        speech.speak('have you been exposed to anyone with a contagious condition')
        respond = speech.receive_command()
        if respond in speech.confirmation:
            return True

    def cardio_vascular_check(self):
        speech.speak(f'your resting heart rate will now be taken to check if it is above average')
        speech.speak(f'place your finger on the heart rate monitor')
        heart_rate = self.heart_rate()
        rate = self.heart_rate_analysis(heart_rate)
        speech.speak(f'you have a {rate} resting heart rate of {heart_rate}')
        if heart_rate > 100:
            return 1
        else:
            return 0

    def retrieve_diagnosis(self):
        speech.speak(f'previously diagnosed condition is')
        if self.diagnosed_cond is not None:
            for i in self.diagnosed_cond:
                speech.speak(f'{i}')



