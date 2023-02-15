import requests

def getResponse():
  url_for_word_check_spelling = "https://agilec.cs.uh.edu/words"
  response = requests.get(url_for_word_check_spelling)
  
  if response.status_code != 200:
    raise RuntimeError("Network error")
  
  return response.text


def parseTextToListOfWords(text):
  listOfWords = text[1:-2].split(',')
  
  for index in range(0, len(listOfWords)):
    listOfWords[index] = listOfWords[index].strip()
  
  return listOfWords


def fetchWords():
  return parseTextToListOfWords(getResponse())
