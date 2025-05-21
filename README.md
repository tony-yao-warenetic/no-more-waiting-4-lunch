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
