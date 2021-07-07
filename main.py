import sys
from os.path import realpath, join

from flask import Flask, render_template, jsonify

from core.command_parser import CommandParser
from core.listener import Listener
from core.synth import Synthesizer

sys.path.append(realpath(join(realpath(__file__), '..', '..')))

global listener, synth, command_parser
app = Flask(__name__, template_folder='template')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/start")
def start():
    on_listened = OnListened()
    listener.start(on_listened)
    return jsonify('Lisa is listening...')


@app.route("/get_audio")
def get_audio():
    transcript = open('transcript.txt', 'r', encoding='utf-8').read()
    return jsonify(transcript)


class OnListened:

    def __call__(self, said):
        command_parser.parse(said, self.save_speak)

    def save_speak(self, transcript):
        open("transcript.txt", 'w+', encoding='utf-8').write(transcript)
        synth.speak(transcript)


if __name__ == "__main__":
    command_parser = CommandParser()
    synth = Synthesizer()
    listener = Listener()

    # webbrowser.open_new('http://127.0.0.1:7000/')
    app.run(port=7000)
