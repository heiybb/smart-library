#!/usr/bin/env python3

# Reference: https://pypi.org/project/SpeechRecognition/
# Reference: https://www.geeksforgeeks.org/speech-recognition-in-python-using-google-speech-api/
# Note this example requires PyAudio because it uses the Microphone class

"""
Speech to text Module
Capture the voice input and convert it to text
using the google speech-to-text api
"""

import speech_recognition as sr
import subprocess


class VoiceRecognise:
    """
    Provide the interface for the voice recognise
    using the Google-Speech-Text API
    """

    @staticmethod
    def recognise():
        """
        Convert the voice input to text and return it
        :return: str text
        """
        global device_id
        mic_name = "Microsoft® LifeCam HD-3000: USB Audio (hw:1,0)"
        # Set the device ID of the mic that we specifically want to use to avoid ambiguity
        for i, microphone_name in enumerate(sr.Microphone.list_microphone_names()):
            if microphone_name == mic_name:
                device_id = i
                break

        # obtain audio from the microphone
        recognizer = sr.Recognizer()
        print(device_id)
        with sr.Microphone(device_index=device_id) as source:
            # clear console of errors
            subprocess.run("clear")

            # wait for a second to let the recognizer adjust the
            # energy threshold based on the surrounding noise level
            recognizer.adjust_for_ambient_noise(source)

            print("Say something!")
            try:
                audio = recognizer.listen(source, timeout=1.5)
            except sr.WaitTimeoutError:
                print("Listening timed out whilst waiting for phrase to start")
                quit()

        # recognize speech using Google Speech Recognition
        try:
            # for testing purposes, just using the default API key
            c_text = recognizer.recognize_google(audio)
            print("Google Speech Recognition thinks you said '{}'".format(c_text))
            return c_text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return None
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
            return None


if __name__ == "__main__":
    VR = VoiceRecognise
    VR.recognise()
