import os

from tensorflow.keras.models import load_model
import numpy


class SpeechClassifier:
    __label_to_index, __index_to_label = {}, {}  # mappers
    __encoding = 'utf-8'

    def __init__(self, trained_root_dir=os.path.abspath("model/commands/trained_model")):
        self.trained_root_dir = trained_root_dir
        self.command_labels_file = self.trained_root_dir + '/command_labels.txt'
        self.trained_model_file = self.trained_root_dir + '/model.h5'
        self.model = self.load_trained_model()
        self.labels = open(self.command_labels_file, 'r', encoding=self.__encoding).read().split('\n')

        self.populate_labels()

    def load_trained_model(self):
        if not os.path.exists(self.trained_root_dir):
            raise FileNotFoundError('First run SpeechModelTrainer to generate all needed files')

        return load_model(self.trained_model_file)

    def populate_labels(self):
        for k, label in enumerate(self.labels):
            self.__label_to_index[label] = k
            self.__index_to_label[k] = label

    def classify(self, text):
        data = numpy.zeros((1, 48, 256), dtype='float32')
        for i, char in enumerate(bytes(text.encode(self.__encoding))):
            data[0, i, int(char)] = 1.0

        out = self.model.predict(data)
        index = out.argmax()
        return self.__index_to_label[index]


if __name__ == '__main__':
    # Execute it to test the previous trained model
    speech_classifier = SpeechClassifier(trained_root_dir="commands/trained_model")
    while True:
        input_text = input('Type something: ')
        classified_command = speech_classifier.classify(input_text)
        print(classified_command)
