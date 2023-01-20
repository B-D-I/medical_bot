import os
import unittest
from scratch_database import Database
from scratch_med_bot import MedBot
from patient import Patient
from scratch_image_classification import ImageClassification
from communication import Communication
from scratch_diagnosis import DiagnosisAPI
from scratch_credentialsOLD import conditions_hash, lesions_hash
import wikipedia.exceptions
import datetime

patient = Patient()
patient.name = 'test_images'
db = Database()
bot = MedBot(patient)
image = ImageClassification()
diagnosis = DiagnosisAPI()
speech = Communication()


class TestMedBotFunctions(unittest.TestCase):


    def test_get_name(self):
        result = patient.name
        expected = 'test_images'
        self.assertEqual(result, expected)
        self.assertIsNotNone(result)

    def test_get_age(self):
        result = patient.get_age()
        current_year = datetime.datetime.now().date()
        current_year = current_year.strftime('%Y')
        age = int(current_year) - patient.birth_year
        self.assertEqual(result, age)
        self.assertIsNotNone(result)

    def test_infermedica_api_connection(self):
        result = diagnosis.return_api_info()
        self.assertIsNotNone(result)

    def test_choice_response(self):
        # confirm possible response choices correlate to the api choice id
        for i in speech.confirmation:
            self.assertEqual(diagnosis.return_choice(i), 'present')
        for j in speech.negative:
            self.assertEqual(diagnosis.return_choice(j), 'absent')
        for l in speech.unsure:
            self.assertEqual(diagnosis.return_choice(l), 'unknown')

    def test_model_integrity(self):
        self.assertEqual(db.integrity_check('models/converted_conditions_model.tflite'), conditions_hash)
        self.assertEqual(db.integrity_check('models/converted_lesions_model.tflite'), lesions_hash)

    def test_return_confirmation_binary(self):
        expected = 1
        result = speech.return_confirmation_binary('yes')
        self.assertIsNotNone(result)
        self.assertEqual(expected, result)

    def test_convert_smoker_exercise_value(self):
        expected = 1
        result = diagnosis.convert_smoker_exercise_value('yes')
        self.assertIsNotNone(result)
        self.assertEqual(expected, result)

    def test_heart_rate_analysis(self):
        expected_low = 'low'
        expected_av = 'average'
        expected_high = 'high'
        result_one = diagnosis.heart_rate_analysis(50)
        result_two = diagnosis.heart_rate_analysis(70)
        result_three = diagnosis.heart_rate_analysis(110)
        self.assertIsNotNone(result_one)
        self.assertEqual(result_one, expected_low)
        self.assertEqual(result_two, expected_av)
        self.assertEqual(result_three, expected_high)

    def test_exercise_conversion(self):
        expected_one = 1
        expected_two = 0
        result_one = diagnosis.is_exercise_conv(0)
        result_two = diagnosis.is_exercise_conv(1)
        self.assertIsNotNone(result_one)
        self.assertEqual(result_one, expected_one)
        self.assertEqual(result_two, expected_two)

    def test_skin_lesion_model(self):
        # iterate over test_images skin lesion files and confirm expected result
        image_path = f'images/test_lesions/'
        for filename in os.listdir(image_path):
            diagnose = image.prediction(image_path, 'lesions', filename)
            # get name of files (without ext), then compare with classification
            file = diagnose[0][:-5]
            self.assertIsNotNone(diagnose)
            self.assertEqual(diagnose[1], file)

    def test_skin_conditions_model(self):
        image_path = f'images/test_conditions/'
        for filename in os.listdir(image_path):
            diagnose = image.prediction(image_path, 'conditions', filename)
            # get filename before extension
            file = diagnose[0].split('.', 1)[0]
            self.assertIsNotNone(diagnose)
            self.assertEqual(diagnose[1], file)


if __name__ == '__main__':
    unittest.main()
