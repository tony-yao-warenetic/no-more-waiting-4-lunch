import cv2
import time
import numpy as np

cap = cv2.VideoCapture("/dev/video2")
cap2 = cv2.VideoCapture("/dev/video0")
cap3 = cv2.VideoCapture("/dev/video4")
cap4 = cv2.VideoCapture("/dev/video8")
cap5 = cv2.VideoCapture("/dev/video6")
#cap6 = cv2.VideoCapture("/dev/video10")

save_interval = 5  # seconds
last_capture_time = time.time()


#Cameras seem to be interfering with one another. USB Hub can take up to two cameras. Else one will be kicked out

while True:
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()
    ret3, frame3 = cap3.read()
    ret4, frame4 = cap4.read()
    ret5, frame5 = cap5.read()

    
    cv2.imshow('Captured Image', frame)
    cv2.imshow('Captured Image2', frame2)
    cv2.imshow('Captured Image3', frame3)
    cv2.imshow('Captured Image4', frame4)
    cv2.imshow('Captured Image5', frame5)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cap2.release()
cap3.release()
cap4.release()
cap5.release()
cv2.destroyAllWindows()

