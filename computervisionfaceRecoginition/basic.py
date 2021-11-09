import numpy as np
import face_recognition
import cv2
file = 'imagesBase/avik.jpg'
file2 = 'imagesBase/avik1.jpg'
img = face_recognition.load_image_file(file)
img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
img2 = face_recognition.load_image_file(file2)
img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2RGB)


locations2 = face_recognition.face_locations(img2)[0]
encode2 = face_recognition.face_encodings(img2)[0]
locations = face_recognition.face_locations(img)[0]
encode = face_recognition.face_encodings(img)[0]

cv2.rectangle(img2,(locations[3],locations[0]),(locations[1],locations[2]),(255,0,255),2)

cv2.rectangle(img,(locations[3],locations[0]),(locations[1],locations[2]),(255,0,255),2)

result = face_recognition.compare_faces([encode],encode2)
print(result)
encodeVal = face_recognition.face_distance([encode],encode2)
print(encodeVal)
cv2.putText(img2,f'{result} {round(encodeVal[0],2)}',(50,50),cv2.FONT_HERSHEY_PLAIN,1,(0,0,255),2)

cv2.imshow('image',img)
cv2.imshow('image2',img2)
cv2.waitKey(0)