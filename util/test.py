from TokenizationUtils import sentence_tokenize, word_tokenize

if __name__ == '__main__':
    text = "к.т.н. — канDSдидат3 технsических н2аук. по-моему"
    sentences = sentence_tokenize(text)
    print(sentences)
    words = word_tokenize(text)
    print(words)
