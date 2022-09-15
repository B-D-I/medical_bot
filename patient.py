from database import Database
from modules import datetime, usb, statistics
from voice_control import VoiceControl
db = Database()
speech = VoiceControl()


class Patient:

    def __init__(self, name: str):
        self.name = name
        self.__gender = db.get_db_data('gender', 'patients', 'first_name', name)[0]
        self.__birth_year = db.get_db_data('birth_year', 'patients', 'first_name', name)[0]
        self.__height = db.get_db_data('height_cm', 'patients', 'first_name', name)[0]
        self.__weight = db.get_db_data('weight_kg', 'patients', 'first_name', name)[0]
        self.__is_exercise = db.get_db_data('exercise_bool', 'patients', 'first_name', name)[0]
        self.__is_smoker = db.get_db_data('smoker_bool', 'patients', 'first_name', name)[0]

    @property
    def gender(self):
        return self.__gender

    @gender.setter
    def gender(self, new_value: str):
        db.update_db('patients', 'gender', f'{new_value}', 'first_name', self.name)

    @property
    def birth_year(self):
        return self.__birth_year

    def get_age(self):
        current_year = datetime.datetime.now().date()
        current_year = current_year.strftime('%Y')
        year_birth = self.birth_year
        age = int(current_year) - year_birth
        return age

    @property
    def height(self):
        return self.__height

    @property
    def weight(self):
        return self.__weight

    @property
    def is_exercise(self):
        return self.__is_exercise

    @property
    def is_smoker(self):
        return self.__is_smoker

    @property
    def body_mass(self):
        body_mass = self.__weight / (self.height / 100) ** 2
        body_mass = "{:.2f}".format(body_mass)
        return body_mass

    @property
    def bmi(self):
        body_mass = str(self.body_mass)
        if body_mass <= str(18.4):
            bmi_weight = "underweight"
        elif body_mass <= str(24.9):
            bmi_weight = "healthy"
        elif body_mass <= str(29.9):
            bmi_weight = "overweight"
        elif body_mass <= str(34.9):
            bmi_weight = "severely overweight"
        elif body_mass <= str(39.9):
            bmi_weight = "obese"
        else:
            bmi_weight = "severely overweight"
        return bmi_weight

    def update_weight(self):
        speech.speak('say in kilos your new weight')
        response = speech.receive_command()
        if response.isnumeric():
            db.update_db('patients', 'weight_kg', int(response), 'first_name', self.name)
            speech.speak(f'updated weight to {response} kilos')
        else:
            speech.speak('incorrect value')

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
                    # speech.speak(f"your heart rate is {str(av_heart_rate)} beats per minute {self.name}")
                    return av_heart_rate
                except TypeError or ValueError as error:
                    print('Error: ', error)

    @property
    def symptom(self):
        speech.speak('starting diagnosis, please state your symptom')
        symptom = speech.receive_command()
        return symptom

