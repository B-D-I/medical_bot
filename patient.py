import datetime


class Patient:
    gender_female = ['female', 'woman', 'lady', 'girl']

    def __init__(self):
        self.__name = None
        self.__gender = None
        self.__birth_year = None
        self.__age = None
        self.__height = None
        self.__weight = None
        self.__is_exercise = None
        self.__is_smoker = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def gender(self):
        # infermedica api only accepts male or female
        if self.__gender in self.gender_female:
            return 'female'
        else:
            return 'male'

    @gender.setter
    def gender(self, value: str):
        self.__gender = value

    @property
    def birth_year(self):
        return self.__birth_year

    @birth_year.setter
    def birth_year(self, value: float):
        self.__birth_year = value

    @property
    def age(self):
        current_year = datetime.datetime.now().date()
        current_year = current_year.strftime('%Y')
        year_birth = self.birth_year
        age = int(current_year) - year_birth
        return age

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, value: float):
        self.__height = value

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value: float):
        self.__weight = value

    @property
    def is_exercise(self):
        if self.__is_exercise == 1:
            return 'yes'
        else:
            return 'no'

    @is_exercise.setter
    def is_exercise(self, value):
        self.__is_exercise = value

    @property
    def is_smoker(self):
        if self.__is_smoker == 1:
            return 'yes'
        else:
            return 'no'

    @is_smoker.setter
    def is_smoker(self, value):
        self.__is_smoker = value

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


