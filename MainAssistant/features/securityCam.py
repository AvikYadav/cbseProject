import threading

import cv2
import winsound
import pywhatkit
import pytz
import datetime
import playsound
cam = cv2.VideoCapture(0)
import os

AudioFile = 'Data/Burglar Alarm SOUND EFFECT - Einbruch Einbrecher Alarm SOUNDS.mp3'

if __name__ == '__main__':
    AudioFile = "Burglar Alarm SOUND EFFECT - Einbruch Einbrecher Alarm SOUNDS.mp3"

filename = 'video.avi'
play = False
frames_per_second = 24.0
res = '720p'
write = False
run = True

def alert():
    time1 = pytz.timezone('Europe/London')
    time2 = datetime.datetime.now().strftime('%H:%M')
    print(time2)
    time3 = time2
    time3 = time3.replace(':', '')
    time4 = list(time3)
    print(time4)
    time5 = str(time4.pop(0))
    time5 = time5 + str(time4.pop(-3))
    time6 = str(time4.pop(-2))
    time6 = time6 + str(time4.pop(-1))
    print(time5)
    print(time6)
    time5 = int(time5)
    time6 = int(time6)
    time6 = 1 + time6
    pywhatkit.sendwhatmsg('+919810220510', 'Alert , we have detected some motion on your device',time5,time6 )





def PlayAlarm():
    global play,run
    while run:
        if play == True:
            playsound.playsound(AudioFile)
            play = False

# Standard Video Dimensions Sizes
STD_DIMENSIONS =  {
    "480p": (640, 480),
    "720p": (1280, 720),
    "1080p": (1920, 1080),
    "4k": (3840, 2160),
}

# Function adapted from https://kirr.co/0l6qmh
def change_res(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

# grab resolution dimensions and set video capture to it.
def get_dims(cap, res='1080p'):
    width, height = STD_DIMENSIONS["480p"]
    if res in STD_DIMENSIONS:
        width,height = STD_DIMENSIONS[res]
    ## change the current caputre device
    ## to the resulting resolution
    change_res(cap, width, height)
    return width, height

# Video Encoding, might require additional installs
# Types of Codes: http://www.fourcc.org/codecs.php
VIDEO_TYPE = {
    'avi': cv2.VideoWriter_fourcc(*'XVID'),
    #'mp4': cv2.VideoWriter_fourcc(*'H264'),
    'mp4': cv2.VideoWriter_fourcc(*'XVID'),
}
def get_video_type(filename):
    filename, ext = os.path.splitext(filename)
    if ext in VIDEO_TYPE:
      return  VIDEO_TYPE[ext]
    return VIDEO_TYPE['avi']

out = cv2.VideoWriter(filename, get_video_type(filename), 25, get_dims(cam, res))
x = threading.Thread(target=PlayAlarm)
x.start()

while cam.isOpened():

    ret,frame1 = cam.read()
    ret,frame2 = cam.read()
    diff = cv2.absdiff(frame1,frame2)
    gray = cv2.cvtColor(diff,cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    _, thresh = cv2.threshold(blur,20,255,cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh,None,iterations =3)
    contours,_ = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if write:
        out.write(frame1)
    # cv2.drawContours(frame1,contours,-1,(0,255,0),2)
    for c in contours:
        if cv2.contourArea(c)< 5000:
            continue
        #x,y,w,h = cv2.boundingRect(c)
        #cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        #winsound slows down the program se removed it

        #winsound.Beep(1000,500)
        if(play == False):
            play = True
        write = True
        # alert()
    if cv2.waitKey(10)==ord('q'):
        run = False
        out.release()
        break

    cv2.imshow('security Cam',frame1)


