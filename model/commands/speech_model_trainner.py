import os

import numpy
import yaml
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical


class SpeechModelTrainer:
    __inputs, __outputs = [], []
    __label_to_index, __index_to_label = {}, {}  # mappers
    __encoding = 'utf-8'

    def __init__(self, root_path=os.path.abspath("commands")):
        self.commands_file = root_path + '/commands.yml'
        self.trained_root_dir = root_path + '/trained_model'
        self.command_labels = self.trained_root_dir + '/command_labels.txt'
        self.trained_model_file = self.trained_root_dir + '/model.h5'

    def open_commands_file(self):
        return yaml.safe_load(open(file=self.commands_file, mode='r', encoding=self.__encoding).read())

    def populate_inputs_and_outputs(self):
        data = self.open_commands_file()
        for command in data['commands']:
            for inp in command['command']['inputs']:
                self.__inputs.append(inp)
                self.__outputs.append("{}\\{}".format(command['command']['entity'], command['command']['action']))

    def populate_labels(self):
        if not os.path.exists(self.trained_root_dir):
            os.makedirs(self.trained_root_dir)

        file_writer = open(self.command_labels, 'w', encoding=self.__encoding)
        labels = set(self.__outputs)

        for k, label in enumerate(labels):
            self.__label_to_index[label] = k
            self.__index_to_label[k] = label
            file_writer.write(label + '\n')
        file_writer.close()

    # Max size of the spoken text
    def max_sequence(self):
        return max([len(bytes(i.encode(self.__encoding))) for i in self.__inputs])

    def build_input_data(self):
        input_data = numpy.zeros((len(self.__inputs), self.max_sequence(), 256), dtype='float32')
        for i, inps in enumerate(self.__inputs):
            for k, char in enumerate(bytes(inps.encode(self.__encoding))):
                input_data[i, k, int(char)] = 1.0
        return input_data

    def build_output_data(self):
        output_data = []
        for output in self.__outputs:
            output_data.append(self.__label_to_index[output])

        return to_categorical(output_data, len(output_data))

    def build_model(self, input_data, output_data):
        model = Sequential()
        model.add(LSTM(128))
        model.add(Dense(len(output_data), activation='softmax'))
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['acc'])
        model.fit(input_data, output_data, epochs=128)
        return model

    def start_training(self):
        self.populate_inputs_and_outputs()
        self.populate_labels()
        input_data = self.build_input_data()
        output_data = self.build_output_data()
        model = self.build_model(input_data, output_data)
        model.save(self.trained_model_file)


if __name__ == '__main__':
    # Execute it to train your model
    SpeechModelTrainer().start_training()
