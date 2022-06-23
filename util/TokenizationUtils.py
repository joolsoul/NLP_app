patterns = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#№$;%:&^*\"\'(),/<>{}[]\\|—_=+"


def sentence_tokenize(text: str):
    sentences = []
    current_sentence = ''
    for index in range(len(text)):
        char = text[index]
        if char == '.' or char == '!' or char == '?' and index != len(text) - 1:
            if check_upper_case(text[index + 1:]):
                sentences.append(current_sentence)
                current_sentence = ''
            else:
                current_sentence = current_sentence + char
        else:
            if char == ' ' and len(current_sentence) == 0:
                continue
            else:
                current_sentence = current_sentence + char

    sentences.append(current_sentence)
    return sentences


def check_upper_case(sentence):
    for char in sentence:
        if char == ' ':
            continue
        if char.isupper():
            return True
        return False


def word_tokenize(text: str):
    words = text.split(' ')
    remove_patterns(words)
    remove_empty_values_from_list(words, '')
    return words


def remove_empty_values_from_list(input_list, value):
    indexes = []
    for index in range(len(input_list)):
        if input_list[index] == value:
            indexes.append(index)
    for index_to_remove in indexes:
        input_list.pop(index_to_remove)


def remove_patterns(words: list):
    remove_empty_values_from_list(words, '')
    for index in range(len(words)):
        word = words[index]
        if word[-1] == '.':
            if index == len(words) - 1:
                word = remove_char(word, len(word) - 1)
            else:
                if words[index + 1][0].isupper():
                    word = remove_char(word, len(word) - 1)
        for char in word:
            if char in patterns:
                word = word.replace(char, '')

        words[index] = word


def remove_char(word, index):
    new_word = ''
    for i in range(len(word)):
        if i != index:
            new_word = new_word + word[i]
    return new_word
