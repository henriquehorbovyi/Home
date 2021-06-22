import pickle
import random

import nltk
import numpy
import numpy as np
import yaml
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model


class ChatClassifier:
    __lemmatizer = WordNetLemmatizer()

    def __init__(self, model_path='model/chatting/trained_model/chat_model.h5'):
        self.model = load_model(model_path)
        self.words = pickle.load(open('model/chatting/trained_model/words.pkl', 'rb'))
        self.classes = pickle.load(open('model/chatting/trained_model/classes.pkl', 'rb'))
        self.training_data = yaml.safe_load(open(file='model/chatting/training_data.yml', encoding='utf-8').read())

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

    def classify(self, sentence):
        prediction = self.predict_intent_tag(sentence)
        predicted_tag = prediction[0]['intent']
        # TODO prediction_probability = prediction[0]['intent']

        intents = self.training_data['intents']
        answer = "can't clearly understand what you mean"

        print(sentence)
        print()
        print(prediction)
        for intent in intents:
            if predicted_tag == intent['intent']['tag']:
                answer = random.choice(intent['intent']['responses'])
        return answer
