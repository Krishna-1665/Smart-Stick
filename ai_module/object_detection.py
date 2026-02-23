from ultralytics import YOLO
import cv2
import time

# -----------------------------
# Load YOLO Model (Fast Nano Version)
# -----------------------------
model = YOLO("yolov8n.pt")

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
DISTANCE_THRESHOLD = 100  # Alert only if object within 100 cm


# -----------------------------
# Placeholder: Distance from Arduino
# Replace with real serial reading later
# -----------------------------
def get_distance_from_arduino():
    """
    Dummy distance simulation.
    Replace this with real Arduino serial integration.
    """
    return 75  # Simulated distance (cm)


# -----------------------------
# Core Detection Function
# -----------------------------
def detect_obstacles(frame, last_announced_objects):
    """
    Detect important obstacles in frame.
    Avoid repeated announcements.
    
    Returns:
        annotated_frame
        current_detected_objects (set)
    """

    results = model(frame)
    detected_objects = set()
    distance = get_distance_from_arduino()

    for result in results:
        for box in result.boxes:

            confidence = float(box.conf[0])
            class_id = int(box.cls[0])
            object_name = model.names[class_id]
             # 🔎 DEBUG PRINT
            print(f"Detected: {object_name} | Confidence: {confidence:.2f} | Distance: {distance} cm")


            if (
                confidence > CONFIDENCE_THRESHOLD
                and any(keyword in object_name for keyword in IMPORTANT_OBJECTS)
                and distance < DISTANCE_THRESHOLD
            ):
                detected_objects.add(object_name)

                # Draw bounding boxes
                frame = result.plot()

                # Show label + distance
                cv2.putText(
                    frame,
                    f"{object_name} - {distance} cm",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2
                )

    # Anti-spam logic (announce only new obstacles)
    new_objects = detected_objects - last_announced_objects

    for obj in new_objects:
        print(f"Alert: {obj} detected at {distance} cm")

    return frame, detected_objects


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

        frame, current_objects = detect_obstacles(frame, last_announced)

        last_announced = current_objects

        cv2.imshow("Smart Stick - Object Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()