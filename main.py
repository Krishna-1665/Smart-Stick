import cv2
from ai_module.object_detection import detect_obstacles
from voice_module.voice_alert import VoiceAlert



def main():
    obstacle_active = False
    voice = VoiceAlert()
    voice.system_start()

    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (640, 480))

        frame, current_objects, distance = detect_obstacles(frame, set())
        distance=float(distance)
        print("Distance:", distance)
        print("Current Objects:", current_objects)

        for obj in current_objects:
            voice.object_detected(obj, distance)

            if distance is not None:
                if distance < 600:
                    if not obstacle_active:
                        print("Obstacle Detected! Speaking...")
                        voice.obstacle_alert()
                        obstacle_active = True
                else:
                    obstacle_active = False

        cv2.imshow("Smart Stick - Object Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    voice.system_stop()


if __name__ == "__main__":
    main()
