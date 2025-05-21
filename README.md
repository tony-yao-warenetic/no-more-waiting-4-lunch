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
Loads a YOLO model using YOLO("yolo11l.pt"). Opens 4 camera streams. Prepares a region of interest (ROI) mask using polygon points to crop the relevant area of the frame.

👁️ Detection Loop
Reads frames from each camera. Applies the YOLO model to detect people in each frame. Calculates total number of people from all 4 streams.

Sends the count to the backend using:
```python
server.update_line_status(total_people_count, isLeft=False)
```
If upload status is enabled (server.get_upload_status()), sends the diagnostic images using base64-encoded JPEGs.

🛑 Exit
Releases all camera resources once the loop ends or the program is stopped.
3. Server Communication (server.py)
✅ get_program_status()
Checks whether the detection should be running (controlled by a backend switch).

✅ update_line_status(number, isLeft)
Sends the number of detected people and estimated wait time (people × 12 seconds) to backend.

✅ get_upload_status()
Checks if the system should upload diagnostic images.

✅ send_frame(frame, index)
Encodes image in base64 and POSTs it to backend for diagnostic visualization.

🗂️ File Structure
bash
Copy
Edit
.
├── detection.py         # Core detection logic (YOLO + OpenCV)
├── server.py            # Backend communication module
├── main.py              # Entry point and control loop
├── yolo11l.pt           # YOLO model file (not included)
└── README.md            # You're reading it!
🔧 Requirements
Install all dependencies with:

bash
Copy
Edit
pip install ultralytics opencv-python requests numpy
Note: You need to install the appropriate version of OpenCV and Ultralytics' YOLO. Also, the YOLO model file (yolo11l.pt) should be trained or downloaded separately.

🧪 Camera Calibration
Ensure cameras are connected and accessible at:

/dev/video0

/dev/video2

/dev/video4

/dev/video6

Calibrate the polygon cropping region in detection.py if your dining hall layout is different.

📡 Backend Server Endpoints
All URLs are placeholders. Replace them with actual backend URLs.

python
Copy
Edit
RESULTS_URL_LEFT = "URL..."
RESULTS_URL_RIGHT = "URL..."
STATUS_URL = "URL..."
UPLOAD_URL = "URL..."
PROGRAM_STATUS_URL = "URL..."
⚠️ Known Limitations
No dynamic error recovery for camera disconnection.

The cropping polygon is hardcoded and may need adjustment per deployment.

System assumes all detected people are in line (no additional filtering).

🚀 Future Improvements
Add left lane support

Improve detection filtering (exclude sitting individuals)

Visual dashboard integration

Auto calibration of ROI

🧑‍💻 Author
Developed for improving operational efficiency in dining hall wait time management using real-time computer vision.

css
Copy
Edit

Let me know if you’d like a separate `requirements.txt` or a diagram to visualize the data flow.






You said:
put everything in a file so i can just copy and paste


ChatGPT said:
Sure! Here's the entire README.md content in one code block so you can copy and paste it directly:

markdown
Copy
Edit
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
If True, it starts detection using a new thread:
threading.Thread(target=detection.right_lane, daemon=True).start()

If False, it stops the detection.

This loop checks the status every 180 seconds.

2. Detection Module (detection.py)
🔍 Initialization
Loads a YOLO model using YOLO("yolo11l.pt")

Opens 4 camera streams

Prepares a region of interest (ROI) mask using polygon points to crop the relevant area of the frame.

👁️ Detection Loop
Reads frames from each camera.

Applies the YOLO model to detect people in each frame.

Calculates total number of people from all 4 streams.

Sends the count to the backend using:

python
Copy
Edit
server.update_line_status(total_people_count, isLeft=False)
If upload status is enabled (server.get_upload_status()), sends the diagnostic images using base64-encoded JPEGs.

🛑 Exit
Releases all camera resources once the loop ends or the program is stopped.

3. Server Communication (server.py)
✅ get_program_status()
Checks whether the detection should be running (controlled by a backend switch).

✅ update_line_status(number, isLeft)
Sends the number of detected people and estimated wait time (people × 12 seconds) to backend.

✅ get_upload_status()
Checks if the system should upload diagnostic images.

✅ send_frame(frame, index)
Encodes image in base64 and POSTs it to backend for diagnostic visualization.

🗂️ File Structure
bash
Copy
Edit
.
├── detection.py         # Core detection logic (YOLO + OpenCV)
├── server.py            # Backend communication module
├── main.py              # Entry point and control loop
├── yolo11l.pt           # YOLO model file (not included)
└── README.md            # You're reading it!
🔧 Requirements
Install all dependencies with:

bash
Copy
Edit
pip install ultralytics opencv-python requests numpy
Note: You need to install the appropriate version of OpenCV and Ultralytics' YOLO. Also, the YOLO model file (yolo11l.pt) should be trained or downloaded separately.

🧪 Camera Calibration
Ensure cameras are connected and accessible at:

/dev/video0

/dev/video2

/dev/video4

/dev/video6

