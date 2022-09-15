import tweepy
import smtplib
import ssl
from modules import requests, json, random
from voice_control import VoiceControl

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
