from cv2 import cv2
import time
from ComputerVisionGestures import HandTrackingModule as htm
import numpy as np
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
area = 0
volPer = volume.GetMasterVolumeLevel()
while True:
    success,img = cap.read()
    #FindHand
    img = detector.findHands(img)

    lmList,bbox = detector.findPos(img,draw=True)
    if(len(lmList)!=0):
        #print(lmList[4],lmList[8])
        area= (bbox[2]-bbox[0])*(bbox[3]-bbox[1])//100
        #print(area)

        # Filter based on size done

        if(100 <area<500):
            #print("yes")


            #FIND DIST
            length ,img,lineInfo = detector.findDistance(4,8,img)

            # convert







            volBar = np.interp(length,[22,120],[400,150])
            volPer = np.interp(length,[22,120],[0,100])
            #volume.SetMasterVolumeLevel(int(vol), None)





            smoothness = 10

            fingers = detector.fingersUp()
            print(fingers)

            volPer = smoothness * round(volPer/smoothness)





            # if pinky finger down set volume
            if fingers != None and len(fingers)>3:
                try:
                    if fingers[4] == False:
                        # set volume
                        volume.SetMasterVolumeLevelScalar(volPer / 100, None)
                        cv2.circle(img, (lineInfo[4], lineInfo[5]), 6, (0, 255, 255), cv2.FILLED)
                except:
                    print("Another nasty error")



            if (length < 22 or length > 120):
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 6, (0, 255, 0), cv2.FILLED)


        cv2.rectangle(img,(50,150),(85,400),(0,255,0),5)
        cv2.rectangle(img,(50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)
        cv2.putText(img,f"{int(volPer)} % ",(40,450),cv2.FONT_HERSHEY_PLAIN,2,(255,0,0),2)


    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(10,50),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)
    cv2.imshow("img",img)
    if cv2.waitKey(10)==ord('q'):
        break