Calibrate the polygon cropping region in detection.py if your dining hall layout is different.

📡 Backend Server Endpoints
All URLs are placeholders. Replace them with actual backend URLs.

python
Copy
Edit
RESULTS_URL_LEFT = "URL..."
RESULTS_URL_RIGHT = "URL..."
STATUS_URL = "URL..."
UPLOAD_URL = "URL..."
PROGRAM_STATUS_URL = "URL..."
⚠️ Known Limitations
No dynamic error recovery for camera disconnection.

The cropping polygon is hardcoded and may need adjustment per deployment.

System assumes all detected people are in line (no additional filtering).

🚀 Future Improvements
Add left lane support

Improve detection filtering (exclude sitting individuals)

Visual dashboard integration

Auto calibration of ROI

🧑‍💻 Author
Developed for improving operational efficiency in dining hall wait time management using real-time computer vision.

vbnet
Copy
Edit

Let me know if you want a downloadable version or want to integrate this into a GitHub project structure.






You said:
put everything in markdown


ChatGPT said:
Absolutely! Below is the full content formatted completely in Markdown, ready for copy-paste into a README.md file:

markdown
Copy
Edit
# Dining Hall Wait Time Prediction System

This project is a **computer vision-based system** that predicts the wait time in a dining hall by counting the number of people in line using live camera feeds. It uses **YOLO (You Only Look Once)** object detection and communicates with a backend server to send people count data and diagnostic images.

---

## 📸 Overview

The system connects to multiple cameras, captures video frames, detects people in those frames, and sends both counts and optionally images to a backend for real-time monitoring.

- **Cameras**: `/dev/video0`, `/dev/video2`, `/dev/video4`, `/dev/video6`
- **Model**: YOLO (via [Ultralytics YOLO](https://docs.ultralytics.com/))
- **Language**: Python
- **Communication**: HTTP requests to RESTful backend endpoints

---

## 🧠 How It Works

### 1. Main Control Loop (`main.py`)

A continuous loop checks whether the detection system should be running using the backend flag.

```python
is_running = server.get_program_status()
If True, it starts detection in a background thread:

python
Copy
Edit
threading.Thread(target=detection.right_lane, daemon=True).start()
If False, it stops detection via stop_detection_right().

The loop sleeps for 180 seconds between checks.

2. Detection System (detection.py)
✅ Setup
Loads a YOLO model:

python
Copy
Edit
model = YOLO("yolo11l.pt")
Opens four camera devices.

Defines a polygon mask for region-of-interest cropping.

🔁 Detection Loop
Every few seconds:

Captures frames from 4 cameras.

Crops one of the frames using a polygonal mask.

Runs YOLO detection for each frame:

python
Copy
Edit
results = model(frame, classes=[0])
Counts people in all 4 frames:

python
Copy
Edit
people_count = len(results[0])
Sends the total people count to the backend:

python
Copy
Edit
server.update_line_status(total_people_count, isLeft=False)
Sends annotated images if image uploading is enabled:

python
Copy
Edit
server.send_frame(results[0].plot(), 1)
Releases cameras when detection stops.

3. Server Communication (server.py)
get_program_status()
Gets whether detection should start or stop.

update_line_status(number, isLeft)
Sends the number of people and an estimated wait time (people × 12 seconds) to the backend.

get_upload_status()
Returns True if diagnostic image uploads are enabled.

send_frame(frame, index)
Converts an image to base64 and sends it to the backend.

📂 File Structure
graphql
Copy
Edit
.
├── detection.py         # Detection logic using YOLO and OpenCV
├── server.py            # Communication with backend APIs
├── main.py              # Control loop managing detection start/stop
├── yolo11l.pt           # YOLO model weights (not included)
└── README.md            # Project documentation
🛠️ Requirements
Install the required Python packages:

bash
Copy
Edit
pip install ultralytics opencv-python requests numpy
⚠️ Make sure yolo11l.pt exists or is downloaded beforehand. It's required for object detection.

🧪 Camera Calibration
Ensure the following camera devices are available:

/dev/video0

/dev/video2

/dev/video4

/dev/video6

The polygon mask coordinates (used to crop detection area) can be edited inside detection.py.

🔌 Backend URLs
Update the following constants in server.py with your actual API endpoints:

python
Copy
Edit
RESULTS_URL_LEFT = "URL..."
RESULTS_URL_RIGHT = "URL..."
STATUS_URL = "URL..."
UPLOAD_URL = "URL..."
PROGRAM_STATUS_URL = "URL..."
⚠️ Known Issues
No dynamic handling if a camera disconnects during runtime.

Hardcoded ROI polygon for one of the frames.

Assumes everyone detected is in line (no queue-specific filtering).

🚀 Possible Improvements
Add left lane support

Filter out non-queue people

Support camera reconnect/recovery

Integrate real-time dashboard

Automatic ROI selection

👨‍💻 Author
Developed to improve real-time efficiency tracking in university dining halls using computer vision.

vbnet
Copy
Edit

Let me know if you'd like this exported as a `.md` file or added to a ZIP with your source code!










