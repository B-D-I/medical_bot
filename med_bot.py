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
    """
    This class provides the methods that are directly called during conversation with the patient
    """

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
            "diagnosis": self.initial_infermedica_diagnosis,
            "retrieve_diagnosis": self.retrieve_diagnosis
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

    def initial_infermedica_diagnosis(self):
        diagnose.evidence.clear()
        symptom_id = diagnose.confirm_symptom(self.current_patient)
        diagnose.evidence.append({'id': f'{symptom_id}', 'choice_id': 'present', 'source': 'initial'})
        self.infermedica_diagnosis()

    def infermedica_diagnosis(self):
        """
        Initial diagnosis evidence array is appended prior to calling this method.
        This recursive function uses the Diagnosis object and Infermedica API to perform real time diagnoses. The user provides
        evidence to be assessed. If a condition is determined at over 70%, it will be given to the user
        :param is_initial: Is the function being called for the first time
        :return: Function will be called recursively until a diagnosis of over 70% is made
        """
        d = diagnose.diagnosis(diagnose.evidence, self.current_patient.get_age(), self.current_patient.gender)
        try:
            print(d['question']['text'])
            for condition in d['conditions']:
                if condition['probability'] > 0.7:
                    probability = "{:.2f}".format(condition["probability"])
                    print(probability)
                    speech.speak(f'based on these answers it is believed you have '
                                 f'{condition["common_name"]}, with a probability of {probability} percent')
                    diagnose.diagnosed_verbal = condition["common_name"]
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
                                self.infermedica_diagnosis()
                            except infermedica_api.exceptions.BadRequest as err:
                                print(err)
                                continue
        except TypeError as error:
            print(error)

    def diagnose_skin_photo(self):
        # provide patient with a diagnosis of a provided skin photo -> if image is diagnosed as a known condition,
        # then further methods will be called
        speech.speak('confirm if image is of a mole or other skin condition')
        skin_issue = speech.receive_command()
        if skin_issue in diagnose.lesions:
            diagnosis = image.return_skin_classification('lesions')
            speech.speak(f'image {diagnosis[0]}, has been diagnosed as a {diagnosis[1]} lesion')
            diagnose.diagnosed_image = f'{diagnosis[1]} lesion'
        elif skin_issue in diagnose.condition:
            diagnosis = image.return_skin_classification('conditions')
            if diagnosis[1] != 'normal_skin':
                self.further_skin_diagnosis(diagnosis[1], diagnosis[2])
            else:
                speech.speak(
                    f'image {diagnosis[0]}, has been diagnosed as {diagnosis[1]}')
            diagnose.diagnosed_image = diagnosis[1]
        else:
            speech.speak('not recognised')

    def calculate_cardiovascular_risk(self, is_smoker: int, is_exercise: int, is_high_bpm: int, body_mass: float):
        if body_mass > 25:
            body_mass = 1
        else:
            body_mass = 0
        cardiovascular_risk = body_mass + is_smoker + is_exercise + is_high_bpm
        if cardiovascular_risk >= 3:
            self.current_patient.is_cardiovascular_risk = True

    def skin_infermedica_diagnosis(self):
        # start diagnosis with 'dermatological changes' set as symptom id
        diagnose.evidence.clear()
        diagnose.evidence.append({'id': 's_241', 'choice_id': 'present', 'source': 'initial'})
        self.infermedica_diagnosis()

    def further_skin_diagnosis(self, condition, percentage):
        """
        This method is called if the result of a skin condition classification is positive for a condition. The patients
        cardiovascular and other data will be assessed and contributed towards the diagnosis. The patient will then
        be asked if they wish to undergo further diagnosis, provided by the Infermedica API.
        :param condition: determined from skin classification
        :param percentage: percentage of prediction
        :return: Infermedica API diagnosis
        """
        is_smoker = self.current_patient.is_smoker
        is_exercise = self.current_patient.is_exercise
        is_exercise = diagnose.is_exercise_conv(is_exercise)
        is_high_bpm = diagnose.cardio_vascular_check()
        body_mass = float(self.current_patient.body_mass)
        self.calculate_cardiovascular_risk(is_smoker, is_exercise, is_high_bpm, body_mass)
        speech.speak(f'The image has been classified as {condition}, with a probability of {percentage}')
        if condition == 'chickenpox' or condition == 'measles' and diagnose.confirm_if_exposed_to_contagious_cont():
            speech.speak('you are at a higher risk of having this contagious condition, as you have been exposed to '
                         'others who also have it')
        if condition in ['psoriasis', 'rosacea', 'eczema', 'atopic_dermatitis'] and self.current_patient.is_cardiovascular_risk:
            speech.speak('you are at a higher risk of having this condition, due to you bmi,'
                         'resting heart rate, and other health information, you are of a higher cardiovascular risk')
        speech.speak('would you like to undergo a further skin diagnosis')
        response = speech.receive_command()
        if response in speech.confirmation:
            self.skin_infermedica_diagnosis()

    def retrieve_diagnosis(self):
        speech.speak(f'do wish to hear your recent image or verbal diagnosis')
        resp = speech.receive_command()
        if resp in ['image', 'photo', 'skin image', 'picture'] and diagnose.diagnosed_image is not None:
            self.give_diagnosis(diagnose.diagnosed_image)
        elif resp in ['verbal', 'spoken', 'speech'] and diagnose.diagnosed_verbal is not None:
            self.give_diagnosis(diagnose.diagnosed_verbal)

    def give_diagnosis(self, diagnosis):
        speech.speak(f'previous image diagnosis is {diagnosis}. would you like more information')
        resp = speech.receive_command()
        if resp in speech.confirmation:
            self.search(f'tell me about {diagnosis}', False)
