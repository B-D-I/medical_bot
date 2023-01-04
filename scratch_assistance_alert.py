import tweepy
import smtplib
import ssl
from modules import requests, json, random, usb
from device_voice_control import VoiceControl
from credentialsOLD import *

speech = VoiceControl()


class AssistanceAlert:
    """
    This class is used to provide emergency alerts to patient next of kin, via Twitter, Alexa and Email.
    The device will also set off a short alarm. (credentials stored in credentials file)
    """

    def send_all_alerts(self):
        speech.speak('are you sure you wish to send alerts? ')
        response = speech.receive_command().lower()
        if response in speech.confirmation:
            self.alexa_alert(access_code_alexa)
            self.twitter_alert(api_key, api_secret, access_token, access_token_secret)
            # self.email_alert(smtp_server, port, sender_email, receiver_email, password)
            speech.speak('alerts have been sent')
            usb.write(b'alert')
            print('alerts sent')
        else:
            speech.speak('alerts have not been sent')

    @staticmethod
    def alexa_alert(alexa_access_code: str):
        """
        When called will send an alexa notification to the notifymyecho API. Access token included in credentials.
        """
        alexa_body = json.dumps({
            "notification": f"Alert",
            "accessCode": f"{alexa_access_code}"
        })
        # Post the notification to API
        requests.post(url="https://api.notifymyecho.com/v1/NotifyMe", data=alexa_body)

    @staticmethod
    def twitter_alert(key: str, secret: str, token: str, token_secret: str):
        auth = tweepy.OAuthHandler(key, secret)
        auth.set_access_token(token, token_secret)
        api = tweepy.API(auth)

        random_id = random.randint(1, 1000)
        api.update_status(status=f"Alert Tweet: {random_id}")

    @staticmethod
    def email_alert(server: str, port_num: int, send_email: str, rec_email: str, passwd: str):
        # Create a secure SSL context
        context = ssl.create_default_context()
        message = f"""
        Subject: This is an alert email from med bot

        This is an alert email from med bot
        """
        try:
            server = smtplib.SMTP(server, port_num)
            server.ehlo()
            server.starttls(context=context)  # Secure the connection
            server.ehlo()
            server.login(send_email, passwd)
            server.sendmail(send_email, rec_email, message)
            server.quit()
        except Exception as error:
            print(error)
