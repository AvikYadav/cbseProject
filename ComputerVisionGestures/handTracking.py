from cv2 import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

ptime = 0
cTime = 0

while True:
    sucess,img = cap.read()

    imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    #print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handlms in results.multi_hand_landmarks:

            for id,landmark in enumerate(handlms.landmark):
                #print((id,landmark))
                height,width,channel = img.shape
                cx,cy = int(landmark.x*width),int(landmark.y*height)
                #print(id,cx,cy)
                if id ==0:
                    cv2.circle(img,(cx,cy),15,(255,0,255),cv2.FILLED)


            mpDraw.draw_landmarks(img,handlms,mpHands.HAND_CONNECTIONS)



    cTime = time.time()
    fps = 1/(cTime-ptime)
    ptime = cTime

    cv2.putText(img,str(int(fps)),(10,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,255),3)

    cv2.imshow("Image",img)
    cv2.waitKey(1)