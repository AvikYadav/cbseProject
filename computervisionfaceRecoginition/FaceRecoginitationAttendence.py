from datetime import datetime
import time

from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

import numpy as np
import face_recognition
from cv2 import cv2
import os
import keyboard
"""initialization to save files to google drive

gauth = GoogleAuth()

# Creates local webserver and auto
# handles authentication.
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)
"""
#init cv2
video_capture = cv2.VideoCapture(0)
cascPath=os.path.dirname(cv2.__file__)+"/data/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
#getting images from folder
path = 'Data/imagesSaveFolder'
if __name__ == '__main__':
    path = 'imagesSaveFolder'
imagesName = []
myList = os.listdir(path)
print(myList)
images = []





# this fuction works to save files in google drive , it needs authencation detalis in a json file which you get get through google https://console.developers.google.com/
# i am not implementing this as i don't want to give my personal credentials here sane function applies for security cam
'''
def saveFileToDrive():
    for x in os.listdir(path):
        f = drive.CreateFile({'people used computer today': x})
        f.SetContentFile(os.path.join(path, x))
        f.Upload()

        f = None
'''

for img in myList:
    os.remove(path+f"/{img}")


print(imagesName)
area = -500


def findEncodeings(images):
    encodeList = []
    try:
        for i in images:
            i = cv2.cvtColor(i,cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(i)[0]
            encodeList.append(encode)
        return encodeList
    except Exception as e:
        print("Execption at finding face encodings" , e)
        return False

# find face encoding to compare with faces present in cam frame
cap = cv2.VideoCapture(0)
#running loop for webcam
while True:
    sucess,img = cap.read()
    dupe = img
    myList = os.listdir(path)
    images = []

    for imge in myList:
        if len(myList)==0:
            break
        curImg = cv2.imread(f'{path}/{imge}')
        curImg = face_recognition.load_image_file(f'{path}/{imge}')
        images.append(curImg)
        imagesName.append(os.path.splitext(imge)[0])
    #calculating area of face to tell user perfect distance from cam for best results

    gray = cv2.cvtColor(dupe, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    # Draw a rectangle around the faces
    for (x, y, x2, y2) in faces:
        if len(myList) == 0:
            outfile = '%s/%s.jpg' % (path, str(datetime.now().strftime("%m-%d-%Y-%H-%M-%S")))
            res = cv2.imwrite(str(outfile), dupe)
        cv2.rectangle(dupe, (x, y), (x+x2, y+y2), (0, 255, 0), 2)
        area= (x2-x)*(y2-y)//100

    #cv2.imshow('Video', dupe)













# checking for distacnce from camera
    if area > 10:
        pass
        cv2.putText(img,"Too far from camera",(50,50),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
    elif area < -100:
        pass
        cv2.putText(img,"too close to camera",(50,50),cv2.FONT_HERSHEY_PLAIN,2,(255,255,255),2)
    else:
            # face recognition
            encodeKnownList = findEncodeings(images)
            if encodeKnownList == False:
                continue
            imgS = cv2.resize(img,(0,0),None,0.25,0.25)
            imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
            imgSLoc = face_recognition.face_locations(imgS)
            encode = face_recognition.face_encodings(imgS,imgSLoc)

            for enc,loc in zip(encode,imgSLoc):
                match = face_recognition.compare_faces(encodeKnownList,enc)
                faceDis = face_recognition.face_distance(encodeKnownList,enc)
                #print(faceDis)
                if not len(faceDis) == 0:
                    matchIndex = np.argmin(faceDis)

                #if 2 faces mathch
                    if match[matchIndex]:
                        name = imagesName[matchIndex].upper()
                        #print(name)
                        #print(loc)
                        print("faceDetected",name)
                        y1,x2,y2,x1 = loc
                        y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                        cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,255),2)
                        cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 255),cv2.FILLED)
                        cv2.putText(img,name, (x1+6, y2-6),cv2.FONT_HERSHEY_PLAIN,1,(255,255,255),2)
                        # do something when face is detected
                    else:
                        outfile = '%s/%s.jpg' % (path, str(datetime.now().strftime("%m-%d-%Y-%H-%M-%S")))

                        cv2.imwrite(outfile, img)
    cv2.imshow('webcam',img)
    if cv2.waitKey(10)==ord('q'):
        break
video_capture.release()
cv2.destroyAllWindows()

# save security cam video to drive

