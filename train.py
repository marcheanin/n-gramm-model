import argparse
import os
import pickle
import re
import sys


def get_text_from_file(filepath):
    text = ""

    with open(filepath, "r", encoding='utf-8') as f:
        for line in f.readlines():
            if line != '\n':
                text += line

    return text


class Train:

    def __init__(self, data_path, model_path):
        self.text = None
        self.data_path = data_path
        self.model_path = model_path
        self.dict = {}

    def do(self):
        self.get_text()

        if len(self.text) > 1:
            print("Start training model...")
            self.train()
            print("Saving model...")
            if not os.path.isfile(self.model_path):
                raise OSError("Model not found")
            else:
                self.save_model()
                print("Complete!")

    def get_text(self):
        self.text = ""
        if self.data_path is not None:
            self.get_text_from_files()
        else:
            self.get_text_from_stdin()
        self.tokenize_text()

    def get_text_from_files(self):
        if self.data_path is None:
            print("Empty directory, try again")
            return
        print("Getting text from " + self.data_path + "...")
        for root, dirs, files in os.walk(self.data_path):
            print("Finded files: ")
            print(files)
            for file in files:
                if file.endswith(".txt"):
                    # print("get file {file}")
                    self.text += get_text_from_file(os.path.join(root, file))

    def get_text_from_stdin(self):
        print('Please input text to train model or \'Exit\':')
        for line in sys.stdin:
            if 'Exit' == line.rstrip():
                break
            print('Please input text to train model or \'Exit\':')
            self.text += line

    def tokenize_text(self):
        self.text = self.text.lower()
        self.text = re.sub(r'[^a-z0-9а-яё\s]', '', self.text)
        self.text = re.sub(r'\n', ' ', self.text)
        self.text = self.text.split()

    def train(self):
        text = self.text
        for i in range(len(text) - 1):
            # для префикса длины 1
            if text[i] not in self.dict:
                self.dict[text[i]] = [text[i + 1]]
            else:
                self.dict[text[i]].append(text[i + 1])

            # для префикса длины 2
            if i > 0 and (text[i - 1], text[i]) not in self.dict:
                self.dict[(text[i - 1], text[i])] = [text[i + 1]]
            elif i > 0:
                self.dict[(text[i - 1], text[i])].append(text[i + 1])

            # для префикса длины 3
            if i > 1 and (text[i - 2], text[i - 1], text[i]) not in self.dict:
                self.dict[(text[i - 2], text[i - 1], text[i])] = [text[i + 1]]
            elif i > 1:
                self.dict[(text[i - 2], text[i - 1], text[i])].append(text[i + 1])

    def save_model(self):
        with open(self.model_path, "w+b") as f:
            pickle.dump(self.dict, f)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", dest="data_path", required=False, help="Directory with files to train model")
    parser.add_argument("--model", dest="model_path", required=True, help="Path to file with model")

    args = parser.parse_args()
    model_path = args.model_path
    data_path = args.data_path

    gen = Train(data_path, model_path)
    gen.do()


if __name__ == '__main__':
    main()
