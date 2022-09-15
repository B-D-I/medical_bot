from function_list import *
from modules import json, random

"""
Application info

Created:
Updated:
"""
__author__ = "Nathan"
__status__ = "Planning"


# CREATE LOGIN -> PATIENT.NAME = 'USERNAME'
# INCLUDE CNN MODEL AND CLASSIFY (HASH CHECK)
# DIAGNOSIS API
# MULTI THREAD: STOP TALKING COMMAND
# UNIT TESTING - MORE


def conversation():
    """
       This function opens the 'chat_conv' json file, and listens to voice commands from the user.
       If a query is recognised from the input array in the json file, an output from the relevant
       output list will be randomly selected, and spoken. If the input query has a function allocated,
       these will be included in the 'func_dict' dictionary, and called if queried, using the 'call_func'
       function. This 'conversation' function also listens for the keyword 'tell me about', which initiates
       the 'search()' function, with the query as a parameter.
    """
    with open("chat_conv.json", "r") as chat_file:
        chat_dict = json.load(chat_file)
    while True:
        query = speech.receive_command()
        if "tell me about" in query:
            search(query)
        for i in chat_dict["conversation"]:         # for items in dict
            if query in i['inputs']:                # if query found
                if i['outputs'] != "":
                    speech.speak(random.choice(i['outputs']), f'{patient.name}')   # speak the outputs + name
                    func = i['conv_name']
                    call_func(func)
                    continue


# functions dictionary to be called
func_dict = {
    "time": tell_time,
    "date": tell_day,
    "alert": send_all_alerts,
    "bmi": get_bmi,
    "heart_rate": get_heart_rate,
    "start_camera": start_camera,
    "update_weight": update_weight,
    "diagnosis": start_diagnosis
}


def call_func(func):    # parameter given from conversation func
    for key in func_dict:       # if the key is same as func query, call function
        if func == key:
            func_dict[key]()


def start():
    usb.write(b'alert_off')
    speech.speak(f'hello {patient.name}')
    conversation()


if __name__ == "__main__":
    start()












