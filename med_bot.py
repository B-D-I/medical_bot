from modules import datetime
from modules import random, json
from voice_control import VoiceControl
from image_classification import ImageClassification
from emergency_alert import EmergencyAlert
from diagnosis import DiagnosisAPI
import wikipedia
import wikipedia.exceptions
import infermedica_api.exceptions
speech = VoiceControl()
image = ImageClassification()
alert = EmergencyAlert()
diagnose = DiagnosisAPI()


class MedBot:

    def __init__(self, current_patient):
        self.current_patient = current_patient
        self.func_dict = {
            "time": self.tell_time,
            "date": self.tell_day,
            "alert": alert.send_all_alerts,
            "bmi": self.get_bmi,
            "heart_rate": self.get_heart_rate,
            "diagnose_skin_photo": self.diagnose_skin_photo,
            "take_face_photo": image.take_face_photo,
            "set_camera": image.set_camera,
            "update_weight": self.current_patient.update_weight,
            "diagnosis": self.diagnosis,
        }

    @staticmethod
    def login_recognition(name):
        if image.facial_recognition(name):
            return True

    @staticmethod
    def tell_day():
        day = datetime.datetime.today().weekday() + 1
        month = datetime.datetime.today().month
        year = datetime.datetime.today().year
        date = datetime.datetime.today().day
        day_of_week = ''
        day_dict = {1: 'Monday', 2: 'Tuesday',
                    3: 'Wednesday', 4: 'Thursday',
                    5: 'Friday', 6: 'Saturday',
                    7: 'Sunday'}
        month_dict = {1: 'January', 2: 'February', 3: 'March',
                      4: 'April', 5: 'May', 6: 'June',
                      7: 'July', 8: 'August', 9: 'September',
                      10: 'October', 11: 'November', 12: 'December'}

        if day in day_dict.keys():
            day_of_week = day_dict[day]
        if month in month_dict.keys():
            month_of_year = month_dict[month]
            speech.speak("Today is " + day_of_week, date, month_of_year, year)

    @staticmethod
    def tell_time():
        # Place the string format of time into time variable -> then sliced for specific values
        time = str(datetime.datetime.now())
        time_hour = time[11:13]
        time_min = time[14:16]
        speech.speak("The time is" + time_hour + "Hours and" + time_min + "Minutes")

    def user_search(self, query):
        self.search(query, False)

    @staticmethod
    def search(query, is_test: bool):
        """
        When called will use the Wikipedia module to carry out a search of user's query. The 'tell me about' keyword is
        removed, to ensure only the relevant query is searched. The information will then be outputted, unless there query
        is too unambiguous, in which case the user will be told to rectify the command.
        :param is_test: whether function is being called for unit testing
        :param query: This is imported from the conversation() function, and contains the string format of
        the user's spoken query.
        :return: The required information will be outputted, or user will be notified to be more specific.
        """
        # Remove the query command, and search user input
        query = query.replace("tell me about", "")
        try:
            # place the result into a variable. confirm amount of sentences spoken
            result = wikipedia.summary(query, sentences=3)
            if not is_test:
                speech.speak(result)
            else:
                print(result)
        # This exception is used if the user searches an unambiguous or too broad a query
        except wikipedia.exceptions.DisambiguationError as error:
            if not is_test:
                print(error)
                speech.speak(
                    f"sorry, that query is too broad, could you try again and re-phrase what you would like to "
                    f"search")
            else:
                print(error)

    def conversation(self):
        """
           This function opens the 'chat_conv' json file, and listens to voice commands from the user.
           If a query is recognised from the input array in the json file, an output from the relevant
           output list will be randomly selected, and spoken. If the input query has a function allocated,
           these will be included in the 'func_dict' dictionary, and called if queried, using the 'call_func'
           function. This 'conversation' function also listens for the keyword 'tell me about', which initiates
           the 'search()' function, with the query as a parameter.
        """
        with open("chat_conv.json", "r") as chat_file:
            chat_dict = json.load(chat_file)
        while True:
            query = speech.receive_command()
            if "tell me about" in query:
                self.user_search(query)
            for i in chat_dict["conversation"]:  # for items in dict
                if query in i['inputs']:  # if query found
                    if i['outputs'] != "":
                        speech.speak(random.choice(i['outputs']), f'{self.current_patient.name}')  # speak the outputs + name
                        func = i['conv_name']
                        self.call_func(func)
                        continue

    def call_func(self, func):  # parameter given from conversation func
        for key in self.func_dict:  # if the key is same as func query, call function
            if func == key:
                self.func_dict[key]()

    def get_bmi(self):
        body_mass = self.current_patient.body_mass
        bmi = self.current_patient.bmi
        speech.speak(f'Your BMI is: {body_mass[:5]}. You are {bmi}, {self.current_patient.name}')
        speech.speak('would you like some advice regarding these results')
        query = speech.receive_command()
        if query in speech.confirmation:
            self.search(f'healthy weight', False)

    def get_heart_rate(self):
        av_heart_rate = diagnose.heart_rate()
        speech.speak(f'your heart rate is {str(av_heart_rate)} beats per minute {self.current_patient.name}')
        rate = diagnose.heart_rate_analysis(av_heart_rate)
        speech.speak(f'this is a {rate} resting heart rate')

    def diagnosis(self):
        self.diagnose_respond(True, self.current_patient)

    def diagnose_respond(self, is_initial: bool, *provided_symptom):
        """
        is_initial: bool,
        This recursive function uses the Diagnosis object and Infermedica API to perform real time diagnoses. The user provides
        evidence to be assessed. If a condition is determined at over 70%, it will be given to the user
        :param is_initial: Is the function being called for the first time
        :return: Function will be called recursively until a diagnosis of over 70%is made
        """
        if is_initial:
            diagnose.evidence.clear()
            symptom_id = diagnose.confirm_symptom(self.current_patient)
            diagnose.evidence.append({'id': f'{symptom_id}', 'choice_id': 'present', 'source': 'initial'})
        d = diagnose.diagnosis(diagnose.evidence, self.current_patient.get_age(), self.current_patient.gender)
        if provided_symptom:
            diagnose.evidence.append({'id': f'{provided_symptom}', 'choice_id': 'present', 'source': 'initial'})
            d = diagnose.diagnosis(diagnose.evidence, self.current_patient.get_age(), self.current_patient.gender)
        try:
            print(d['question']['text'])
            for condition in d['conditions']:
                if condition['probability'] > 0.7:
                    probability = "{:.2f}".format(condition["probability"])
                    speech.speak(f'based on these answers it is believed you have '
                                 f'{condition["common_name"]}, with a probability of {probability} percent')
                    self.conversation()
                else:
                    speech.speak(d['question']['text'])
                    if d['question']['text'] is not None:
                        for item in d['question']['items']:
                            try:
                                speech.speak(item['name'])
                                id = item['id']
                                response = speech.receive_command()
                                choice = diagnose.return_choice(response)
                                diagnose.evidence.append({'id': id, 'choice_id': choice})
                                self.diagnose_respond(False)
                            except infermedica_api.exceptions.BadRequest as err:
                                print(err)
                                continue
        except TypeError as error:
            print(error)

    def diagnose_skin_photo(self):
        speech.speak('confirm if image is of a mole or other skin condition')
        skin_issue = speech.receive_command()
        if skin_issue in diagnose.lesions:
            diagnosis = image.return_skin_classification('lesions')
            speech.speak(f'image {diagnosis[0]}, has been diagnosed as a {diagnosis[1]}')

        elif skin_issue in diagnose.condition:
            diagnosis = image.return_skin_classification('conditions')
            speech.speak(
                f'image {diagnosis[0]}, has been diagnosed as {diagnosis[1]}, with a percentage of {diagnosis[2]}')
            if diagnosis[1] != 'normal_skin':
                self.further_skin_diagnosis(diagnosis[1])
        else:
            speech.speak('not recognised')

    @staticmethod
    def cardio_vascular_check():
        speech.speak(f'your resting heart rate will now be taken to check if it is above average')
        speech.speak(f'place your finger on the heart rate monitor')
        heart_rate = diagnose.heart_rate()
        rate = diagnose.heart_rate_analysis(heart_rate)
        speech.speak(f'you have a {rate} resting heart rate of {heart_rate}')
        if heart_rate > 100:
            return 1
        else:
            return 0

    def further_skin_diagnosis(self, condition):
        speech.speak(f'due to this image being classified as {condition}, further diagnosis will be performed')
        is_smoker = self.current_patient.is_smoker
        is_exercise = self.current_patient.is_exercise
        is_high_bpm = self.cardio_vascular_check()
        body_mass = float(self.current_patient.body_mass)
        bmi = self.current_patient.bmi
        print(body_mass)
        if body_mass > 30:
            body_mass = 1
        else:
            body_mass = 0
        cardiovascular_risk = body_mass + is_smoker + is_exercise + is_high_bpm
        print(body_mass, is_smoker, is_exercise, is_high_bpm)
        print(cardiovascular_risk)

