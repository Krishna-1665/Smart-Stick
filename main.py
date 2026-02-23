import cv2
from ai_module.object_detection import detect_obstacles, get_distance_from_arduino
from voice_module.voice_alert import VoiceAlert


def main():

    # Initialize Voice
    voice = VoiceAlert()
    voice.system_start()

    cap = cv2.VideoCapture(0)
    last_announced = set()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Run Detection
        frame, current_objects = detect_obstacles(frame, last_announced)

        # Get Distance (same function used in detection)
        distance = get_distance_from_arduino()

        # Voice Integration (only new objects)
        new_objects = current_objects - last_announced

        for obj in new_objects:
            voice.object_detected(obj, distance)

            # Extra alert if very close
            if distance < 50:
                voice.obstacle_alert()

        last_announced = current_objects

        cv2.imshow("Smart Stick - Object Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    voice.system_stop()


if __name__ == "__main__":
    main()