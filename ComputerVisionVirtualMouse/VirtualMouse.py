from cv2 import cv2
import numpy as np
from ComputerVisionGestures import HandTrackingModule as htm
import time
import autopy
import pyautogui
width,height = 640,480
cap = cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)
ptime = 0
plocx,plocy = 0,0
clocx,clocy = 0,0


detector = htm.handDetector(max_num_hands=1)
WScreen,HScreen = autopy.screen.size()


smoothening = 7
print(WScreen,HScreen)


frameReduction = 100
while True:

    success,img = cap.read()

    img = detector.findHands(img)
    lmlist,bbox = detector.findPos(img)


    if len(lmlist)!=0:
        x1,y1 = lmlist[8][1:]
        x2,y2 = lmlist[12][1:]

        # print(x1,y1,x2,y2)

        fingers = detector.fingersUp()
        if fingers != None:

            if fingers[1] == 1 and fingers[2] == 0:


                x3 = np.interp(x1,(frameReduction,width-frameReduction),(0,WScreen))
                y3 = np.interp(y1,(frameReduction,height-frameReduction),(0,HScreen))

                clocx = plocx+(x3-plocx)/smoothening
                clocy = plocy+(y3-plocy)/smoothening

                try:
                    autopy.mouse.move(WScreen-clocx,clocy)
                except Exception as e:
                    print(e)
                cv2.circle(img,(x1,y1),5,(0,255,255),cv2.FILLED)
                plocx,plocy = clocx,clocy
            if fingers[1] == 1 and fingers[2] == 1:
                length,img,info = detector.findDistance(8,12,img)
                print(length)#less tha 18 then a click
                if length < 18:
                    cv2.circle(img, (info[4], info[5]), 5, (255, 255, 0), cv2.FILLED)
                    autopy.mouse.click()

            if fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1:
                pyautogui.click(button='right')
                time.sleep(.25)

    #fps
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime


    #output
    cv2.rectangle(img, (frameReduction, frameReduction), (width - frameReduction, height - frameReduction),
                  (255, 0, 255), 2)

    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,2,(0,0,0),2)
    cv2.imshow("image",img)
    cv2.waitKey(1)