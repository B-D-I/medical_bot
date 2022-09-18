from function_list import *

"""
Medical Bot: Home Diagnosis Device


"""
__author__ = "Nathan Hewett"


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


def call_func(func):    # parameter given from conversation func
    for key in func_dict:       # if the key is same as func query, call function
        if func == key:
            func_dict[key]()


def start():
    usb.write(b'alert_off')
    speech.speak(f'hello {patient.name}')
    conversation()


def face_login():
    if image.facial_recognition(patient.name):
        speech.speak(f'logged in as {patient.name}')
        start()


def diagnose_respond(is_initial: bool):
    """
    This recursive function uses the Diagnosis object and Infermedica API to perform real time diagnoses. The user provides
    evidence to be assessed. If a condition is determined at over 70%, it will be given to the user
    :param is_initial: Is the function being called for the first time
    :return: Function will be called recursively until a diagnosis of over 70%is made
    """
    if is_initial:
        diagnose.evidence.clear()
        symptom_id = confirm_symptom()
        diagnose.evidence.append({'id': f'{symptom_id}', 'choice_id': 'present', 'source': 'initial'})
    d = diagnose.diagnosis(diagnose.evidence, patient.get_age(), patient.gender)
    try:
        print(d['question']['text'])
        for condition in d['conditions']:
            if condition['probability'] > 0.7:
                probability = "{:.2f}".format(condition["probability"])
                speech.speak(f'based on these answers it is believed you have '
                             f'{condition["common_name"]}, with a probability of {probability} percent')
                conversation()
            else:
                speech.speak(d['question']['text'])
                if d['question']['text'] is not None:
                    for item in d['question']['items']:
                        try:
                            speech.speak(item['name'])
                            id = item['id']
                            response = speech.receive_command()
                            choice = diagnose.return_choice(response)
                            diagnose.evidence.append({'id': id, 'choice_id': choice})
                            diagnose_respond(False)
                        except infermedica_api.exceptions.BadRequest as err:
                            print(err)
                            continue
    except TypeError as error:
        print(error)


def diagnosis():
    diagnose_respond(True)


# functions dictionary to be called during coversation
func_dict = {
    "time": tell_time,
    "date": tell_day,
    "alert": send_all_alerts,
    "bmi": get_bmi,
    "heart_rate": get_heart_rate,
    "take_skin_photo": take_skin_photo,
    "take_face_photo": take_face_photo,
    "update_weight": update_weight,
    "diagnosis": diagnosis
}


if __name__ == "__main__":
    while True:
        if speech.receive_command() == 'log in':
            speech.speak('to login, face the camera for facial recognition')
            face_login()












