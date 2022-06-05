from TokenizationUtils import sentence_tokenize, word_tokenize

if __name__ == '__main__':
    text = "к.т.н. — кандидат технических наук. "
    sentences = sentence_tokenize(text)
    print(sentences)
    words = word_tokenize(text)
    print(words)
