import tweepy
import smtplib
import ssl
from modules import requests, json, random, usb
from voice_control import VoiceControl
from credentials import *

speech = VoiceControl()


class EmergencyAlert:

    def __init__(self, user):
        self.user = user

    def alexa_alert(self, alexa_access_code: str):
        """
        When called will send an alexa notification to the notifymyecho API. Access token included in credentials.
        """
        alexa_body = json.dumps({
            "notification": f"Alert for {self.user}",
            "accessCode": f"{alexa_access_code}"
        })
        # Post the notification to API
        requests.post(url="https://api.notifymyecho.com/v1/NotifyMe", data=alexa_body)

    def twitter_alert(self, key: str, secret: str, token: str, token_secret: str):
        auth = tweepy.OAuthHandler(key, secret)
        auth.set_access_token(token, token_secret)
        api = tweepy.API(auth)

        random_id = random.randint(1, 1000)
        api.update_status(status=f"Alert Tweet {self.user}: {random_id}")

    def email_alert(self, server: str, port_num: int, send_email: str, rec_email: str, passwd: str):
        # Create a secure SSL context
        context = ssl.create_default_context()
        message = f"""
        Subject: This is an alert email for {self.user} from med bot

        This is an alert email for {self.user} from med bot
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
            # speak("alert email not sent, please check login credentials and smtp configurations")

    # def send_all_alerts(self):
    #     """
    #     When called, will confirm if alert(s) are to go ahead. If so, Twitter access tokens and information are taken from
    #     credentials. To ensure a tweet has a unique code, the random.randint method is used. A tweet will be posted, along
    #     with an email and Alexa notification to the specified locations. Also, the Arduino 'alert' function will be called
    #     initiating an alarm.
    #     :return: twitter, email, alexa, arduino alerts
    #     """
    #     # while True:
    #     speech.speak('are you sure you wish to send alerts? ')
    #     response = speech.receive_command().lower()
    #     if response in speech.confirmation:
    #         self.alexa_alert(access_code_alexa)
    #         self.twitter_alert(api_key, api_secret, access_token, access_token_secret)
    #         # self.email_alert(smtp_server, port, sender_email, receiver_email, password)
    #         speech.speak("alerts have been sent")
    #         usb.write(b'alert')
    #         print('alerts sent')
    #         # break
    #     else:
    #         speech.speak('alerts have not been sent')
    #         # break


# alerts = EmergencyAlert('Tester')
# alerts.send_all_alerts()
# alerts.alexa_alert(access_code)
# alerts.twitter_alert(api_key, api_secret, access_token, access_token_secret)
# alerts.email_alert(smtp_server, port, sender_email, receiver_email, password)