import os
import random
import smtplib
import ssl
from credentials import smtp_server, port, sender_email, receiver_email, password
from device_voice_control import VoiceControl
from image_classifier import ImageClassifier
from diagnosis_triage_report import TriageReport
speech = VoiceControl()
classifier = ImageClassifier()
report = TriageReport()


class DiagnosisBot:

    def __init__(self, current_patient, camera):
        self.current_patient = current_patient
        self.camera = camera
        self.predictions_results = []

    def start_diagnosis(self, image_type: str):
        # speech.speak('image will be taken in 10 seconds')
        self.camera.take_image(1, image_type)
        image_path = f'images/{image_type}_images/'
        for filename in os.listdir(image_path):
            diagnosis = classifier.prediction(image_path, image_type, filename)
            self.predictions_results.append(diagnosis[0])
            self.predictions_results.append(diagnosis[1])
            self.predictions_results.append(diagnosis[2])
        self.create_report()

    def create_report(self):
        print(self.predictions_results)
        id = random.randrange(1, 50)
        # Create a secure SSL context
        context = ssl.create_default_context()
        message = f"""
        Subject: Patient: {self.current_patient.name, id}

        Please see MPXV triage report regarding {self.current_patient.name, id}
        
        Results of MPXV classification model:
        Image Name: {self.predictions_results[0]}
        Predicted Condition: {self.predictions_results[1]}
        Prediction Probability: {self.predictions_results[2]}
        
        Gender: {self.current_patient.gender}
        Age: {self.current_patient.age}
        Height:
        Weight:
        BMI:
        Exercises:
        Smoker:
        
        
        """
        try:
            server = smtplib.SMTP(smtp_server, port)
            server.ehlo()
            server.starttls(context=context)  # Secure the connection
            server.ehlo()
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
            server.quit()
        except Exception as error:
            print(error)