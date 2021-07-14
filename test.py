import cv2
import mediapipe as mp

cv = cv2.VideoCapture(0)
mpHands = mp.solutions.hands

hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    
    sucsess,img = cv.read()
    imgmirror = cv2.flip(img,7)
    imgRGB = cv2.cvtColor(imgmirror, cv2.COLOR_BGR2RGB)
    result = hands.process(imgRGB)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:

            for id, lm in enumerate(handLms.landmark):
                h, w, c = imgmirror.shape
                cx ,cy = int(lm.x*w) ,int(lm.y*h)
                if id == 8 :
                    print(cx,cy)
                    cv2.circle(imgmirror, (cx, cy), 10, (255, 255, 255), cv2.FILLED)
            mpDraw.draw_landmarks(imgmirror, handLms, mpHands.HAND_CONNECTIONS)
    cv2.imshow('show',imgmirror)
    cv2.waitKey(1) 
    