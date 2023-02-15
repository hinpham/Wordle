from enum import Enum
import random

class Match(Enum):
    NONE = 0
    EXACT = 1
    WRONG_POSITION = 2

class Status(Enum):
    WON = 0
    LOST = 1
    TRY_AGAIN = 2
    ERROR = 3

WORD_SIZE = 5
MAX_TRIES = 6
MIN_TRIES = 1

def exactMatchOccurences(guess, target, letter):
    return sum(list(map(lambda letterInGuess, letterInTarget: 1 if (letterInGuess == letter and letterInTarget == letter) else 0, guess, target)))

def letterOccurrencesUntilPosition(position, word, letter):
    return sum(list(map(lambda letterInWord: 1 if (letter == letterInWord) else 0, word))[:position + 1])

def tallyForPosition(guess, target, position):
    if guess[position] == target[position]:
        return Match.EXACT
    
    theLetter = guess[position]
    nonExactOccurencesInTarget = letterOccurrencesUntilPosition(WORD_SIZE, target, theLetter) - exactMatchOccurences(guess, target, theLetter)
    
    return Match.WRONG_POSITION if (nonExactOccurencesInTarget >= letterOccurrencesUntilPosition(position, guess, theLetter)) else Match.NONE

def verifyGuessLength(guess):
    if len(guess) != WORD_SIZE:
        raise Exception("INVALID GUESS")

def tally(guess, target):
    verifyGuessLength(guess)

    return (list(map(lambda currentPosition: tallyForPosition(guess, target, currentPosition), list(range(0, 5)))))

def getMessage(attempt, status, target):
    messages = ['AMAZING!', 'SPLENDID!', 'AWESOME!', 'YAY!!!', 'YAY!!', 'YAY!']

    if status == Status.WON:
       return messages[attempt - 1]

    return f"It was {target}, better luck next time" if status == Status.LOST else ""
    
def determineStatus(attempts, matches):
    if matches == [Match.EXACT] * WORD_SIZE:
       return Status.WON

    return Status.LOST if attempts == MAX_TRIES else Status.TRY_AGAIN

def statusContinue(status, messageContinue, attempts):
    return (status == Status.TRY_AGAIN or Status == Status.ERROR) or (status == Status.ERROR and messageContinue) and attempts <= MAX_TRIES

def play(target, readGuess, display, isSpellingCorrect=lambda word: True):
   attempts = 0
   status = Status.TRY_AGAIN
   messageContinue = True

   while statusContinue(status, messageContinue, attempts):
       guess = readGuess()

       try:
           if isSpellingCorrect(guess):
               attempts = attempts + 1
               result = tally(guess, target)
               status = determineStatus(attempts, result)
               message = getMessage(attempts, status, target)
           else:
               result = None
               status = Status.ERROR
               message = "not a word"

       except RuntimeError as networkError:
           result = None
           status = Status.ERROR
           message = str(networkError)
           messageContinue = False

       display(attempts, status, result, message)


def getRandomWord(wordListService):
    return random.choice(wordListService())
