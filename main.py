import threading

from core.command_parser import CommandParser
from core.listener import Listener
from core.synth import Synthesizer

if __name__ == '__main__':
    listener = Listener()
    parser = CommandParser()
    synth = Synthesizer()

    def on_listened(text):
        # parser.parse(text, synth.speak)
        parser.chatting(text, synth.speak)


    listener.start(on_listened=on_listened)
    threading.Event().wait()
