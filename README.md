# Dining Hall Wait Time Prediction System

This project is a **computer vision-based system** that predicts the wait time in a dining hall by counting the number of people in line using live camera feeds. It uses **YOLO (You Only Look Once)** object detection and communicates with a backend server to send people count data and diagnostic images.

---

## 📸 Overview

The system connects to multiple cameras, captures video frames, detects people in those frames, and sends both counts and optionally images to a backend for real-time monitoring.

- Cameras: `/dev/video0`, `/dev/video2`, `/dev/video4`, `/dev/video6`
- Model: YOLO (via [Ultralytics YOLO](https://docs.ultralytics.com/))
- Language: Python
- Communication: HTTP requests to RESTful backend endpoints

---

## 🧠 How It Works (Step-by-Step Breakdown)

### 1. **Main Control Loop**
Located in the main script, the system continuously checks with the backend if the detection process should be running using:

```python
is_running = server.get_program_status()
```
If True, it starts detection using a new thread:
threading.Thread(target=detection.right_lane, daemon=True).start()

If False, it stops the detection.

This loop checks the status every 180 seconds.

### 2. **Detection Module (detection.py)**
🔍 Initialization
1. Loads a YOLO model using YOLO("yolo11l.pt").
2. Opens 4 camera streams.
3. Prepares a region of interest (ROI) mask using polygon points to crop the relevant area of the frame.

👁️ Detection Loop
1. Reads frames from each camera.
2. Applies the YOLO model to detect people in each frame.
3. Calculates total number of people from all 4 streams.
4. Sends the count to the backend using:
```python
server.update_line_status(total_people_count, isLeft=False)
```
5. If upload status is enabled (server.get_upload_status()), sends the diagnostic images using base64-encoded JPEGs.

🛑 Exit
Releases all camera resources once the loop ends or the program is stopped.

###3. **Server Communication (server.py)**
✅ get_program_status()
Checks whether the detection should be running (controlled by a backend switch).

✅ update_line_status(number, isLeft)
Sends the number of detected people and estimated wait time (people × 12 seconds) to backend.

✅ get_upload_status()
Checks if the system should upload diagnostic images.

✅ send_frame(frame, index)
Encodes image in base64 and POSTs it to backend for diagnostic visualization.

## 🗂️ File Structure
```bash
.
├── detection.py         # Core detection logic (YOLO + OpenCV)
├── server.py            # Backend communication module
├── main.py              # Entry point and control loop
├── yolo11l.pt           # YOLO model file (not included)
└── README.md            # You're reading it!
```

## 🔧 Requirements
Install all dependencies with:
```bash
pip install ultralytics opencv-python requests numpy
```

## 📡 Backend Server Endpoints
All URLs are placeholders. Replace them with actual backend URLs.

```python
RESULTS_URL_LEFT = "URL..."
RESULTS_URL_RIGHT = "URL..."
STATUS_URL = "URL..."
UPLOAD_URL = "URL..."
PROGRAM_STATUS_URL = "URL..."
```

## 🧑‍💻 Author
Developed with love and care by Tony Yao 25' for improving operational efficiency in dining hall wait time management using real-time computer vision.
