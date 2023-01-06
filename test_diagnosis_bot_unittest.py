import unittest
from credentials import file_hash
from patient import Patient
from camera import Camera
from diagnosis import Diagnosis
from image_classifier import ImageClassifier

camera = Camera()
patient = Patient()
classifier = ImageClassifier()
patient.name = 'test'
bot = Diagnosis(patient, camera)


class TestMedBotFunctions(unittest.TestCase):

    def test_model_integrity(self):
        self.assertEqual(classifier.integrity_check(), file_hash)

    def test_get_name(self):
        result = patient.name
        expected = 'test'
        self.assertEqual(result, expected)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
