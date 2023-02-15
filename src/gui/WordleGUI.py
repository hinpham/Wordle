import pygame
import numpy as np
import threading

import src.Wordle as Wordle
import src.AgileSpellChecker as ASP
import src.AgileWordService as AWS
from src.Wordle import Status as Status

pygame.init()

HEIGHT = 50
WIDTH = 50
ROWS = 6
COLUMNS = 5
MARGIN = 5
WINDOW_SIZE = (500, 500)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 50)
LIGHT_YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
SMALL_FONT = pygame.font.SysFont('Corbel', 35)
BASE_FONT = pygame.font.Font(None, 39)

TARGET = Wordle.getRandomWord(AWS.fetchWords)

class WordleGUI():
  def __init__(self):
    self.count = 1
    self.latch = threading.Condition()
    self.letter_counter = 0
    self.currentRowStatus = 0
    self.isGameOver = False
    self.words_storage = [''] * 6
    self.user_guess = ''
    self.message_displayed = SMALL_FONT.render('', True, RED)
    self.display_surface = pygame.display.set_mode(WINDOW_SIZE)
    self.display_surface.fill(BLACK)
    self.BUTTON = SMALL_FONT.render('GUESS', True, RED)
    self.GRID = self.makeGrid()

  def display(self, numOfAttempts, gameStatus, tallyResponse, gameMessage):
    if gameStatus == Status.ERROR:
      self.currentRowStatus = self.currentRowStatus - 1
      self.count = 1
      self.words_storage[numOfAttempts] = ""
      self.message_displayed = SMALL_FONT.render(gameMessage, True, RED)
      self.latch = threading.Condition()
      return
    
    if gameStatus == Status.WON:
      self.message_displayed = SMALL_FONT.render(gameMessage, True, YELLOW)
      self.isGameOver = True
    elif gameStatus == Status.LOST:
      self.message_displayed = SMALL_FONT.render(gameMessage, True, RED)
    else:
      self.message_displayed = SMALL_FONT.render("", True, BLACK)
    
    for index in range(0, len(tallyResponse)):
      self.GRID[numOfAttempts - 1][index] = tallyResponse[index].value
      
    self.count = 1
    self.latch = threading.Condition()

  def makeGrid(self):
    return np.array([[-1 for column in range(COLUMNS)] for row in range(ROWS)])

  def readGuess(self):
      self.latch.acquire()

      while self.count > 0:
        self.latch.wait()

      self.latch.release()

      return self.words_storage[self.currentRowStatus - 1]

  def filterColor(self, row, column, noColor):
    color = WHITE

    if noColor:
      return color
    
    if self.GRID[row][column] == 1:
      color = GREEN
    elif self.GRID[row][column] == 2:
      color = LIGHT_YELLOW
    elif self.GRID[row][column] == 0:
      color = GRAY

    return color

  def drawGrid(self, noColor = True):
    for row in range(ROWS):
      for column in range(COLUMNS):
        color = self.filterColor(row, column, noColor)
        pygame.draw.rect(self.display_surface,
                         color,
                         [(MARGIN + WIDTH) * column + MARGIN,
                          (MARGIN + HEIGHT) * row + MARGIN,
                          WIDTH,
                          HEIGHT])

        if len(self.words_storage[row]) != 0:
          self.display_surface.blit(BASE_FONT.render(self.words_storage[row][column], True, BLACK),
                          [(MARGIN + WIDTH) * column + MARGIN + 15,
                          (MARGIN + HEIGHT) * row + MARGIN + 15,
                          WIDTH,
                          HEIGHT])
        elif len(self.user_guess) > 0:
          self.updateRowByInput()

  def updateRowByInput(self):
    for currentRow in range(len(self.user_guess)):
      self.display_surface.blit(BASE_FONT.render(self.user_guess[currentRow], True, BLACK),
                                [(MARGIN + WIDTH) * currentRow + MARGIN + 15,
                                 (MARGIN + HEIGHT) * self.currentRowStatus + MARGIN + 15,
                                 WIDTH,
                                 HEIGHT])

  def isButtonClicked(self, mouse_coordinates):
    return True if ((327 <= mouse_coordinates[0] <= 427) and (48 <= mouse_coordinates[1] <= 80)) and self.isButtonEnabled() else False

  def updateButton(self):
    if self.letter_counter == 5:
      self.BUTTON = SMALL_FONT.render('GUESS', True, GREEN)
    else:
      self.BUTTON = SMALL_FONT.render('GUESS', True, RED)

  def isButtonEnabled(self):
    return True if self.letter_counter == 5 else False

  def reset(self):
    self.currentRowStatus += 1
    self.letter_counter = 0
    self.user_guess = ''

  def refresh(self):
    self.display_surface.fill(BLACK)
    self.display_surface.blit(self.BUTTON, (500 / 2 + 75, 50))
    self.drawGrid(False)
    self.display_surface.blit(self.message_displayed, (5, 380))
    pygame.display.flip()

  def updateIfValidInput(self, event):
    if event.key == pygame.K_BACKSPACE and len(self.user_guess) != 0:
      self.user_guess = self.user_guess[:-1]
      self.letter_counter -= 1
    elif len(self.user_guess) <= 4 and event.unicode.isalpha():
      self.user_guess += event.unicode.upper()
      self.letter_counter += 1

    self.drawGrid(True)

  def updateByKeyInput(self, event):
    if event.type == pygame.KEYDOWN and self.currentRowStatus < 6 and not self.isGameOver:
      self.updateIfValidInput(event)

  def updateIfButtonClicked(self, event):
    if (event.type == pygame.MOUSEBUTTONDOWN and self.isButtonClicked(pygame.mouse.get_pos())) and self.currentRowStatus < 6:
      self.words_storage[self.currentRowStatus] = self.user_guess
      pygame.display.flip()
      self.latch.acquire()
      self.count -= 1

      if self.count <= 0:
        self.latch.notifyAll()

      self.latch.release()
      self.reset()
    
def main():
  running = True

  while running:
    gui.updateButton()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
          
      gui.updateByKeyInput(event)
      gui.updateIfButtonClicked(event)

    gui.refresh()


gui = WordleGUI()
play_thread = threading.Thread(target=Wordle.play, args=(TARGET, gui.readGuess, gui.display, ASP.isSpellingCorrect))
play_thread.start()
main()
