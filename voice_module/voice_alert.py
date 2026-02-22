import pyttsx3
import time

class VoiceAlert:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 1.0)

        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)

        self.last_spoken_time = 0
        self.cooldown = 3  # seconds

    def speak(self, message):
        current_time = time.time()

        if current_time - self.last_spoken_time > self.cooldown:
            self.engine.say(message)
            self.engine.runAndWait()
            self.last_spoken_time = current_time
    def object_detected(self, label):
        self.speak(f"{label} detected")

    def obstacle_alert(self):
        self.speak("Obstacle very close")

if __name__ == "__main__":
    voice = VoiceAlert()
    voice.speak("Smart stick system activated")
