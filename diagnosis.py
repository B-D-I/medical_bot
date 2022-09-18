from credentials import *
from voice_control import VoiceControl
import infermedica_api
import infermedica_api.exceptions

speech = VoiceControl()


class DiagnosisAPI:

    def __init__(self):
        self.BASE_URL = 'https://api.infermedica.com/v3'
        self.api = infermedica_api.APIv3Connector(app_id=app_id, app_key=app_keys)
        # dev_mode=True, model="infermedica-en"
        self.evidence = []

    def print_api_info(self):
        print(self.api.info())

    def diagnosis(self, evidence, age, gender):
        request = self.api.diagnosis(evidence=evidence, age=age, sex=gender)
        return request

    def search_symptoms(self, symptom_str, age):
        search_res = []
        for i in symptom_str:
            res = self.api.search(i, age=age)
            for k in res:
                res_p = {}
                res_p['id'] = str(k[str('id')])
                res_p['label'] = str(k[str('label')])
                search_res.append(res_p)
                res_p = None
            return search_res

    @staticmethod
    def return_choice(response):
        choice_id = ''
        if response in speech.confirmation:
            choice_id = 'present'
        elif response in speech.negative:
            choice_id = 'absent'
        elif response in speech.unsure:
            choice_id = 'unknown'
        return choice_id
