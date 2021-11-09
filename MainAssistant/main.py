import os
from time import sleep
import pyjokes
import gtts
import pyautogui
from playsound import playsound
import pywhatkit
import difflib
import spacy
import json
import speech_recognition as sr
import datetime
import wikipedia
import requests
global paused
paused = False
kill = False
# MainKill = False
months = None
file = None
instructions = None
nlp = None
PID = os.getpid()
# def add_command(text):
    # pass
def search(i):
    pywhatkit.search(i)
    res = wikipedia.summary(i,2)
    print(res)
    speak(res)


def get_tags(text:str):
    if text == False:
        return
    # greetings
    for i in instructions['General']['greetings']["phrases"]:
        #print("in data")
        with open("Data/" + str(i), 'r') as file:
            #print("in ")

            data = file.readlines()
            for j in data:
                #print(text , j)
                doc1 = nlp(str(j).strip())
                doc2 = nlp(text)
                #print(doc1.similarity(doc2))

                if doc1.similarity(doc2) > 0.9:
                 #   print(str(j).strip())
                  #  print(text)
                    print('this is greetings tag')
                    greet()
                    return #'greetings',str(j).strip()



    # personal

    for i in instructions['General']['personal']['phrases']:
        doc1 = nlp(i)
        doc2 = nlp(text)

        if doc1.similarity(doc2) > 0.9:
            print('this is personal tag')
            personal(instructions['General']['personal']['phrases'].index(i))
            return #'personal',instructions['General']['personal']['phrases'].index(i)

#search
    for i in instructions['General']['search']['phrases']:

        if ("is " in text.lower() and "weather" in text.lower()) or ("is" in text.lower() and "time" in text.lower()) or ("is" in text.lower() and" date" in text.lower()):
            break
        if findSimilarity(i,text,findExactWord=True):
            print('this is search tag')
            search(text)
            return #'search',instructions['general']['search']['phrases'].index(i)



#command
    for i in instructions['General']['command']['phrases']:
        if i.find(" "):

            if findSimilarity(i,text,findExactWord=False):
                print('this is command tag')
                commands(text,instructions["General"]['command']['phrases'].index(i))
                print(instructions["General"]['command']['phrases'].index(i))
                return# 'command',instructions["General"]['command']['phrases'].index(i)
        else:
            if findSimilarity(i,text,findExactWord=True):
                print('this is command tag')
                commands(text,instructions["General"]['command']['phrases'].index(i))
                print(instructions["General"]['command']['phrases'].index(i))
                return# 'command',instructions["General"]['command']['phrases'].index(i)

        # feedback
    for i in instructions['General']['feedback']['phrases']:
        if i in text:
            print('this is feedback tag')
            feedback()
            return #'feedback',instructions['General']['feedback']['phrases'].index(i)
    print("other")
    speak("could not get that in a moment")
    return #'other',None



def findSimilarity(word:str,phrase:str , findExactWord = False):
    try:
        list2 = phrase.split(" ")
    except:
        list2 = [phrase]
    for i in list2:
        if(findExactWord == False):
            print(i)
            print(word)
            print()
            if i in word:
                return True
        else:
            if word.lower() in i.lower() or word.lower() in phrase.lower():
                return True
    return False
    # print(similar)
    # print(list1)
    # print(list2)
    # falseNo = 0
    # trueNo = 0
    # for i in similar:
    #     if i:
    #         trueNo+=1
    #     else:
    #         falseNo+=1
    # if(trueNo > falseNo or trueNo == falseNo):
    #     return True
    # else:
    #     return False


def similarWords(text):
    difference = difflib.get_close_matches(text, instructions['websites'])
    return difference[0]
def greet():
    speak(instructions['General']['greetings']['responses'][-1])


def type():
    speak('you may start speaking now')
    speak('enter for how long would you like to type')
    from MainAssistant.features import getAudiotoSpeech

    with open('Data/TypeData.txt','r') as file:
        data = file.readlines()
    speak('starting typing be ready')
    sleep(2)
    for i in data:
        pyautogui.write(i,interval=0.01)
# def about(tag,command):
#     if tag == 'about':
#         print('running about')
#         if 'i' in command:
#             command = command.replace('i', '')
#         if 'my' in command:
#             command = command.replace('my', '')
#         with open('userData.txt', 'a') as file2:
#             print(command,file = file2)
#             # file2.write(command)
#         speak(instructions['about']['responses'][-1])
def personal(index):
    speak(instructions['General']['personal']['responses'][index])

def feedback():
        speak(instructions['General']['feedback']['responses'][-1])

