from enum import Enum

import pymorphy2
from flask import Flask, request, render_template, redirect, url_for
from util import TokenizationUtils as Tokenization

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


def text_process(text: str):
    tokens = Tokenization.word_tokenize(text)
    morph = pymorphy2.MorphAnalyzer()
    tags = {}  # атрибуты каждого слова (начальная форма, часть речи, кол-во вхождений
    words = []  # массив с готовыми векторами

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


def get_part_of_speech(part_of_speech):
    if part_of_speech is None:
        return "Не определено"
    for current_part in Part_of_speech:
        if current_part.name == part_of_speech:
            return current_part.value
    return None


def check_input():
    pass


@app.route('/')
def start():
    text = "В наших лесах живут соловьи. Там часто звучат соловьиные трели. " \
           "Соловьи вьют гнезда на сучьях деревьев. Летом у соловьев появляются птенцы. " \
           "Малыши пищат. Они всегда голодны. Весь день летают родители и ищут пищу птенчикам. Осенью соловьи улетают на далекий юг."
    words = text_process(text)
    # return render_template('result_page.html', text=text, words=words)
    return render_template('index.html')


@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'GET':
        return render_template("result_page.html")
    text = None  # TODO get text from context and convert to str. Need to check input field or file input.
    words = text_process(text)
    return render_template('result_page.html', text=text, words=words)


@app.route('/about')
def about():  # TODO fill page
    return render_template("about.html")


if __name__ == '__main__':
    app.run()
