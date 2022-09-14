import unittest
from database import Database
from med_bot import MedBot
from patient import Patient
import wikipedia.exceptions
import datetime

db = Database()
bot = MedBot()
patient = Patient('nathan')


class TestMedBotFunctions(unittest.TestCase):

    def test_db_selection(self):
        table = 'patients'
        col = 'patient_id'
        user_id = 1
        result = db.get_db_data(col, table, col, user_id)[0]
        self.assertEqual(user_id, result)
        self.assertIsNotNone(result)

    def test_get_table_data(self):
        result = db.get_all_table_data('patients')
        self.assertIsNotNone(result)

    def test_search_function(self):
        self.assertRaises(wikipedia.exceptions.PageError, bot.search, 'tell me about pepper pig', True)

    def test_get_name(self):
        result = patient.name
        expected = 'nathan'
        self.assertEqual(result, expected)
        self.assertIsNotNone(result)

    def test_get_age(self):
        result = patient.get_age()
        current_year = datetime.datetime.now().date()
        current_year = current_year.strftime('%Y')
        age = int(current_year) - patient.birth_year
        self.assertEqual(result, age)
        self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
