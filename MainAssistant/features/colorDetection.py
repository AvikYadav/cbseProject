import cv2
from time import sleep
cap = cv2.VideoCapture(0)
import numpy as np
lower_blue = np.array([110,50,50])
upper_blue = np.array([130,255,255])
prev_y = 0

while True:
    ret,frame = cap.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,lower_blue,upper_blue)
    contors,hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for c in contors:
        area = cv2.contourArea(c)
        if area > 500:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            print(y)
            diff = prev_y - y
            if prev_y < y and diff < 1000:
                sleep(0)
            prev_y = y

    cv2.imshow("frame",frame)
    cv2.imshow('mask',mask)

    if cv2.waitKey(10) == ord('q'):
        break

cap.release()