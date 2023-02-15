import requests

def getResponse(word):
    url_for_word_check_spelling = f"http://agilec.cs.uh.edu/spell?check={word}"
    response = requests.get(url_for_word_check_spelling)

    if response.status_code != 200:
        raise RuntimeError("Network error")

    return response.text


def parse(text):
    return text == "true"


def isSpellingCorrect(word):
    return parse(getResponse(word))
