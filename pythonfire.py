import cv2
import numpy as np
import requests

# Replace with the appropriate latitude and longitude
LATITUDE = "X"
LONGITUDE = "Y"
WEB_SERVER_URL = "http://<laptop_ip>:<port>/fire_alert"

def send_fire_alert():
    data = {
        "message": f"Fire detected at location: latitude {LATITUDE}, longitude {LONGITUDE}"
    }
    try:
        response = requests.post(WEB_SERVER_URL, json=data)
        if response.status_code == 200:
            print("Alert sent successfully.")
        else:
            print(f"Failed to send alert. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending alert: {e}")

def detect_fire(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_bound = np.array([18, 50, 50], dtype=np.uint8)
    upper_bound = np.array([35, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    fire_detected = cv2.countNonZero(mask) > 5000  # Adjust threshold based on sensitivity
    return fire_detected, mask

# Use the USB webcam; usually index 0 or 1 is used for USB cameras
cap = cv2.VideoCapture(0)  # Change to 1 or higher if necessary

if not cap.isOpened():
    print("Error: Could not open video stream from USB webcam.")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    fire_detected, mask = detect_fire(frame)
    if fire_detected:
        print("Fire detected!")
        send_fire_alert()
        cv2.putText(frame, "FIRE DETECTED!", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow("Fire Detection", frame)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
