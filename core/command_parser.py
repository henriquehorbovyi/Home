
from nlu.model_classifier import ModelClassifier
from services.date_and_time import what_time_is_it, when_is_it_today
from services.weather import check_the_weather
import services.wiki as wiki


class CommandParser:

    def __init__(self):
        self.__classifier = ModelClassifier()

    def parse(self, text, callback):
        classified_answer = self.__classifier.classify(text)

        # Date & Time
        if classified_answer == "time\\what_time_is_it":
            answer = what_time_is_it()
            callback(answer)
        elif classified_answer == "datetime\\what_date_is_it":
            answer = when_is_it_today()
            callback(answer)

        # Weather
        elif classified_answer == "weather\\check_the_weather":
            answer = check_the_weather()
            callback(answer)

        # Wikipedia
        elif "wikipedia\\search" in classified_answer:
            term = classified_answer.split("\\")[-1]
            presearch_answer = wiki.random_presearch_answer(term)
            callback(presearch_answer)
            answer = wiki.search(term)
            callback(answer)

        # General
        else:
            callback(classified_answer)
