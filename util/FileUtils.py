def read_from_file(file_name):
    with open("static/" + file_name, encoding='utf-8') as file:
        text = file.read()
    return text


def write_to_file(file_name, text, argument):
    with open("static/" + file_name, argument, encoding='utf-8') as file:
        for element in text:
            file.write(element)
