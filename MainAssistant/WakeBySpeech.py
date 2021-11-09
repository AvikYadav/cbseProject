import speech_recognition as sr
import threading
from MainAssistant import main
import sys

def Wake(wakeWord : str):
    while True:
        print(main.paused)
        if main.kill:
            x.stop()
            sys.exit("Kill Executed")
        if main.paused:

            continue

        text = microphone()
        if wakeWord.lower() in text.lower():
            main.Initialization()
        if wakeWord.lower() == "shut up":
            main.MainKill = True


def microphone():
    # print(sr.Microphone.list_microphone_names())
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source,duration=0.2)
            audio = r.listen(source,phrase_time_limit=1)

            text = r.recognize_google(audio)
            print(text)
            return text
    except Exception as e:
        print("Error :  " + str(e))
        return ""

x = threading.Thread(target=Wake ,args=("Computer",))
x.start()