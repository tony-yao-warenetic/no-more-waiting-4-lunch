import cv2
from ultralytics import YOLO
import numpy as np
import base64
import time
import requests
import threading
import tkinter as tk
import os

model = YOLO("yolo11s.pt") #n, s, m, l, x

results_opened = False

running_left = False
running_right = False


def get_upload_status():
    try:
        response = requests.get(STATUS_URL, timeout=3)
        response.raise_for_status()
        return response.json().get("is_sending", False)
    except requests.exceptions.RequestException as e:
        print("Error fetching status:", e)
        return False
       

def send_frame(frame, ind):
    try:
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')
        payload = {'image_base64': img_base64}
       
        if ind == 1:
            response = requests.post(UPLOAD_URL_LEFT, json=payload, timeout=5)
            response.raise_for_status()
        elif ind == 2:
            response = requests.post(UPLOAD_URL_RIGHT, json=payload, timeout=5)
            response.raise_for_status()
        else:
            response = requests.post(UPLOAD_URL_3, json=payload, timeout=5)
            response.raise_for_status()
        print("Image uploaded successfully.")
    except requests.exceptions.RequestException as e:
        print("Error uploading image:", e)


def run_detection(camera_index, server_url, update_status_fn, isLeft):
    global running_left, running_right, results_opened
    cap = cv2.VideoCapture("/dev/v4l/by-id/usb-046d_HD_Pro_Webcam_C920_5B319ECF-video-index0")
    cap2 = cv2.VideoCapture("/dev/v4l/by-id/usb-046d_HD_Pro_Webcam_C920_37F67ECF-video-index0")
    cap3 = cv2.VideoCapture("/dev/v4l/by-id/usb-046d_Logitech_Webcam_C930e_FF19D1DE-video-index0")
    cap4 = cv2.VideoCapture("/dev/v4l/by-id/usb-046d_Logitech_Webcam_C930e_A8CFF0DE-video-index0")
    cap5 = cv2.VideoCapture("/dev/v4l/by-id/usb-046d_Logitech_Webcam_C930e_BFEFF0DE-video-index0")
    if not cap.isOpened():
        print("Error: Unable to open camera.")
        update_status_fn("Error: Unable to open camera")
        return
    last_captured_time = time.time()
   
    while True:
        #CHECK PROGRAM STATUS
        if isLeft and not running_left:
            break
        elif not isLeft and not running_right:
            break
           
        #CAMERA FEED
        ret, frame = cap.read()
        ret2, frame2 = cap2.read()
        ret3, frame3 = cap3.read()
        ret4, frame4 = cap4.read()
        ret5, frame5 = cap5.read()
        if time.time()-last_captured_time < 5:
            continue
        #cv2.imshow("test", frame)
        if not ret:
            print("Error Reading Camera: Check Camera Connection")
            break
       
        #RUN YOLO
        results = model(frame,classes=[0])
        results2 = model(frame2, classes=[0])
        results3 = model(frame3, classes=[0])
        people_count = 0
        people_count2 = 0
        people_count3 = 0
        for r in results:
            for box in r.boxes:
                if int(box.cls) == 0:
                    people_count += 1
        for r in results2:
            for box in r.boxes:
                if int(box.cls) == 0:
                    people_count2 += 1
        for r in results3:
            for box in r.boxes:
                if int(box.cls) == 0:
                    people_count3 += 1
       
        #UPLOAD DATA TO SERVER
        url = f"{server_url}/{people_count+people_count2+people_count3}/{(people_count+people_count2+people_count3) * 12}/passkey**"
       
        try:
            response = requests.post(url)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
        except requests.exceptions.RequestException as e:
            print("Error sending data to server:", e)
            update_status_fn(e)
       
        #UPLOAD DIAGNOSTIC IMAGES IF NEEDED
        try:
            if get_upload_status():
                send_frame(results2[0].plot(), 1)
                send_frame(results3[0].plot(), 2)
                send_frame(results[0].plot(), 3)
        except Exception as e:
            print(f"Error while sending frame: {e}")

        #UPDATE MISCELLANEOUS
        update_status_fn(people_count)
        if cv2.waitKey(1) == ord('q'):
            break
           
        #UPDATE TIME ELAPSED
        last_captured_time = time.time()
    cap.release()
    cap2.release()
    cap3.release()

# Functions to start and stop the detection for left and right
def start_detection_left():
    global running_left
    if not running_left:
        running_left = True
        # Start the left detection in a separate thread
        threading.Thread(target=run_detection_left, args=("/dev/v4l/by-id/usb-046d_HD_Pro_Webcam_C920_37F67ECF-video-index0", SERVER_URL_LEFT, update_left_status, True), daemon=True).start()
        label_left_status.config(text="Left Lane Detection: ON", fg="green")

def start_detection_right():
    global running_right
    if not running_right:
        running_right = True
        # Start the right detection in a separate thread
        threading.Thread(target=run_detection, args=("/dev/v4l/by-id/usb-046d_Logitech_Webcam_C930e_FF19D1DE-video-index0", SERVER_URL_RIGHT, update_right_status, False), daemon=True).start()
        label_right_status.config(text="Right Lane Detection: ON", fg="green")

def stop_detection_left():
    global running_left
    running_left = False
    label_left_status.config(text="Left Lane Detection: OFF", fg="red")
    url = f"{SERVER_URL_LEFT}/{-1}/{-1}/passkey**"
           
    try:
        response = requests.post(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
    except requests.exceptions.RequestException as e:
        print("Error sending data to server:", e)

def stop_detection_right():
    global running_right
    running_right = False
    label_right_status.config(text="Right Lane Detection: OFF", fg="red")
    url = f"{SERVER_URL_RIGHT}/{-1}/{-1}/passkey**"
           
    try:
        response = requests.post(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
    except requests.exceptions.RequestException as e:
        print("Error sending data to server:", e)

def quit_program():
    stop_detection_left()
    stop_detection_right()
    os._exit(0)

# Update the status labels
def update_left_status(people_count):
    label_left_status.config(text=f"Left Lane Detection: {people_count} people detected", fg="green")

def update_right_status(people_count):
    label_right_status.config(text=f"Right Lane Detection: {people_count} people detected", fg="green")

# Tkinter window setup
window = tk.Tk()
window.title("Detection Control")

label = tk.Label(window, text="Welcome to Stevenson Smart Dining System", font=("Arial", 16))
label.pack(pady=10)

start_button_left = tk.Button(window, text="Start Detection for Left Lane", width=20, height=2, command=start_detection_left)
start_button_left.pack(pady=10)

start_button_right = tk.Button(window, text="Start Detection for Right Lane", width=20, height=2, command=start_detection_right)
start_button_right.pack(pady=10)

stop_button_left = tk.Button(window, text="Stop Detection for Left Lane", width=20, height=2, command=stop_detection_left)
stop_button_left.pack(pady=10)

stop_button_right = tk.Button(window, text="Stop Detection for Right Lane", width=20, height=2, command=stop_detection_right)
stop_button_right.pack(pady=10)

quit_button = tk.Button(window, text="Quit Program", width=20, height=2, command=quit_program)
quit_button.pack(pady=10)

# Status labels for the detection of each lane
label_left_status = tk.Label(window, text="Left Lane Detection: OFF", font=("Arial", 12), fg="red")
label_left_status.pack(pady=5)

label_right_status = tk.Label(window, text="Right Lane Detection: OFF", font=("Arial", 12), fg="red")
label_right_status.pack(pady=5)

window.mainloop()
