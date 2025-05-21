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
