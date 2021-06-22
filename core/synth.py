from gtts import gTTS
from playsound import playsound


class Synthesizer:

    def __init__(self, source_voice_path='core/voice.mp3', lang="en"):
        self.source_voice_path = source_voice_path
        self.lang = lang

    def speak(self, text):
        tts = gTTS(text=text, lang=self.lang)
        tts.save(self.source_voice_path)
        playsound(self.source_voice_path)
