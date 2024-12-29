# Filename: pb_speak.py

import pyttsx3

class pbSpeak:
    def __init__(self, name="Agent", rate=170, voice_index=1):
        """
        Initialize the pbSpeak with a custom name, speaking rate, and voice.

        :param name: The name to display when speaking (default is "Agent").
        :param rate: Speech rate (default is 170).
        :param voice_index: Index of the voice (default is 1 for female voice).
        """
        self.name = name
        self.engine = pyttsx3.init('sapi5')
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[voice_index].id)
        self.engine.setProperty('rate', rate)

    def speak(self, text):
        """
        Speak the given text using pyttsx3 and print the name.

        :param text: The text to speak.
        """
        print('')
        print(f'{self.name}: {text}')
        print('') 
        self.engine.say(text)
        self.engine.runAndWait()
