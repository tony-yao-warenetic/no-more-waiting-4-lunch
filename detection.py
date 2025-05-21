import cv2
from ultralytics import YOLO
import numpy as np
import server
import time
import threading

# Detection Model -> Ultralytics YOLO
model = YOLO("yolo11l.pt") #n, s, m, l, x

running_right = False

# Detection
def right_lane():
    global running_left
    
    # Turning on the camera through camera index
    cap = cv2.VideoCapture("/dev/video0")
    cap2 = cv2.VideoCapture("/dev/video2")
    cap3 = cv2.VideoCapture("/dev/video4")
    cap4 = cv2.VideoCapture("/dev/video6")

    if not cap.isOpened() or not cap2.isOpened() or not cap3.isOpened() or not cap4.isOpened():
        print("Error: Unable to open camera.")
        #update_status_fn("Error: Unable to open camera")
        return
    
    last_captured_time = time.time()
    
    while True:
        #CHECK PROGRAM STATUS
        if not running_right:
            break
            
        #GET CAMERA FEED
        ret, frame = cap.read()
        ret2, frame2 = cap2.read()
        ret3, frame4 = cap3.read()
        ret4, frame3 = cap4.read()
        if time.time()-last_captured_time < 5:
            continue 
        
        if not ret or not ret2 or not ret3:
            print("Error Reading Camera: Check Camera Connection")
            break
        
        # CROPPING IMAGE
        points = np.array([[0, 190],[200,110], [360,90],[720,0],[720,200],[560, 300],[35,450],[0,480],[0,0]], np.int32)
        points = points.reshape((-1, 1, 2))
            
        mask = np.zeros(frame4.shape[:2], dtype=np.uint8)
        cv2.fillPoly(mask, [points], 255)

        masked_frame = cv2.bitwise_and(frame4, frame4, mask=mask);

        x, y, w, h = cv2.boundingRect(points)
        cropped = masked_frame[y:y+h, x:x+w]

        #RUN YOLO
        results = model(frame, classes=[0])
        results2 = model(frame2, classes=[0])
        results3 = model(frame3, classes=[0])
        results4 = model(cropped, classes=[0])
        people_count = len(results[0])
        people_count2 = len(results2[0])
        people_count3 = len(results3[0])
        people_count4 = len(results4[0])
        
        #UPLOAD DATA TO SERVER
        server.update_line_status(people_count+people_count2+people_count3+people_count4,False)
        
        if server.get_upload_status():
            server.send_frame(results[0].plot(), 1)
            server.send_frame(results2[0].plot(), 2)
            server.send_frame(results3[0].plot(), 3)
            server.send_frame(results4[0].plot(), 4)

        #UPDATE MISCELLANEOUS
        #update_status_fn(people_count)
        # ~ if cv2.waitKey(1) == ord('q'):
            # ~ break

        #UPDATE TIME ELAPSED
        last_captured_time = time.time()
    
    # SHUTTING DOWN CAMERAS
    cap.release()
    cap2.release()
    cap3.release()
    cap4.release()
    
