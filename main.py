import pygame
import random
import time
import sys

pygame.init()
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Cracker Barrel Game")

clock = pygame.time.Clock()

in_game = True

my_font = pygame.font.SysFont('Comic Sans MS', 40)

pegs = []

class Peg:

  def __init__(self, x, y, size, empty, border_color, border_width, selected, row, col, option, options):
    self.x = x
    self.y = y
    self.size = size
    self.empty = empty
    self.border_color = border_color
    self.border_width = border_width
    self.selected = selected
    self.row = row
    self.col = col
    self.option = option
    self.options = options

  def draw(self):
    if self.selected:
      self.border_color = (0, 255, 0)
    elif self.option:
      self.border_color = (255, 0, 0)
    else:
      self.border_color = (0, 0, 0)
    pygame.draw.rect(screen, self.border_color, [self.x, self.y, self.size, self.size], self.border_width)
    pygame.draw.rect(screen, (255, 255, 255), [self.x + self.border_width, self.y + self.border_width, self.size - self.border_width * 2, self.size -  self.border_width * 2])
    if self.empty == False:
      pygame.draw.circle(screen, (0, 0, 255), (round(self.x + self.size / 2), round(self.y + self.size / 2)), 10)
  
  def return_rect(self):
    return pygame.Rect(self.x, self.y, self.size, self.size)

def create_peg_board():
  count = 1
  y = 75
  for i in range(5):
    x = 250 - (count / 2) * 70
    for i in range(count):
      if count == 1:
        empty = True
      else:
        empty = False
      pegs.append(Peg(x, y, 70, empty, (0, 0, 0), 3, False, count - 1, i, False, []))
      x += 70
    count += 1
    y += 70

moves = {(0, 0):[[2, 0, 1, 0], [2, 2, 1, 1]], (1, 0):[[3, 0, 2, 0], [3, 2, 2, 1]], (1, 1):[[3, 1, 2, 1], [3, 3, 2, 2]],
(2, 0):[[4, 0, 3, 0], [4, 2, 3, 1], [0, 0, 1, 0], [2, 2, 2, 1]], (2, 1):[[4, 1, 3, 1], [4, 3, 3, 2]], (2, 2):[[4, 2, 3, 2], [4, 4, 3, 3], 
[0, 0, 1, 1], [2, 0, 2, 1]], (3, 0):[[1, 0, 2, 0], [3, 2, 3, 1]], (3, 1):[[1, 1, 2, 1], [3, 3, 3, 2]], (3, 2):[[1, 0, 2, 1], [3, 0, 3, 1]], 
(3, 3):[[1, 1, 2, 2], [3, 1, 3, 2]], (4, 0):[[2, 0, 3, 0], [4, 2, 4, 1]], (4, 1):[[2, 1, 3, 1], [4, 3, 4, 2]], (4, 2):[[2, 0, 3, 1], [2, 2, 3, 2], [4, 4, 4, 3], [4, 0, 4, 1]], 
(4, 3):[[2, 1, 3, 2], [4, 1, 4, 2]], (4, 4):[[2, 2, 3, 3], [4, 2, 4, 3]]}


selected = []

def find_options(row, col, pegged):
  global moves
  spots = moves[(row, col)]
  for i in spots:
    if find_peg(row, col).empty == False and find_peg(i[2], i[3]).empty == False and find_peg(i[0], i[1]).empty: 
      pegged.options.append(find_peg(i[0], i[1]))

def display_text(text, x, y, color):
  text = my_font.render(text, False, color)
  screen.blit(text, (x, y))

def find_peg(row, col):
  for peg in pegs:
    if row == peg.row and col == peg.col:
      return peg
      break

def remove_peg(peg):
  # this eliminates a peg from the board
  peg.empty = True
  full.remove(peg)

def check_mid_peg(row, col, er, ec):
  global moves
  for i in moves.keys():
    if i[0] == row and i[1] == col:
      for j in moves[(i[0], i[1])]:
        if j[0] == er and j[1] == ec:
          return find_peg(j[2], j[3])

def select(peg):
  peg.selected = True
  selected.append(peg)
  find_options(peg.row, peg.col, peg)

create_peg_board()

full = [peg for peg in pegs if peg.empty == False]

while in_game:
  screen.fill((0, 0, 0))

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      in_game = False
    if event.type == pygame.MOUSEBUTTONDOWN:
      mouse_pos = pygame.mouse.get_pos()
      chosen_peg = [peg for peg in pegs if peg.return_rect().collidepoint(mouse_pos)]
      if len(chosen_peg) > 0:
        if chosen_peg[0].selected == False:
          select(chosen_peg[0])
        elif chosen_peg[0].selected:
          chosen_peg[0].selected = False
          chosen_peg[0].options.clear()
          for i in selected[0].options:
            i.option = False
          selected.remove(chosen_peg[0])
          
  if len(selected) > 1:
    peg1 = selected[0]
    peg2 = selected[1]
    mid_peg = check_mid_peg(peg1.row, peg1.col, peg2.row, peg2.col)
    if peg1.empty == False and peg2 in peg1.options and peg2.empty:
      try:
        peg1.selected = False
        remove_peg(peg1)
        mid_peg = check_mid_peg(peg1.row, peg1.col, peg2.row, peg2.col)
        remove_peg(mid_peg)
        for op in peg1.options:
          op.option = False
        selected.remove(peg1)
        peg2.empty = False
        full.append(peg2)
      except:
        print("Choose another place.")
    else:
      peg1.selected = False
      for op in peg1.options:
        op.option = False
      selected.remove(peg1)

  for i in selected:
    for j in range(len(i.options)):
      if i.options[j].empty:
        i.options[j].option = True

  for peg in pegs:
    peg.draw()

  display_text("Cracker Barrel Game", 100, 25, (255, 255, 255))

  pygame.display.update()
  clock.tick(60)

pygame.quit()
quit()