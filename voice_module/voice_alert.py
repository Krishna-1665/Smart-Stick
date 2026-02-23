"""
voice_alert.py
----------------
Voice module for Smart Assistive Stick Project.
Handles all audio feedback using pyttsx3 (offline text-to-speech).
"""

import pyttsx3
import time


class VoiceAlert:
    def __init__(self, cooldown=3):
        """
        Initialize voice engine and settings.
        :param cooldown: Minimum seconds between two voice alerts
        """
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 150)      # Speech speed
        self.engine.setProperty("volume", 1.0)    # Max volume

        voices = self.engine.getProperty("voices")
        if voices:
            self.engine.setProperty("voice", voices[0].id)

        self.cooldown = cooldown
        self.last_spoken_time = 0
        self.last_message = ""

    # -----------------------------
    # Internal Speak Function
    # -----------------------------
    def _speak(self, message):
        """
        Speak a message if cooldown time has passed.
        Prevents repeated and continuous speaking.
        """
        current_time = time.time()

        if (
            current_time - self.last_spoken_time > self.cooldown
            and message != self.last_message
        ):
            self.engine.say(message)
            self.engine.runAndWait()
            self.last_spoken_time = current_time
            self.last_message = message

    # -----------------------------
    # Public Functions
    # -----------------------------
    def system_start(self):
        """Speak when system starts."""
        self._speak("Smart assistive stick activated")

    def system_stop(self):
        """Speak when system stops."""
        self._speak("Smart assistive stick shutting down")

    def object_detected(self, label):
        """
        Speak detected object name.
        :param label: Object label from YOLO
        """
        message = f"{label} detected"
        self._speak(message)

    def obstacle_alert(self):
        """Speak when obstacle is very close."""
        self._speak("Obstacle very close")

    def custom_message(self, message):
        """
        Speak any custom message.
        """
        self._speak(message)


# -----------------------------
# Testing Section
# -----------------------------
if __name__ == "__main__":
    voice = VoiceAlert()

    voice.system_start()
    time.sleep(2)

    voice.object_detected("person")
    time.sleep(2)

    voice.obstacle_alert()
    time.sleep(2)

    voice.system_stop()