from cv2 import cv2
import mediapipe as mp
import time
import math



class handDetector():
    def __init__(self,static_image_mode=False,max_num_hands=2,min_detection_confidence=0.5,min_tracking_confidence=0.5):
        self.mode = static_image_mode
        self.maxHands = max_num_hands
        self.detectionCon = min_detection_confidence
        self.trackCon = min_tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,1,self.detectionCon,self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self,img,draw = True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handlms in self.results.multi_hand_landmarks:

                if draw:

                    self.mpDraw.draw_landmarks(img, handlms, self.mpHands.HAND_CONNECTIONS)
        return img
    def findPos(self,img,handNo=0,draw=True):
        xList = []
        yList = []
        boundingBox = []
        self.lm_list = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]

            for id, landmark in enumerate(myHand.landmark):
                # print((id,landmark))
                height, width, channel = img.shape
                cx, cy = int(landmark.x * width), int(landmark.y * height)
                xList.append(cx)
                yList.append(cy)
                # print(id,cx,cy)
                self.lm_list.append([id,cx,cy])
                if draw:
                     cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)


            xMin,xMax = min(xList),max(xList)
            yMin,yMax = min(yList),max(yList)
            boundingBox = xMin,yMin,xMax,yMax

            if draw:
                cv2.rectangle(img,(boundingBox[0]-20,boundingBox[1]-20),(boundingBox[2]+20,boundingBox[3]+20),(0,255,0),2)

        return self.lm_list,boundingBox

    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lm_list[self.tipIds[0]][1] < self.lm_list[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        for id in range(1, 5):
            if self.lm_list[self.tipIds[id]][2] < self.lm_list[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
                return fingers


    def findDistance(self,p1,p2,img,draw = True):

        # Find Dist
        x1, y1 = self.lm_list[p1][1], self.lm_list[p1][2]
        x2, y2 = self.lm_list[p2][1], self.lm_list[p2][2]

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        if draw:
            cv2.circle(img, (x1, y1), 3, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 3, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 3, (255, 0, 0), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        return length,img,[x1,y1,x2,y2,cx,cy]
        # print(length)
        # handrange = 15 - 85


#
# mpHands = mp.solutions.hands
# hands = mpHands.Hands()
# mpDraw = mp.solutions.drawing_utils



def main():
    ptime = 0
    cTime = 0
    detector = handDetector()
    cap = cv2.VideoCapture(0)

    while True:
        sucess, img = cap.read()
        img = detector.findHands(img,True)
        lmList = detector.findPos(img)
        if len(lmList)!=0:
            print(lmList[4])
        cTime = time.time()
        fps = 1 / (cTime - ptime)
        ptime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Image", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()