from patient import Patient
patient = Patient()
patient.name ='nathan'
bot = MedBot(patient)
bot.further_skin_diagnosis('measles')
    #
    # @staticmethod
    # def further_diagnose(first_response, second_response, condition_type):
    #     if first_response and second_response in speech.confirmation:
    #         speech.speak(f'based on these image results and questions, it is advisable to speak to a doctor as soon as '
    #                      f'possible, regarding {condition_type}. Would you like further information')
    #         response = speech.receive_command()
    #         if response in speech.confirmation:
    #             # bot.search(f'tell me about {condition_type}', False)
    #             pass

    # def skin_further_diagnosis(self, condition_type):
    #     for cond in self.conditions_symptoms.keys():
    #         if cond.split('_', 1)[0] == condition_type:
    #             speech.speak(self.conditions_symptoms[cond][0])
    #             first_resp = speech.receive_command()
    #             speech.speak(self.conditions_symptoms[cond][1])
    #             second_resp = speech.receive_command()
    #             if condition_type in ['psoriasis', 'rosacea', 'eczema', 'atopic_dermatitis']:
    #                 self.cardio_vascular_check()
    #             self.further_diagnose(first_resp, second_resp, condition_type)
#     conditions_symptoms = {
#         'eczema_symptoms': ['is the rash itchy', 'do you have a history of asthma or hay fever'],
#         'chickenpox_symptoms': ['do you have an itchy blister rash', 'have you been exposed to anyone with chickenpox'],
#         'measles_symptoms': ['have you been exposed to anyone with measles', 'do you have a fever'],
#         'psoriasis_symptoms': ['does anyone in your family have psoriasis', 'do you have itchy skin'],
#         'rosacea_symptoms': ['is you skin sensitive', 'do you have red patches of skin'],
#         'vasculitis_symptoms': ['do you have a fever', 'are you fatigued'],
#         'malignant lesion_symptoms': ['do you have a history of sunburn', 'has anyone in your family had a malignant lesion']
#     }