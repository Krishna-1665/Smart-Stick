from ultralytics import YOLO
import cv2
import time
import serial

# -----------------------------
# Load YOLO Model (Fast Nano Version)
# -----------------------------
model = YOLO("yolov8n.pt")

# -----------------------------
# Arduino Serial Connection
# -----------------------------
arduino = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)

# -----------------------------
# Smart Stick Important Objects
# -----------------------------
IMPORTANT_OBJECTS = [
    "person",
    "chair",
    "dining table",
    "car",
    "bicycle",
    "motorcycle",
    "truck",
    "bus"
]

CONFIDENCE_THRESHOLD = 0.3
DISTANCE_THRESHOLD = 50   # Speak only if object within 60 cm


# -----------------------------
# Get Distance From Arduino
# -----------------------------
last_valid_distance = 200.0  # global variable

def get_distance_from_arduino():
    global last_valid_distance

    try:
        if arduino.in_waiting > 0:
            raw = arduino.readline().decode().strip()
            print("RAW FROM ARDUINO:", raw)

            import re
            numbers = re.findall(r"\d+", raw)

            if numbers:
                last_valid_distance = float(numbers[0])

        return last_valid_distance

    except Exception as e:
        print("Serial Error:", e)
        return last_valid_distance
    
# -----------------------------
# Core Detection Function
# -----------------------------
def detect_obstacles(frame, last_announced_objects):

    results = model(frame, stream=True, imgsz=320)
    detected_objects = set()

    # Get distance once per frame
    distance = get_distance_from_arduino()

    for result in results:
        for box in result.boxes:

            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            object_name = model.names[class_id]

            print(f"Detected: {object_name} | Confidence: {confidence:.2f} | Distance: {distance} cm")

            # Check if important object
            if (
                confidence > CONFIDENCE_THRESHOLD
                and object_name in IMPORTANT_OBJECTS
            ):

                # Draw bounding box
                frame = result.plot()

                cv2.putText(
                    frame,
                    f"{object_name} - {distance} cm",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

                # Only add if close enough
                detected_objects.add(object_name)

    return frame, detected_objects, distance


# -----------------------------
# Standalone Test Mode
# -----------------------------
if __name__ == "__main__":

    cap = cv2.VideoCapture(0)
    last_announced = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame, current_objects, distance = detect_obstacles(frame, last_announced)

        print("Distance:", distance)
        print("Current Objects:", current_objects)

        last_announced = current_objects

        cv2.imshow("Smart Stick - Object Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()