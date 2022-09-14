from modules import datetime
from voice_control import VoiceControl
from emergency_alert import EmergencyAlert
import wikipedia
import wikipedia.exceptions

speech = VoiceControl()
alerts = EmergencyAlert('nathan')


class MedBot:

    @staticmethod
    def tell_day():
        day = datetime.datetime.today().weekday() + 1
        month = datetime.datetime.today().month
        year = datetime.datetime.today().year
        date = datetime.datetime.today().day
        day_of_week = ''
        day_dict = {1: 'Monday', 2: 'Tuesday',
                    3: 'Wednesday', 4: 'Thursday',
                    5: 'Friday', 6: 'Saturday',
                    7: 'Sunday'}
        month_dict = {1: 'January', 2: 'February', 3: 'March',
                      4: 'April', 5: 'May', 6: 'June',
                      7: 'July', 8: 'August', 9: 'September',
                      10: 'October', 11: 'November', 12: 'December'}

        if day in day_dict.keys():
            day_of_week = day_dict[day]
        if month in month_dict.keys():
            month_of_year = month_dict[month]
            speech.speak("Today is " + day_of_week, date, month_of_year, year)

    @staticmethod
    def tell_time():
        # Place the string format of time into time variable
        time = str(datetime.datetime.now())
        # sliced for specific values
        time_hour = time[11:13]
        time_min = time[14:16]
        speech.speak("The time is" + time_hour + "Hours and" + time_min + "Minutes")

    @staticmethod
    def search(query):
        """
        When called will use the Wikipedia module to carry out a search of user's query. The 'tell me about' keyword is
        removed, to ensure only the relevant query is searched. The information will then be outputted, unless there query
        is too unambiguous, in which case the user will be told to rectify the command.
        :param query: This is imported from the conversation() function, and contains the string format of
        the user's spoken query.
        :return: The required information will be outputted, or user will be notified to be more specific.
        """
        # Remove the query command, and search user input
        query = query.replace("tell me about", "")
        # while True:
        try:
            # place the result into a variable. confirm amount of sentences spoken
            result = wikipedia.summary(query, sentences=3)
            speech.speak(result)
        # This exception is used if the user searches an unambiguous or too broad a query
        except wikipedia.exceptions.DisambiguationError as error:
            print(error)
            speech.speak(
                f"sorry, that query is too broad, could you try again and re-phrase what you would like to "
                f"search")
            # finally:
            #     break

    # would you like to hear more?
    # # an attempt to listen for a 'stop' during speak. not work
    # while True:
    #     listen = takeCommand().lower()
    #     if 'stop' in listen:
    #         break
    #     speak(result)   # need a 'would like to continue?' option.. or way to break

# def alert():
#     """
#     When called, will confirm if alert(s) are to go ahead. If so, Twitter access tokens and information are taken from
#     credentials. To ensure a tweet has a unique code, the random.randint method is used. A tweet will be posted, along
#     with an email and Alexa notification to the specified locations. Also, the Arduino 'alert' function will be called
#     initiating an alarm.
#     :return: twitter, email, alexa, arduino alerts
#     """
#     while True:
#         # try / except
#         speech.speak('are you sure you wish to send an alert? ')
#         response = speech.receive_command().lower()
#         if response in speech.confirmation:
#             alerts.alexa_alert(access_code_alexa)
#             alerts.twitter_alert(api_key, api_secret, access_token, access_token_secret)
#             alerts.email_alert(smtp_server, port, sender_email, receiver_email, password)
#             speech.speak("alerts have been sent")
#             usb.write(b'alert')
#             print('alerts sent')
#             break
#         else:
#             speech.speak('alerts have not been sent')
#             break


# med = MedBot()
# med.tell_time()
# med.tell_day()