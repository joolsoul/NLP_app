import os
from enum import Enum

import pymorphy2
from flask import Flask, request, render_template
from util import TokenizationUtils as Tokenization
from util import FileUtils

app = Flask(__name__)


class Part_of_speech(Enum):
    NOUN = "Noun"
    ADJF = "Adjective name (full)"
    ADJS = "Adjective name (short)"
    COMP = "Comparative"
    VERB = "Verb"
    INFN = "Verb"
    PRTF = "Participle (full)"
    PRTS = "Participle (short)"
    GRND = "Gerund"
    NUMR = "Numeral"
    ADVB = "Adverb"
    NPRO = "Pronoun"
    PRED = "Predicative"
    PREP = "Preposition"
    CONJ = "Conjunction"
    PRCL = "Particle"
    INTJ = "Interjection"


class Word():
    def __init__(self, normal_form: str, part_of_speech: str, number_of_entries: int):
        self.normal_form = normal_form
        self.part_of_speech = part_of_speech
        self.number_of_entries = number_of_entries

    def __str__(self):
        return self.normal_form + '|' + self.part_of_speech + '|' + str(self.number_of_entries)

    def __repr__(self):
        return repr((self.normal_form, self.part_of_speech, self.number_of_entries))


def text_process(text: str):
    tokens = Tokenization.word_tokenize(text)
    morph = pymorphy2.MorphAnalyzer()
    tags = {}
    words = []

    for token in tokens:
        word = morph.parse(token)[0]
        normal_form = word.normal_form
        part_of_speech = get_part_of_speech(word.tag.POS)

        if normal_form not in tags.keys():
            tags[normal_form] = [1, part_of_speech]
        else:
            tags[normal_form][0] = tags[normal_form][0] + 1

    for key in tags.keys():
        words.append(Word(key, tags[key][1], tags[key][0]))

    return words


def bubble(array):
    for i in range(len(array)):
        for j in range(len(array) - i - 1):
            if array[j].number_of_entries < array[j + 1].number_of_entries:
                buff = array[j]
                array[j] = array[j + 1]
                array[j + 1] = buff


def get_part_of_speech(part_of_speech):
    if part_of_speech is None:
        return "Not defined"
    for current_part in Part_of_speech:
        if current_part.name == part_of_speech:
            return current_part.value
    return None


def check_input():
    FileUtils.write_to_file("input", " ", "w")
    if request.form.get("input_textarea") == '':
        uploaded_file = request.files['input_file']
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/input'))
    else:
        uploaded_file = request.files['input_file']
        argument = 'w'
        if uploaded_file.filename != '':
            uploaded_file.save(os.path.join('static/input'))
            argument = 'a'
            FileUtils.write_to_file("input", ' ', argument)
        input_text = request.form.get("input_textarea")
        FileUtils.write_to_file("input", input_text, argument)


@app.route('/')
def start():
    return render_template('start_page.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'GET':
        return render_template("result_page.html")

    check_input()
    text = FileUtils.read_from_file("input")
    words = text_process(text)
    bubble(words)

    return render_template('result_page.html', text=text, words=words)


@app.route('/about')
def about():
    return render_template("about_page.html")


if __name__ == '__main__':
    app.run()
