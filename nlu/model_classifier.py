import pickle
import random

import nltk
import numpy
import numpy as np
import yaml
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model


class ModelClassifier:
    __lemmatizer = WordNetLemmatizer()

    def __init__(self, model_path='nlu/trained_model/model.h5'):
        self.model = load_model(model_path)
        self.words = pickle.load(open('nlu/trained_model/words.pkl', 'rb'))
        self.classes = pickle.load(open('nlu/trained_model/classes.pkl', 'rb'))
        self.training_data = yaml.safe_load(open(file='nlu/dataset.yml', encoding='utf-8').read())

    def clean_up_sentence(self, sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [self.__lemmatizer.lemmatize(word) for word in sentence_words]
        return sentence_words

    def bag_of_words(self, sentence):
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0] * len(self.words)
        for word in sentence_words:
            for i, w in enumerate(self.words):
                if word == w:
                    bag[i] = 1
        return np.array(bag)

    def predict_intent_tag(self, sentence):
        bow = self.bag_of_words(sentence)
        prediction = self.model.predict(numpy.array([bow]))[0]
        error_threshold = 0.25
        results = [[i, r] for i, r in enumerate(prediction) if r > error_threshold]
        results.sort(key=lambda item: item[1], reverse=True)

        output = []
        for result in results:
            output.append({'intent': self.classes[result[0]], 'probability': str(result[1])})

        return output

    def replace_action_term(self, tag, action, sentence, patterns):
        action_term = ""

        for pattern in patterns:
            p = set(pattern.split(" "))
            s = set(sentence.split(" "))
            diff = s.difference(p)
            if len(diff) == 1:
                action_term = diff.pop()
                break
        return "{0}\\{1}\\{2}".format(tag, action, action_term)

    def classify(self, sentence):
        prediction = self.predict_intent_tag(sentence)
        predicted_tag = prediction[0]['intent']
        scenarios = self.training_data['scenarios']
        answer = "can't clearly understand what you mean"

        for scenario in scenarios:
            if predicted_tag == scenario['intent']['tag']:
                intent = scenario['intent']
                action = intent['action']
                patterns = intent['patterns']

                # default action is a tag\\action >>> E.g: time\\what_time_is_it
                answer = "{}\\{}".format(predicted_tag, action)

                # if action comes with argument like: wikipedia/search/<query>,
                # youtube/search/<query>, service/search/<query>
                action_term = self.replace_action_term(predicted_tag, action, sentence, patterns)

                if "<query>" in " ".join(patterns):
                    answer = action_term

                # if there's no action, usually for talk-back commands
                if action is None:
                    answer = random.choice(intent['responses'])

        return answer
