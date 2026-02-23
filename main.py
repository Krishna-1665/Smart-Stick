from voice_module.voice_alert import VoiceAlert 
from cProfile import label
from voice_module.voice_alert import VoiceAlert

voice = VoiceAlert()

voice.system_start()

voice.object_detected(label)

voice.obstacle_alert()

voice.system_stop()
print("We are going to create a smart stick")
