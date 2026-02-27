import pyttsx3
import time


class VoiceAlert:
    def __init__(self):
        self.last_spoken_time = 0
        self.cooldown = 2

    def speak(self, message):
        current_time = time.time()

        if current_time - self.last_spoken_time > self.cooldown:
            try:
                engine = pyttsx3.init()   # 🔥 Reinitialize every time
                engine.setProperty("rate", 170)
                engine.say(message)
                engine.runAndWait()
                engine.stop()
                self.last_spoken_time = current_time
            except Exception as e:
                print("Voice Error:", e)

    def system_start(self):
        self.speak("Smart stick system started")

    def object_detected(self, label, distance=None):
        if distance is not None:
            message = f"{label} detected at {int(distance)} centimeters"
        else:
            message = f"{label} detected"

        self.speak(message)

    def obstacle_alert(self):
        self.speak("Obstacle ahead")

    def system_stop(self):
        self.speak("System stopped")