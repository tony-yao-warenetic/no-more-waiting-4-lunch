import requests
import base64
import cv2

# URLs to backend server (Hidden for security purposes)
RESULTS_URL_LEFT = "URL..."
RESULTS_URL_RIGHT = "URL..."
STATUS_URL = "URL..."
UPLOAD_URL = "URL..."
PROGRAM_STATUS_URL = "URL..."


# Send diagnostic images to backend (Not stored)
def send_frame(frame, ind):
    try:
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_base64 = base64.b64encode(img_encoded).decode('utf-8')
        payload = {'image_base64': img_base64, "index":ind}
        
        response = requests.post(UPLOAD_URL, json=payload, timeout=5)
        response.raise_for_status()
        
        print("Image uploaded successfully.")
    except requests.exceptions.RequestException as e:
        print("Error uploading image:", e)


# Check upload status, determine whether it should upload or not
def get_upload_status():
    try:
        response = requests.get(STATUS_URL, timeout=3)
        response.raise_for_status()
        return response.json().get("is_sending", False)
    except requests.exceptions.RequestException as e:
        print("Error fetching status:", e)
        return False


# Updating data to backend
def update_line_status(number, isLeft):
    url = ""
    multiply = number*12
    if number == -1:
        multiply = -1
    if isLeft:
        url = f"{RESULTS_URL_LEFT}/{number}/{multiply}/passkey"
    else:
        url = f"{RESULTS_URL_RIGHT}/{number}/{multiply}/passkey"
    print(url)

    try:
        response = requests.post(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)
    except Exception as e:
        print(f"Error while sending frame: {e}")
        

# Check program status, determine whether it should run or stop
def get_program_status():
    try:
        response = requests.get(PROGRAM_STATUS_URL, timeout=5)  # timeout after 5 seconds if server hangs
        if response.status_code == 200:
            try:
                data = response.json()
                return data.get("is_running")
            except ValueError:
                print("Server response was not valid JSON.")
                return None
        else:
            print(f"Server error: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return None
