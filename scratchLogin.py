def face_login():
    speech.speak('what is your username')
    name = speech.receive_command().lower()
    try:
        # instantiate med bot with new patient -> confirm face recognition matches username -> set patient name
        # to username -> start conversation function
        bot = MedBot(patient)
        if bot.login_recognition(name):
            usb.write(b'alert_off')
            patient.name = name
            speech.speak(f'logged in as {patient.name}')
            bot.conversation()
    except FileNotFoundError as error:
        print(error)


def create_account():
    patient_details_response = []
    patient_account_questions = ['name', 'gender', 'birth year', 'height in centimetres', 'weight in kilos',
                                 'do you exercise', 'do you smoke']
    try:
        for item in patient_account_questions:
            speech.speak(f'{item}')
            response = speech.receive_command()
            if item == 'name':
                patient_details_response.append(response.lower())
            elif item == 'gender':
                patient_details_response.append(patient.check_gender(response))
            elif item == 'birth year':
                patient_details_response.append(int(response))
            elif item in ['height in centimetres', 'weight in kilos']:
                patient_details_response.append(float(response))
            elif item in ['do you exercise', 'do you smoke']:
                patient_details_response.append(speech.return_confirmation_binary(response))
        # update database with new patient
        db.create_patient('patients', patient_details_response[0], patient_details_response[1],
                          patient_details_response[2], patient_details_response[3], patient_details_response[4],
                          patient_details_response[5], patient_details_response[6])
        # take image for facial recognition login
        image.take_face_photo(patient_details_response[0])
    except ValueError as error:
        speech.speak('incorrect answer format, please start again')
        print(error)

    db.get_all_table_data('patients')



