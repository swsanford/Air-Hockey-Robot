import numpy as np
import cv2

cap = cv2.VideoCapture(1)
cap.set(3,640)
cap.set(4,480)
low_range = np.array([40, 110, 110])
high_range = np.array([70, 250, 250])
prevPt = (0, 0)
prevX = 0
prevY = 0
radius = 0
center = (int(0),int(0))


def _wait_(radius, center):
    while(radius < 10):
        #color detection
        ret, frame = cap.read()
        hue_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        threshold_img = cv2.inRange(hue_image, low_range, high_range)
        contour, hierarchy = cv2.findContours(threshold_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        center = contour[0]    
        moment = cv2.moments(center)  

        #Set up for circle and current point
        (x,y),radius = cv2.minEnclosingCircle(center)
        currentPt = (int(x), int(y))
        center = (int(x),int(y))
        radius = int(radius)

        cv2.imshow('video',frame)

while(cap.isOpened()):

    #color detection
    ret, frame = cap.read()
    hue_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    threshold_img = cv2.inRange(hue_image, low_range, high_range)
    contour, hierarchy = cv2.findContours(threshold_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
    try:
        center = contour[0]    
        moment = cv2.moments(center)

    
        #Set up for circle and current point
        (x,y),radius = cv2.minEnclosingCircle(center)
        currentPt = (int(x), int(y))
        center = (int(x),int(y))
        radius = int(radius)
        if (radius < 20):
            _wait_(radius, center)

        img = cv2.circle(frame,center,radius,(0,255,0),2)

        #math for gettimg a future point
        futX = (int(x)+(int(x)-prevX))
        futY = (int(y)+(int(y)-prevY))
        futPt= (futX,futY)

        #draw line and display video
        img = cv2.line(frame, currentPt, futPt,(0,255,0),2)
        cv2.imshow('video',frame)

        #save these as previous points for next cycle
        prevPt = (int(x), int(y))
        prevX = int(x)
        prevY = int(y)

    except:
        #color detection
        ret, frame = cap.read()
        hue_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        threshold_img = cv2.inRange(hue_image, low_range, high_range)
        contour, hierarchy = cv2.findContours(threshold_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.imshow('video',frame)
          

    #if esc is pressed, quit
    if cv2.waitKey(10) == 27:
        break

cap.release()
cv2.destroyAllWindows()