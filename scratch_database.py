import sqlite3
from sqlite3 import Error as sqlError
from scratch_modules import Union
from hashlib import sha256


class Database:
    """
    Database methods contain prepared statements to reduce the risk of SQL Injection. This attack is less of a concern
    for this project, as the user cannot type commands as input and special characters cannot be verbally
    commanded.
    """

    def __init__(self):
        self.conn = sqlite3.connect("patient_database.db")
        self.c = self.conn.cursor()

    def get_db_data(self, required_col: str, table_name: str, col_name: str,  value: Union[str, int, float]):
        try:
            arg = [value]
            self.c.execute(f"SELECT {required_col} FROM {table_name} WHERE {col_name} =?", arg)
            row = self.c.fetchone()
            return row
        except sqlError or ValueError as error:
            print(error)

    def get_all_table_data(self, table_name: str):
        try:
            self.c.execute(f"SELECT * FROM {table_name}")
            rows = self.c.fetchall()
            return rows
        except sqlError or ValueError as error:
            print(error)

    def update_db(self, table_name: str, col_name: str, new_value: Union[int, str, float], reference_col: str,
                  reference_value: Union[int, str, float]):
        try:
            arg = [new_value]
            self.c.execute(f"UPDATE {table_name} SET {col_name} =? WHERE {reference_col} = '{reference_value}'", arg)
            self.conn.commit()
        except sqlError or ValueError as error:
            print(error)
        # self.conn.close()

    def delete_from_db(self, table_name: str, col_name: str, col_value: Union[str, int, float]):
        try:
            arg = [col_value]
            self.c.execute(f"DELETE FROM {table_name} WHERE {col_name} =?", arg)
            self.conn.commit()
        except sqlError or ValueError as error:
            print(error)
        # self.conn.close()

    def refresh_db(self, table_name: str):
        try:
            self.c.execute(f"DELETE FROM {table_name}")
            self.conn.commit()
        except sqlError or ValueError as error:
            print(error)
        # self.conn.close()

    def create_patient(self, table_name: str, patient_name: str, patient_gender: str, patient_birth_year: int,
                       patient_height: float, patient_weight: float, is_exercise: int, is_smoker: int):
        try:
            args = [patient_name, patient_gender, patient_birth_year, patient_height, patient_weight, is_exercise, is_smoker]
            self.c.execute(f"INSERT INTO {table_name} (first_name, gender, birth_year, height_cm, weight_kg, "
                           f"exercise_bool, smoker_bool) VALUES (?,?,?,?,?,?,?)", args)
            self.conn.commit()
        except sqlError or ValueError as error:
            print(error)
        # self.conn.close()

    def create_patients_table(self):
        try:
            self.c.execute("""
            CREATE TABLE IF NOT EXISTS patients ([patient_id] INTEGER PRIMARY KEY, [first_name] TEXT, 
            [gender] TEXT, [birth_year] INTEGER, [height_cm] REAL, [weight_kg] REAL, [exercise_bool] INTEGER,
            [smoker_bool] INTEGER )
            """)
            self.conn.commit()
        except sqlError as error:
            print(error)

    @staticmethod
    def integrity_check(file_path):
        # check hash of file(used for models)
        with open(file_path, 'rb') as f:
            file = f.read()
            return sha256(file).hexdigest()
