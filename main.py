import threading
import detection
import numpy as np
import tkinter as tk
import os
import time
import server


# Begin detection
def start_detection_right():
    if not detection.running_right:
        detection.running_right = True
        # Start the right detection in a separate thread
        threading.Thread(target=detection.right_lane, daemon=True).start()
        

# Stop detection
def stop_detection_right():
    detection.running_right = False
    server.update_line_status(-1, False)
    

# Quit program
def quit_program():
    stop_detection_left()
    stop_detection_right()
    os._exit(0)


# Every 180 seconds, the code checks the program status and determines whether it should begin detection or stop detection.
while True:
    # True --> Begin Detection  False --> Stop Detection
	is_running = server.get_program_status()
	
	if is_running is None:
		print("Value is none, retrying")
		time.sleep(10)
		continue
	
	if is_running and not detection.running_right:
		print("Begin Running Program")
		start_detection_right()
	elif not is_running and detection.running_right:
		print("Stop running program")
		stop_detection_right()
	else:
        # Time Pause
		print("Standing by")
		time.sleep(180)
