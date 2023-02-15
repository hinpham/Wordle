import unittest

from src import Wordle as Wordle
from src.Wordle import Match
from src.Wordle import Status


class WordleTest(unittest.TestCase):

  def test_canary(self):
    self.assertTrue(True)

  def test_tally(self):
   test_sample = [
     ["FAVOR", "FAVOR", [Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT]],
     ["FAVOR", "TESTS", [Match.NONE, Match.NONE, Match.NONE, Match.NONE, Match.NONE]],
     ["FAVOR", "RAPID", [Match.WRONG_POSITION, Match.EXACT, Match.NONE, Match.NONE, Match.NONE]],
     ["FAVOR", "MAYOR", [Match.NONE, Match.EXACT, Match.NONE, Match.EXACT, Match.EXACT]],
     ["FAVOR", "RIVER", [Match.NONE, Match.NONE, Match.EXACT, Match.NONE, Match.EXACT]],
     ["FAVOR", "AMAST", [Match.WRONG_POSITION, Match.NONE, Match.NONE, Match.NONE, Match.NONE]],
     ["SKILL", "SKILL", [Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT]],
     ["SKILL", "SWIRL", [Match.EXACT, Match.NONE, Match.EXACT, Match.NONE, Match.EXACT]],
     ["SKILL", "CIVIL", [Match.NONE, Match.WRONG_POSITION, Match.NONE, Match.NONE, Match.EXACT]],
     ["SKILL", "SHIMS", [Match.EXACT, Match.NONE, Match.EXACT, Match.NONE, Match.NONE]],
     ["SKILL", "SILLY", [Match.EXACT, Match.WRONG_POSITION, Match.WRONG_POSITION, Match.EXACT, Match.NONE]],
     ["SKILL", "SLICE", [Match.EXACT, Match.WRONG_POSITION, Match.EXACT, Match.NONE, Match.NONE]],
     ["SAGAS", "ABASE", [Match.WRONG_POSITION, Match.NONE, Match.WRONG_POSITION, Match.WRONG_POSITION, Match.NONE]],
   ]

   for target, guess, expected_response in test_sample:
     with self.subTest(msg = f"tally if guess {guess} matches target {target}"):
       self.assertEqual(expected_response, Wordle.tally(guess, target))

  def test_invalid_guess(self):
    test_sample = [
      ["FAVOR", "FOR"],
      ["FAVOR", "FERVER"],
    ]
    
    for target, guess in test_sample:
      with self.subTest(msg = f"tally if guess {guess} matches target {target}"):
        with self.assertRaisesRegex(Exception, 'INVALID GUESS'):
          Wordle.tally(guess, target)


  def test_play(self):
    def readGuess():
      return "FAVOR"

    display_called = False

    def display(numOfAttempts, gameStatus, tallyResponse, message):
      if numOfAttempts < 2:
        self.assertEqual(numOfAttempts, 1)
        self.assertEqual(gameStatus, Status.WON)
        self.assertEqual(tallyResponse, [Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT])
        self.assertEqual(message, "AMAZING!")
        nonlocal display_called
        display_called = True

    Wordle.play("FAVOR", readGuess, display)
    
    self.assertTrue(display_called)

  def test_play_with_invalid_guess_first_attempt(self):
    def readGuess():
      return "FOR"
    
    with self.assertRaisesRegex(Exception, "INVALID GUESS"):
      Wordle.play("FAVOR", readGuess, None)

  def test_play_with_non_winning_guess_first_attempt(self):
    def readGuess():
      return "AMAST"

    display_called = False

    def display(numOfAttempts, gameStatus, tallyResponse, message):
      if numOfAttempts == 1:
        self.assertEqual(numOfAttempts, 1)
        self.assertEqual(gameStatus, Status.TRY_AGAIN)
        self.assertEqual(tallyResponse, [Match.WRONG_POSITION, Match.NONE, Match.NONE, Match.NONE, Match.NONE])
        self.assertEqual(message, "")
        nonlocal display_called
        display_called = True

    Wordle.play("FAVOR", readGuess, display)
    
    self.assertTrue(display_called)

  def test_play_with_winning_guess_second_attempt(self):
    display_call_count = 0
    guesses = ["FAVOR", "AMAST"]
    expectedResponse = [
      [Status.WON, 2, [Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT], "SPLENDID!"],
      [Status.TRY_AGAIN, 1, [Match.WRONG_POSITION, Match.NONE, Match.NONE, Match.NONE, Match.NONE], ""],
    ]

    def readGuess():
      return guesses.pop()

    def display(numOfAttempts, gameStatus, tallyResponse, gameMessage):
      if numOfAttempts < 3:
        status, attempt, response, message = expectedResponse.pop()
        self.assertEqual(numOfAttempts, attempt)
        self.assertEqual(gameStatus, status)
        self.assertEqual(tallyResponse, response)
        self.assertEqual(gameMessage, message)
        nonlocal display_call_count
        display_call_count += 1

    Wordle.play("FAVOR", readGuess, display)
    
    self.assertEqual(2, display_call_count)

  def test_play_with_no_winning_guess_second_attempt(self):
    display_call_count = 0
    expectedResponse = [
      [Status.TRY_AGAIN, 2, [Match.NONE, Match.NONE, Match.EXACT, Match.NONE, Match.EXACT], ""],
      [Status.TRY_AGAIN, 1, [Match.NONE, Match.NONE, Match.EXACT, Match.NONE, Match.EXACT], ""],
    ]

    def readGuess():
      return "RIVER"

    def display(numOfAttempts, gameStatus, tallyResponse, gameMessage):
      if numOfAttempts < 3:
        status, attempt, response, message = expectedResponse.pop()
        self.assertEqual(numOfAttempts, attempt)
        self.assertEqual(gameStatus, status)
        self.assertEqual(tallyResponse, response)
        self.assertEqual(gameMessage, message)
        nonlocal display_call_count
        display_call_count += 1

    Wordle.play("FAVOR", readGuess, display)
    
    self.assertEqual(2, display_call_count)

  def test_play_with_winning_guess_third_attempt(self):
    display_call_count = 0
    guesses = ["FAVOR", "AMAST", "RIVER"]
    expectedResponse = [
      [Status.WON, 3, [Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT], "AWESOME!"],
      [Status.TRY_AGAIN, 2, [Match.WRONG_POSITION, Match.NONE, Match.NONE, Match.NONE, Match.NONE], ""],
      [Status.TRY_AGAIN, 1, [Match.NONE, Match.NONE, Match.EXACT, Match.NONE, Match.EXACT], ""]
    ]

    def readGuess():
      return guesses.pop()

    def display(numOfAttempts, gameStatus, tallyResponse, gameMessage):
      status, attempt, response, message = expectedResponse.pop()
      self.assertEqual(numOfAttempts, attempt)
      self.assertEqual(gameStatus, status)
      self.assertEqual(tallyResponse, response)
      self.assertEqual(gameMessage, message)
      nonlocal display_call_count
      display_call_count += 1

    Wordle.play("FAVOR", readGuess, display)
    
    self.assertEqual(3, display_call_count)

  def test_play_with_winning_guess_fourth_attempt(self):
    display_call_count = 0
    guesses = ["FAVOR", "AMAST", "RIVER", "RAPID"]
    expectedResponse = [
      [Status.WON, 4, [Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT], "YAY!!!"],
      [Status.TRY_AGAIN, 3, [Match.WRONG_POSITION, Match.NONE, Match.NONE, Match.NONE, Match.NONE], ""],
      [Status.TRY_AGAIN, 2, [Match.NONE, Match.NONE, Match.EXACT, Match.NONE, Match.EXACT], ""],
      [Status.TRY_AGAIN, 1, [Match.WRONG_POSITION, Match.EXACT, Match.NONE, Match.NONE, Match.NONE], ""]
    ]

    def readGuess():
      return guesses.pop()

    def display(numOfAttempts, gameStatus, tallyResponse, gameMessage):
      status, attempt, response, message = expectedResponse.pop()
      self.assertEqual(numOfAttempts, attempt)
      self.assertEqual(gameStatus, status)
      self.assertEqual(tallyResponse, response)
      self.assertEqual(gameMessage, message)
      nonlocal display_call_count
      display_call_count += 1

    Wordle.play("FAVOR", readGuess, display)
    
    self.assertEqual(4, display_call_count)

  def test_play_with_winning_guess_fifth_attempt(self):
    display_call_count = 0
    guesses = ["FAVOR", "AMAST", "RIVER", "RAPID", "MAYOR"]
    expectedResponse = [
      [Status.WON, 5, [Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT], "YAY!!"],
      [Status.TRY_AGAIN, 4, [Match.WRONG_POSITION, Match.NONE, Match.NONE, Match.NONE, Match.NONE], ""],
      [Status.TRY_AGAIN, 3, [Match.NONE, Match.NONE, Match.EXACT, Match.NONE, Match.EXACT], ""],
      [Status.TRY_AGAIN, 2, [Match.WRONG_POSITION, Match.EXACT, Match.NONE, Match.NONE, Match.NONE], ""],
      [Status.TRY_AGAIN, 1, [Match.NONE, Match.EXACT, Match.NONE, Match.EXACT, Match.EXACT], ""]
    ]

    def readGuess():
      return guesses.pop()

    def display(numOfAttempts, gameStatus, tallyResponse, gameMessage):
      status, attempt, response, message = expectedResponse.pop()
      self.assertEqual(numOfAttempts, attempt)
      self.assertEqual(gameStatus, status)
      self.assertEqual(tallyResponse, response)
      self.assertEqual(gameMessage, message)
      nonlocal display_call_count
      display_call_count += 1

    Wordle.play("FAVOR", readGuess, display)
    
    self.assertEqual(5, display_call_count)

  def test_play_with_winning_guess_sixth_attempt(self):
    display_call_count = 0
    guesses = ["FAVOR", "AMAST", "RIVER", "RAPID", "MAYOR", "MAYOR"]
    expectedResponse = [
      [Status.WON, 6, [Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT], "YAY!"],
      [Status.TRY_AGAIN, 5, [Match.WRONG_POSITION, Match.NONE, Match.NONE, Match.NONE, Match.NONE], ""],
      [Status.TRY_AGAIN, 4, [Match.NONE, Match.NONE, Match.EXACT, Match.NONE, Match.EXACT], ""],
      [Status.TRY_AGAIN, 3, [Match.WRONG_POSITION, Match.EXACT, Match.NONE, Match.NONE, Match.NONE], ""],
      [Status.TRY_AGAIN, 2, [Match.NONE, Match.EXACT, Match.NONE, Match.EXACT, Match.EXACT], ""],
      [Status.TRY_AGAIN, 1, [Match.NONE, Match.EXACT, Match.NONE, Match.EXACT, Match.EXACT], ""]
    ]

    def readGuess():
      return guesses.pop()

    def display(numOfAttempts, gameStatus, tallyResponse, gameMessage):
      status, attempt, response, message = expectedResponse.pop()
      self.assertEqual(numOfAttempts, attempt)
      self.assertEqual(gameStatus, status)
      self.assertEqual(tallyResponse, response)
      self.assertEqual(gameMessage, message)
      nonlocal display_call_count
      display_call_count += 1

    Wordle.play("FAVOR", readGuess, display)
    
    self.assertEqual(6, display_call_count)

  def test_play_with_non_winning_guess_sixth_attempt(self):
    read_guess_call_count = 0
    display_call_count = 0
    guesses = ["AMAST", "AMAST", "RIVER", "RAPID", "MAYOR", "MAYOR"]
    expectedResponse = [
      [Status.LOST, 6, [Match.WRONG_POSITION, Match.NONE, Match.NONE, Match.NONE, Match.NONE], "It was FAVOR, better luck next time"],
      [Status.TRY_AGAIN, 5, [Match.WRONG_POSITION, Match.NONE, Match.NONE, Match.NONE, Match.NONE], ""],
      [Status.TRY_AGAIN, 4, [Match.NONE, Match.NONE, Match.EXACT, Match.NONE, Match.EXACT], ""],
      [Status.TRY_AGAIN, 3, [Match.WRONG_POSITION, Match.EXACT, Match.NONE, Match.NONE, Match.NONE], ""],
      [Status.TRY_AGAIN, 2, [Match.NONE, Match.EXACT, Match.NONE, Match.EXACT, Match.EXACT], ""],
      [Status.TRY_AGAIN, 1, [Match.NONE, Match.EXACT, Match.NONE, Match.EXACT, Match.EXACT], ""]
    ]

    def readGuess():
      nonlocal read_guess_call_count
      read_guess_call_count += 1
      return guesses.pop()

    def display(numOfAttempts, gameStatus, tallyResponse, gameMessage):
      status, attempt, response, message = expectedResponse.pop()
      self.assertEqual(numOfAttempts, attempt)
      self.assertEqual(gameStatus, status)
      self.assertEqual(tallyResponse, response)
      self.assertEqual(gameMessage, message)
      nonlocal display_call_count
      display_call_count += 1

    Wordle.play("FAVOR", readGuess, display)
    
    self.assertEqual(6, display_call_count)
    self.assertEqual(6, read_guess_call_count)

  def test_readGuess_not_called_after_second_attempt_winning_guess(self):
    read_guess_call_count = 0
    guesses = ["FAVOR", "AMAST"]

    def readGuess():
      nonlocal read_guess_call_count
      read_guess_call_count += 1
      return guesses.pop()

    def display(numOfAttempts, gameStatus, tallyResponse, gameMessage):
      return

    Wordle.play("FAVOR", readGuess, display)
    
    self.assertEqual(2, read_guess_call_count)

  def test_readGuess_not_called_after_sixth_attempt_non_winning_guess(self):
    read_guess_call_count = 0

    def readGuess():
      nonlocal read_guess_call_count
      read_guess_call_count += 1
      return "HELLO"

    def display(numOfAttempts, gameStatus, tallyResponse, gameMessage):
      return

    Wordle.play("FAVOR", readGuess, display)
    
    self.assertEqual(6, read_guess_call_count)

  def test_guess_not_a_word_first_attempt(self):
    guesses = ["FAVOR", "FAVRO"]
    spellChecks = [True, False]

    def readGuess():
      return guesses.pop()

    def isGuessCorrect():
      return spellChecks.pop()

    display_called = False

    def display(numOfAttempts, gameStatus, tallyResponse, message):
      if numOfAttempts == 0:
        self.assertEqual(numOfAttempts, 0)
        self.assertEqual(gameStatus, Status.ERROR)
        self.assertEqual(tallyResponse, None)
        self.assertEqual(message, "not a word")
        nonlocal display_called
        display_called = True

    Wordle.play("FAVOR", readGuess, display, lambda word: isGuessCorrect())
    
    self.assertTrue(display_called)

  def test_guess_not_a_word_second_attempt(self):
    guesses = ["FAVOR", "FVROA"]
    spellChecks = [True, False]
    expectedResponse = [
      [Status.WON, 1, [Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT], "AMAZING!"],
      [Status.ERROR, 0, None, "not a word"]
    ]

    def readGuess():
      return guesses.pop()

    def isGuessCorrect():
      return spellChecks.pop()
      
    display_called = False

    def display(numOfAttempts, gameStatus, tallyResponse, gameMessage):
      if numOfAttempts < 2:
        status, attempt, response, message = expectedResponse.pop()
        self.assertEqual(numOfAttempts, attempt)
        self.assertEqual(gameStatus, status)
        self.assertEqual(tallyResponse, response)
        self.assertEqual(gameMessage, message)
        nonlocal display_called
        display_called = True

    Wordle.play("FAVOR", readGuess, display, lambda word: isGuessCorrect())

    self.assertTrue(display_called)

  def test_guess_not_a_word_second_attempt_but_good_on_third(self):
    guesses = ["FAVOR", "FVROA", "TESTS"]
    spellChecks = [True, False, True]
    expectedResponse = [
      [Status.WON, 2, [Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT, Match.EXACT], "SPLENDID!"],
      [Status.ERROR, 1, None, "not a word"],
      [Status.TRY_AGAIN, 1, [Match.NONE, Match.NONE, Match.NONE, Match.NONE, Match.NONE], ""],
    ]

    def readGuess():
      return guesses.pop()

    def isGuessCorrect():
      return spellChecks.pop()
      
    display_called = False

    def display(numOfAttempts, gameStatus, tallyResponse, gameMessage):
      status, attempt, response, message = expectedResponse.pop()
      self.assertEqual(numOfAttempts, attempt)
      self.assertEqual(gameStatus, status)
      self.assertEqual(tallyResponse, response)
      self.assertEqual(gameMessage, message)
      nonlocal display_called
      display_called = True

    Wordle.play("FAVOR", readGuess, display, lambda word: isGuessCorrect())

    self.assertTrue(display_called)

  def test_guess_not_a_word_first_attempt_throws_exception(self):
    def readGuess():
      return "FAVRO"

    def isGuessCorrect(word):
      raise RuntimeError("Network error")

    display_called = False

    def display(numOfAttempts, gameStatus, tallyResponse, gameMessage):
      self.assertEqual(numOfAttempts, 0)
      self.assertEqual(gameStatus, Status.ERROR)
      self.assertEqual(tallyResponse, None)
      self.assertEqual(gameMessage, "Network error")
      nonlocal display_called
      display_called = True

    Wordle.play("FAVOR", readGuess, display, isGuessCorrect)

    self.assertTrue(display_called)

  def test_getRandomWord_gets_a_word_from_the_wordListService(self):
    def wordListService():
      return ['FAVOR', 'RIVER', 'MAYOR', 'RAPID']
    
    word = Wordle.getRandomWord(wordListService)
    
    self.assertIn(word, wordListService())
    
  def test_call_getRandomWord_twice_and_verify_the_words_returned_are_different(self):
    def wordListService():
      return  ['FAVOR', 'RIGOR', 'SUGAR', 'POWER', 'POINT', 'PIOUS', 'GRIND', 'NASTY', 'WATER', 'AVOID', 'PAINT', 'ABBEY', 'SHIRE', 'CYCLE', 'SHORT', 'WHICH', 'YIELD', 'AGILE', 'BUILD', 'BRICK']
    
    wordOne = Wordle.getRandomWord(lambda: wordListService())
    wordTwo = Wordle.getRandomWord(lambda: wordListService())
    
    self.assertNotEqual(wordOne, wordTwo)

  def test_getRandomWord_passes_the_network_error_exception_it_receives_from_the_service(self):
    def wordListService():
      raise RuntimeError("Network error")
    
    with self.assertRaisesRegex(RuntimeError, "Network error"):
      Wordle.getRandomWord(lambda: wordListService())


if __name__ == 'main':
  unittest.main()
