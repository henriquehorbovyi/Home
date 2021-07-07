class Synthesizer:

    def __init__(self, source_said_path='core/said.wav', lang="en"):
        from gtts import gTTS
        from playsound import playsound
        import subprocess

        self.gTTS = gTTS
        self.playsound = playsound
        self.subprocess = subprocess
        self.source_said_path = source_said_path
        self.lang = lang

    def speak(self, text):
        tts = self.gTTS(text=text, lang=self.lang)
        tts.save(self.source_said_path)
        self.playsound(self.source_said_path)
