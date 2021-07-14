import cv2
import mediapipe as mp
import math


class handDetector():
    def __init__(self,mode = False ,maxHands = 1 ,detectionCon=0.75, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,
                                        self.detectionCon)
        self.mpDraw = mp.solutions.drawing_utils


    def findHands(self,img,draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img,handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img


    def fingerPosition(self,img,handNO = 0 ,draw=True):
        self.lmList = []
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNO]
            for id,lm in enumerate(myHand.landmark):
                h , w , c = img.shape
                cx , cy = int(lm.x * w), int(lm.y * h)

                self.lmList.append([id, cx, cy])
                if draw:
                    if id == 0:
                        cv2.circle(img,(cx,cy), 15 , (255 , 0 , 255),cv2.FILLED)

        return self.lmList


    def fingercount(self):
        fingers = []
        tipId = [4,8,12,16,20]
        if len(self.lmList) != 0:
            # thumb
            if self.lmList[tipId[0]][1] < self.lmList[tipId[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            # all fingers
            for id in range(1, 5):
                if self.lmList[tipId[id]][2] < self.lmList[tipId[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

        return fingers



    def fingerDistance(self,tip1,tip2,img,draw = False):
        if len(self.lmList) != 0:
            x1 ,y1 = self.lmList[tip1][1],self.lmList[tip1][2]
            x2 ,y2 = self.lmList[tip2][1],self.lmList[tip2][2]
            #cx ,cy = (x1+x2) // 2 , (y1+y2) // 2
            if draw :
                cv2.circle(img ,(x1,y1) , 10 , (255,0,255) ,cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
                cv2.line(img,(x1,y1),(x2,y2),(255,255,255),3)

            length = math.hypot(x2-x1,y2-y1)
            #print(length)
        return length ,img ,

    def fingerDistance3(self,tip1,tip2,tip3,img,draw = False):
        if len(self.lmList) != 0:
            x1 ,y1 = self.lmList[tip1][1],self.lmList[tip1][2]
            x2 ,y2 = self.lmList[tip2][1],self.lmList[tip2][2]
            x3, y3 = self.lmList[tip3][1], self.lmList[tip3][2]
            #cx ,cy = (x1+x2) // 2 , (y1+y2) // 2
            if draw :
                cv2.circle(img ,(x1,y1) , 10 , (255,0,255) ,cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
                cv2.line(img,(x1,y1),(x2,y2),(255,255,255),3)

                cv2.circle(img, (x3, y3), 10, (255, 0, 255), cv2.FILLED)
                cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
                cv2.line(img, (x3, y3), (x1, y1), (255, 255, 255), 3)

            length = math.hypot(x2-x1,y2-y1)
            length2 = math.hypot(x3-x1,y3 - y1)
            #print(length,"tip 1")
            #print(length2, "tip 2")
        return length ,length2,img


def main():
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success,img = cap.read()
        imgflip = cv2.flip(img, 1)
        imgflip = detector.findHands(imgflip)
        lmList = detector.fingerPosition(imgflip)
        if len(lmList) != 0:
            print(lmList[4],lmList[8],lmList[12],lmList[16],lmList[20])

        cv2.imshow("Hands",imgflip)
        cv2.waitKey(1)




if __name__ == "__main__":
    main()