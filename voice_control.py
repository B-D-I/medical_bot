import pyttsx3
import speech_recognition as sr
import pyaudio


class VoiceControl:

    def __init__(self):
        self.mic = sr.Microphone()
        self.r = sr.Recognizer()
        self.confirmation = ("yes", "yeah", "yes please", "confirm", "please")
        self.negative = ("no", "nope", "negative", "no thanks", "no thank you", "quit", "stop", "cancel", "abort", "abandon")
        self.over = ("overweight", "severely overweight", "obese")
        self.unsure = ("unsure", "don't know", "do not know", "pass", "unknown", )

    def receive_command(self):
        """
        The Microphone module within the speech recognition module will listen for a command, if a command is recognised
        it will be printed and returned. If the command is unrecognised, this will be printed to prompt.
        Likewise with a request error.
        :return: The recognised command will be returned as 'query'
        """
        with self.mic as source:
            print("Awaiting Command")
            # Amount of seconds of non-speaking audio until a phrase / sentence considered complete
            self.r.pause_threshold = 0.6
            audio = self.r.listen(source)
            # Adjustments for ambient noise
            self.r.adjust_for_ambient_noise(source)  #
            try:
                print("...")
                # Language set to English
                query = self.r.recognize_google(audio, language='en')
                print("command: ", query)
            except sr.UnknownValueError or sr.RequestError as error:
                print(error)
                print("Not Recognised")
                return "None"
            return query

    @staticmethod
    def speak(*audio):
        """
        Text to speech conversion using pyttsx3. Speech rate, volume and voice properties have been set. There has been a
        slight adjustment to the instructions from the pyttsx3 documentation, due to the installation of the module on
        Raspberry Pi, Debian operating system. the parameter for voices[] would usually be 0 for male, or 1 for female,
        however these parameters convert to a foreign language. Therefore voices[10] has been used for English translation.
        :param audio: provided text
        :return: text converted to audio
        """
        engine = pyttsx3.init()
        # rate properties
        rate = engine.getProperty("rate")
        engine.setProperty('rate', 2.0)
        # volume & voice properties
        volume = engine.getProperty("volume")
        engine.setProperty(volume, 1.0)
        voices = engine.getProperty("voices")
        for voice in voices:
            engine.setProperty("voice", voices[10].id)
        # Enable the script to speak the audio
        engine.say(audio)
        # Blocks while processing all currently queued commands
        engine.runAndWait()
