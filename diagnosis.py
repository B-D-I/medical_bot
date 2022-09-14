from credentials import *
import infermedica_api


class DiagnosisAPI:

    def __init__(self):
        self.BASE_URL = "https://api.infermedica.com/v3"
        self.api = infermedica_api.APIv3Connector(app_id=app_id, app_key=app_keys)
        # dev_mode=True, model="infermedica-en"

    def print_api_info(self):
        print(self.api.info())

    @property
    def symptom_dict(self):
        symptom_dict = {
            'fever': 's_98',
            'headache': 's_21',
            'knee_pain': 's_581',
            'colic stomach pain': 's_1848'
        }
        return symptom_dict

    def diagnosis(self, evidence, age, gender):
        request = self.api.diagnosis(evidence=evidence, age=age, sex=gender)
        return request

    def get_symptom_list(self, age):
        age_unit = 'year'
        return self.api.symptom_list(age=age, age_unit=age_unit)

