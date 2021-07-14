import cv2
import pyautogui as py
import HandsModule as hm
import numpy as np
import time
sum = 0
cal=0
click_status=0
wCam , hCam = 640 , 480

smoot = 3
pTime = 0
plocX ,plocY = 0,0
clocX , clocY = 0,0
frame = 80

cap = cv2.VideoCapture(0)

cap.set(3,wCam)
cap.set(4,hCam)

detector = hm.handDetector(maxHands=2)

tipTid = [4, 8, 12, 16, 20]

wScr , hScr = py.size()
print('Side of Screen',wScr,hScr)

while True:
    success , img = cap.read()
    imgflip = cv2.flip(img,1)
    img = detector.findHands(imgflip)
    lmList = detector.fingerPosition(img,draw=False)
    if len(lmList) != 0:
        fingers = []
        x1 ,y1 = lmList[tipTid[1]][1:]
        x2 ,y2 = lmList[tipTid[2]][1:]
    #fingers up
    fingers = detector.fingercount()

    #bound
    cv2.rectangle(img,(frame,frame),(wCam-frame,hCam-frame),(255,0,255),3)

    #move mode

    if len(fingers) != 0:



        if fingers[0] == 0 and fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
            length_distance, img = detector.fingerDistance(8, 12, img, draw=True)

            print(length_distance)
            x3 = np.interp(x1 , (frame,wCam-frame) , (0,wScr))
            y3 = np.interp(y1 , (frame,hCam-frame) , (0,hScr))

            py.moveTo(x3,y3)
            cv2.circle(img, (x1, y1), 10, (255, 255, 255), cv2.FILLED)

            if length_distance < 25:
                if click_status == 0 :
                    py.mouseDown()
                    click_status = 1
                cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
                # cv2.circle(img,(x1,y1), 10 , (255,255,0) ,cv2.FILLED )
            else:
                if click_status == 1 :
                    py.mouseUp()
                    click_status = 0



        if fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
            length_distance, length_distance2, img = detector.fingerDistance3(4, 8, 0, img, draw=True)
            per = (length_distance * 100) / length_distance2
            print(per)
            if per < 100:
                if per < 35:
                    cal = (per - 40) * 2
                    py.scroll(int(cal))
                if per > 45:
                    cal = (per - 40) * 2
                    py.scroll(int(cal))


    #show out put
    cv2.imshow('Out Put',imgflip)
    cv2.waitKey(1)