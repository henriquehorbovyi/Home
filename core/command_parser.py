from model.chatting.chat_classifier import ChatClassifier
from model.commands.speech_classifier import SpeechClassifier
from services.date_and_time import what_time_is_it, when_is_it_today
from services.weather import check_the_weather


class CommandParser:

    def __init__(self):
        self.__speech_classifier = SpeechClassifier()
        self.__chat_classifier = ChatClassifier()

    def parse(self, text, callback):
        classified_command = self.__speech_classifier.classify(text)

        # Date & Time
        if classified_command == "time\\what_time_is_it":
            answer = what_time_is_it()
            callback(answer)
        elif classified_command == "time\\when_is_it_today":
            answer = when_is_it_today()
            callback(answer)

        # Weather
        elif classified_command == "weather\\check_the_weather":
            answer = check_the_weather()
            callback(answer)

    def chatting(self, text, on_answered):
        answer = self.__chat_classifier.classify(text)
        on_answered(answer)
