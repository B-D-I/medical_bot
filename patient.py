from database import Database
from modules import datetime
from voice_control import VoiceControl
db = Database()
speech = VoiceControl()


class Patient:
    gender_female = ['female', 'woman', 'lady', 'girl']

    def __init__(self):
        self.__name = None
        self.__is_cardiovascular_risk = False

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def gender(self):
        return db.get_db_data('gender', 'patients', 'first_name', self.name)[0]

    @gender.setter
    def gender(self, new_value: str):
        db.update_db('patients', 'gender', f'{new_value}', 'first_name', self.name)

    @property
    def birth_year(self):
        return db.get_db_data('birth_year', 'patients', 'first_name', self.name)[0]

    def get_age(self):
        current_year = datetime.datetime.now().date()
        current_year = current_year.strftime('%Y')
        year_birth = self.birth_year
        age = int(current_year) - year_birth
        return age

    @property
    def height(self):
        return db.get_db_data('height_cm', 'patients', 'first_name', self.name)[0]

    @property
    def weight(self):
        return db.get_db_data('weight_kg', 'patients', 'first_name', self.name)[0]

    @property
    def is_exercise(self):
        return db.get_db_data('exercise_bool', 'patients', 'first_name', self.name)[0]

    @property
    def is_smoker(self):
        return db.get_db_data('smoker_bool', 'patients', 'first_name', self.name)[0]

    def check_gender(self, gender):
        # infermedica api only accepts male or female
        if gender in self.gender_female:
            return 'female'
        else:
            return 'male'

    @property
    def body_mass(self):
        body_mass = self.weight / (self.height / 100) ** 2
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
        speech.speak(f'your current weight is {self.weight} kilos')
        speech.speak('say in kilos your new weight')
        response = speech.receive_command()
        if response.isnumeric():
            db.update_db('patients', 'weight_kg', int(response), 'first_name', self.name)
            speech.speak(f'updated weight to {response} kilos')
        else:
            speech.speak('incorrect value')

    @property
    def symptom(self):
        speech.speak('starting diagnosis, please state your symptom')
        symptom = speech.receive_command()
        return symptom

    @property
    def is_cardiovascular_risk(self):
        return self.__is_cardiovascular_risk

    @is_cardiovascular_risk.setter
    def is_cardiovascular_risk(self, value: bool):
        self.__is_cardiovascular_risk = value


