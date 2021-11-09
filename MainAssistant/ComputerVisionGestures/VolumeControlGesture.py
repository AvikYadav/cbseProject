from cv2 import cv2
import time
import HandTrackingModule as htm
import numpy as np
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


#######################################################
Wcam,hCAm = 800,600
#######################################################


cap = cv2.VideoCapture(0)
cap.set(3,Wcam)
cap.set(4,hCAm)
pTime = 0

detector = htm.handDetector(max_num_hands=1,min_detection_confidence=0.8)




devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))


#volume.GetMute()
#volume.GetMasterVolumeLevel()

volRange = volume.GetVolumeRange()
#volume.SetMasterVolumeLevel(-20.0, None)

minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
while True:
    success,img = cap.read()
    #FindHand
    img = detector.findHands(img)

    lmList,bbox = detector.findPos(img,draw=False)
    if(len(lmList)!=0):
        #print(lmList[4],lmList[8])

        #Filter based on size

        #Find Dist
        x1,y1 = lmList[4][1],lmList[4][2]
        x2,y2 = lmList[8][1],lmList[8][2]

        cx,cy = (x1+x2)//2,(y1+y2)//2

        cv2.circle(img,(x1,y1),3,(255,0,255),cv2.FILLED)
        cv2.circle(img,(x2,y2),3,(255,0,255),cv2.FILLED)
        cv2.line(img,(x1,y1),(x2,y2),(255,0,255),3)
        cv2.circle(img,(cx,cy),3,(255,0,0),cv2.FILLED)


        length = math.hypot(x2-x1,y2-y1)
        #print(length)
        #handrange = 15 - 85
        if(length<15 or length >85):
            cv2.circle(img, (cx, cy), 6, (0, 255, 0), cv2.FILLED)
        vol = np.interp(length,[15,85],[minVol,maxVol])
        print(vol)
        volume.SetMasterVolumeLevel(int(vol), None)
        volBar = np.interp(length,[15,85],[400,150])

    cv2.rectangle(img,(50,150),(85,400),(0,255,0),5)
    cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(10,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("img",img)
    cv2.waitKey(1)