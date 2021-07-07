import json
import os
import threading

import pyaudio
from vosk import Model, KaldiRecognizer


class Listener:
    __VA_NAME = "lisa"
    __ROOT_DIR = os.path.abspath("core")

    def __init__(self, voice_model_path='en-model'):
        self.chunk = 8000
        self.voice_model_path = voice_model_path
        self.model = Model(self.voice_model_path)
        self.sample_rate = 16000
        self.record_seconds = 2
        self.rec = KaldiRecognizer(self.model, self.sample_rate)
        self.pyaudio = pyaudio.PyAudio()
        self.stream = self.pyaudio.open(format=pyaudio.paInt16, channels=1, rate=self.sample_rate, input=True,
                                        output=True, frames_per_buffer=self.chunk)

    def listen(self, on_listened):
        while True:
            self.stream.start_stream()
            data = self.stream.read(self.chunk)
            if len(data) == 0:
                pass

            if self.rec.AcceptWaveform(data):
                text = json.loads(self.rec.Result())["text"].lower()
                print(text)
                if text.startswith(self.__VA_NAME):
                    text = text.replace(self.__VA_NAME, "").replace(" ", "", 1)
                    if text == "":
                        continue

                    self.stream.stop_stream()
                    on_listened(text)

    def start(self, on_listened):
        thread = threading.Thread(target=self.listen, args=(on_listened,), daemon=True)
        thread.start()
        print("Listening...")
