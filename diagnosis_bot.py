import os
import random
import smtplib, ssl
from credentials import smtp_server, sender_email, receiver_email, app_passwd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from device_voice_control import VoiceControl
from image_classifier import ImageClassifier
speech = VoiceControl()
classifier = ImageClassifier()


class DiagnosisBot:
    def __init__(self, current_patient, camera):
        self.current_patient = current_patient
        self.patient_id = random.randrange(1, 50)
        self.camera = camera
        self.predictions_results = []

    def start_diagnosis(self, image_type: str):
        speech.speak('image will be taken in 10 seconds')
        self.camera.take_image(1, image_type)
        image_path = f'images/{image_type}_images/'
        for filename in os.listdir(image_path):
            diagnosis = classifier.prediction(image_path, image_type, filename)
            self.predictions_results.append(diagnosis[0])
            self.predictions_results.append(diagnosis[1])
            self.predictions_results.append(diagnosis[2])
        self.send_report()

    def send_report(self):
        msg = MIMEMultipart('related')
        msg['Subject'] = f'Triage Report: Patient {self.patient_id}'
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg.preamble = 'This is a multi-part message in MIME format.'

        msg_alt = MIMEMultipart('alternative')
        msg.attach(msg_alt)
        msg_text = MIMEText(f'''
        MPXV Image Classification Triage Report
        <br><br>Patient: {self.current_patient.name}, id:{self.patient_id} 
        <br>Triage level:
        <br>Image: {self.predictions_results[0]}
        <br>Predicted Condition: {self.predictions_results[1]}
        <br>Prediction Probability: {self.predictions_results[2]}
        <br>
        <br>Gender: {self.current_patient.gender}
        <br>Age: {self.current_patient.age}
        <br>BMI: {self.current_patient.body_mass}  ({self.current_patient.bmi})
        <br>Exercises: {self.current_patient.is_exercise}
        <br>Smoker: {self.current_patient.is_smoker}
        
        <br><br> <img src="cid:image1">
        ''', 'html')
        msg_alt.attach(msg_text)

        fp = open('images/MPXV_images/MPXV1.jpg', 'rb')
        msg_image = MIMEImage(fp.read())
        fp.close()

        msg_image.add_header('Content-ID', '<image1>')
        msg.attach(msg_image)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, 465, context=context) as server:
            server.login(sender_email, app_passwd)
            server.sendmail(
                sender_email, receiver_email, msg.as_string()
            )
