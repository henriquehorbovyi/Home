import os
import random

import yaml
import pickle
import numpy
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import SGD


class ChatModelTrainer:
    __words, __classes, __documents, __ignored_chars = [], [], [], ['?', '!', '.', ',']
    __lemmatizer = WordNetLemmatizer()

    def __init__(self):
        pass

    def populate_data(self):
        training_data = yaml.safe_load(open(file='training_data.yml', mode='r', encoding='utf-8').read())

        for intents in training_data['intents']:
            tag = intents['intent']['tag']
            patterns = intents['intent']['patterns']
            for pattern in patterns:
                words = nltk.word_tokenize(pattern)
                self.__words.extend(words)
                self.__documents.append((words, tag))
                if tag not in self.__classes:
                    self.__classes.append(tag)
        self.__words = [self.__lemmatizer.lemmatize(word) for word in self.__words if word not in self.__ignored_chars]
        self.__words = sorted(set(self.__words))
        self.__classes = sorted(set(self.__classes))

        if not os.path.exists('trained_model'):
            os.mkdir('trained_model')

        pickle.dump(self.__words, open('trained_model/words.pkl', 'wb'))
        pickle.dump(self.__classes, open('trained_model/classes.pkl', 'wb'))

    def prepare_output(self):
        training = []
        output_empty = [0] * len(self.__classes)
        for doc in self.__documents:
            bag = []
            word_patterns = doc[0]
            word_patterns = [self.__lemmatizer.lemmatize(word.lower()) for word in word_patterns]
            for word in self.__words:
                bag.append(1) if word in word_patterns else bag.append(0)

            output_row = list(output_empty)
            output_row[self.__classes.index(doc[1])] = 1
            training.append([bag, output_row])
        return training

    def build_model(self, training_data):
        random.shuffle(training_data)
        training_data = numpy.array(training_data)

        train_x = list(training_data[:, 0])
        train_y = list(training_data[:, 1])

        model = Sequential()
        model.add(Dense(128, input_shape=(len(train_x[0]),), activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(64, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(train_y[0]), activation='softmax'))

        sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
        model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
        hist = model.fit(numpy.array(train_x), numpy.array(train_y), epochs=256, batch_size=5, verbose=True)
        model.save('trained_model/chat_model.h5', hist)
        return model

    def start_training(self):
        self.populate_data()
        training_data = self.prepare_output()
        return self.build_model(training_data)


if __name__ == '__main__':
    ChatModelTrainer().start_training()
