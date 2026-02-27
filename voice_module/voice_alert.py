import pyttsx3
import time


class VoiceAlert:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 170)
        self.last_spoken_time = 0
        self.cooldown = 2  # seconds

    def speak(self, message):
        current_time = time.time()

        if current_time - self.last_spoken_time > self.cooldown:
            self.engine.say(message)
            self.engine.runAndWait()
            self.last_spoken_time = current_time

    def system_start(self):
        self.speak("Smart stick system started")

    def object_detected(self, label, distance=None):
        if distance is not None:
            message = f"{label} detected at {distance} centimeters"
        else:
            message = f"{label} detected"

        self.speak(message)   # ✅ FIXED HERE

    def obstacle_alert(self):
        self.speak("Obstacle ahead")

    def system_stop(self):
        self.speak("System stopped")