def commands(command,ind):
    # print('reach command')
    if instructions['General']['command']['phrases'][ind] == 'time':
        # print('now getting time')
        now = datetime.datetime.now()
        hour = now.strftime('%H')
        min = now.strftime('%M')
        # amOrPm = 'am'
        # if int(hour)>12:
        #     amOrPm = 'pm'
        speak(f'the time is {hour} hour {min} min')
    # if instructions['command']['phrases'][ind] == "open website":
    #     path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
    #     command = command.replace("open website", '')
    #     # if 'amazon' in command:
    #     #     speak('which region would you like to open amazon in . india or foregin')
    #     #     command2 = microphone()
    #     #     command2 = difflib.get_close_matches(command2,['india', 'foregin'])
    #     #     if 'india' in command:
    #     #         web.get(path).open('amazon.in')
    #     #     else:
    #     #         web.get(path).open('amazon.com')
    #     if not ".com" in command:
    #         command = command + '.com'
    #         command = similarWords(command)
    #         for i in instructions['websites']:
    #             if command in i:
    #                 web.get(path).open(command)15

    elif instructions['General']['command']['phrases'][ind] == 'typing type':
        type()
    elif instructions['General']['command']['phrases'][ind] == 'open':
        openApp(command)
        speak("opening app")
    elif instructions['General']['command']['phrases'][ind] == 'date':
        now = datetime.datetime.now()
        year = now.strftime('%Y')
        month = now.strftime('%m')
        date = now.strftime('%d')
        speak(f"today's date is: {date},{months[int(month)]},{year}")
    elif instructions['General']['command']['phrases'][ind] == 'weather':
        # Google Open weather website
        # to get API of Open weather
        api_key = "38ea72126cd228fa8ffcfe3f395f863a"
        base_url = "http://api.openweathermap.org/data/2.5/forecast?"
        speak(" City name ")
        print("City name : ")
        city_name = microphone()
        complete_url = base_url + "q=" + city_name + "&appid=" + api_key
        response = requests.get(complete_url)
        print(complete_url)

        if response.status_code == 200:
            # getting data in the json format
            data = response.json()
            print(data)
            # getting the main dict block
            main = data['list'][0].get('main')
            # getting temperature
            temperature = main['temp']
            # getting the humidity
            humidity = main['humidity']
            # getting the pressure
            pressure = main['pressure']
            # weather report
            report = data['list'][0].get('weather')
            print(main,'\n',temperature,'\n',humidity,'\n',pressure,'\n',report)
            print(f"{city_name:-^30}")
            print(f"Temperature: {temperature}")
            print(f"Humidity: {humidity}")
            print(f"Pressure: {pressure}")
            print(f"Weather Report: {report[0]['description']}")
            speak(f" weather report of {city_name:-^30} is")

            speak(f"Humidity is {humidity}")
            speak(f"Pressure is {pressure}")
            speak(f"Weather Report is {report[0]['description']}")
        else:
            # showing the error message
            print("Error in the HTTP request")
            speak("Could not get that in a moment , please try again later")

    elif instructions['General']['command']['phrases'][ind] == 'joke':
        # pywhatkit.search(command)
        speak(pyjokes.get_joke())
    # elif instructions['command']['phrases'][ind] == 'how':
    #     command = command.replace('how', '')
    #     how = pywhatkit.search(command)
    #     speak(how)
    elif instructions['General']['command']['phrases'][ind] == 'play':
        command = command.replace('play','')
        pywhatkit.playonyt(command)
        speak("Playing")
    elif instructions['General']['command']['phrases'][ind] == 'directory':
        from MainAssistant.features import DirectorySorter
        DirectorySorter.Main()
    elif instructions['General']['command']['phrases'][ind] == 'computer vision':
        speak('features available are')
        for i in instructions['General']['computerVision']:
            speak(i)
        speak("Which feature you want to start")
        command = microphone()
        if instructions['General']['computerVision'][0] in command:
            from MainAssistant.features import securityCam
        elif instructions['General']['computerVision'][1] in command:
            from ComputerVisionGestures import VolumeHandControlImproved
        elif instructions['General']['computerVision'][2] in str(command).lower():
            from ComputerVisionVirtualMouse import VirtualMouse
        # elif instructions['General']['computerVision'][3] in str(command).lower():
        #     from doucument import main
        elif instructions['General']['computerVision'][3] in str(command).lower():
            from computervisionfaceRecoginition import FaceRecoginitationAttendence
        # elif instructions['General']['computerVision'][3] in str(command).lower():
        #     from doucument import main

        else:
            speak("could not get that in a moment , try again later")

def openApp(command):
    pyautogui.press('win')
    sleep(.5)
    command = command.replace('open', '')
    pyautogui.write(command, interval=0.05)
    sleep(.5)
    pyautogui.press('enter')

def Main():
#    speak(instructions['greetings']['responses'][-1])
    command = microphone()
    # command = "tell me a joke"
    if command == False:
        return
    global paused
    get_tags(command)
    paused = False


def speak(text):
    tts = gtts.gTTS(text=text, lang='en')
    tts.save("record.mp3")
    # print("Audio Recorded Successfully \n ")
    playsound('record.mp3')
    os.remove('record.mp3')
    #print(text)

def microphone():
    # print(sr.Microphone.list_microphone_names())
    r = sr.Recognizer()
    global paused
    paused = True
    # try:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source,duration=0.2)
        speak("listening now")
        print("listening.....")
        audio = r.listen(source,phrase_time_limit=10)
        print("Recognizing Now .... ")
        speak("Processing")
        text = r.recognize_google(audio)
        #print("Text Converted Successfully ")
        print(text)
            # print("You have said \n" +text)

        return text
    # except Exception as e:
    #     print("Error :  " + str(e))
    #     #speak("coudn't get that in the moment please try again later")
    #     return False

# def InstantKill():
#     # while True:
#     #     print(MainKill)
#     #     if MainKill:
#             exit()
#         # sleep(1)

def Initialization():
    global nlp,file,instructions,months
    nlp = spacy.load("en_core_web_md")
    file = open('Data/instructions.json', )
    instructions = json.load(file)
    months = [0, 'january', 'February', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
              'november', 'december']
    print(instructions)
    #####################################################
    Main()
    # x = threading.Thread(InstantKill())
    # x.start()



if __name__ == '__main__':
    #####################################################
    #  initialization #
    Initialization()




