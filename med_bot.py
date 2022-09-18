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
        # Place the string format of time into time variable -> then sliced for specific values
        time = str(datetime.datetime.now())
        time_hour = time[11:13]
        time_min = time[14:16]
        speech.speak("The time is" + time_hour + "Hours and" + time_min + "Minutes")

    @staticmethod
    def search(query, is_test: bool):
        """
        When called will use the Wikipedia module to carry out a search of user's query. The 'tell me about' keyword is
        removed, to ensure only the relevant query is searched. The information will then be outputted, unless there query
        is too unambiguous, in which case the user will be told to rectify the command.
        :param is_test: whether function is being called for unit testing
        :param query: This is imported from the conversation() function, and contains the string format of
        the user's spoken query.
        :return: The required information will be outputted, or user will be notified to be more specific.
        """
        # Remove the query command, and search user input
        query = query.replace("tell me about", "")
        try:
            # place the result into a variable. confirm amount of sentences spoken
            result = wikipedia.summary(query, sentences=3)
            if not is_test:
                speech.speak(result)
            else:
                print(result)
        # This exception is used if the user searches an unambiguous or too broad a query
        except wikipedia.exceptions.DisambiguationError as error:
            if not is_test:
                print(error)
                speech.speak(
                    f"sorry, that query is too broad, could you try again and re-phrase what you would like to "
                    f"search")
            else:
                print(error)

