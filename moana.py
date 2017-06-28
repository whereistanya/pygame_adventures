"""An extremely pointless game to learn pygame with."""
#!/usr/bin/python3

import os
import pygame
import random


class LostThings:
  """Objects to be found on the grid."""

  def __init__(self, image, drawer):
    self.things = set()   # Set of (x, y) tuples, indexed by grid pos, not pixels
    self.drawer = drawer
    self.image = image

  def count(self):
    """Return how many things there are."""
    return len(self.things)

  def place(self, count, max_x, max_y):
    while count > 0:
      x = random.randint(0, max_x -1)
      y = random.randint(0, max_y -1)
      if (x, y) in self.things:
        # there's already a thing there; try again
        continue
      self.things.add((x, y))
      count -= 1

  def is_at(self, pos):
    if pos in self.things:
      return True
    return False

  def draw(self):
    for (x, y) in self.things:
      self.drawer.draw(self.image, x, y)

  def delete(self, pos):
    self.things.remove(pos)


class ThingFinder:
  """The icon that moves around, finding the things."""
  def __init__(self, image, drawer):
    self.image = image
    self.drawer = drawer
    self.x = 0
    self.y = 0

  def pos(self):
    """Return current location.

    Returns:
      (int, int): tuple of x, y co-ordinates.
    """
    return (self.x, self.y)

  def draw(self):
    """Instruct the drawer to draw this thing at some location."""
    self.drawer.draw(self.image, self.x, self.y)

  def move_up(self):
    if self.drawer.inbounds(self.x, self.y - 1):
      self.y -= 1

  def move_down(self):
    if self.drawer.inbounds(self.x, self.y + 1):
      self.y += 1

  def move_left(self):
    if self.drawer.inbounds(self.x - 1, self.y):
      self.x -= 1

  def move_right(self):
    if self.drawer.inbounds(self.x + 1, self.y):
      self.x += 1


class Drawer:
  """The class that does the drawing!"""
  def __init__(self, size, max_x, max_y):
    self.size = size
    self.max_x = max_x         # How many squares across.
    self.max_y = max_y         # How many qsuares down.
    self.screen = pygame.display.set_mode((max_x * size, max_y * size))
    self.background = (0, 0, 0)  # rgb (black)

  def set_background(self, rgb):
    """Set the background color.
    Args:
      rgb: (short, short, short) tuple of 0-255 values for red, green, blue.
    """
    self.background = rgb

  def fill(self):
    """Completely fill the screen with the background color."""
    self.screen.fill(self.background)

  def draw(self, image, x, y):
    """Put an image on the screen at some location.
    
    Args:
      image: (pygame.Surface) Already-loaded image to draw.
      x, y: (int) Grid position, in squares.
    """
    self.screen.blit(image, (self.pixels(x), self.pixels(y)))

  def pixels(self, index):
     """Take a grid square and returns coords of its top left hand corner.

     Args:
      index: (int) How many squares across or down.
     Returns:
      (int) How many pixels.
     """
     return index * self.size

  def inbounds(self, x, y):
    """Return whether the coordinates are inside the screen dimensions.
    Args:
      x, y: (int) index of squares on grid.
    Returns:
      (bool) Whether the location is inside the bounds of the grid.
    """
    if x < 0 or y < 0:
      return False
    if x >= self.max_x or y >= self.max_y:
      return False
    return True


class AmazingGame:
  """OMG IT IS SO AMAZING."""

  def __init__(self, size, max_x, max_y, count):
    pygame.init()
    self.clock = pygame.time.Clock()
    self.image_lib = {}
    self.done = False
    self.drawer = Drawer(size, max_x, max_y)
    self.moana = ThingFinder(self.get_image('babymoana.jpg'), self.drawer)
    self.shells = LostThings(self.get_image('shell.png'), self.drawer)
    self.shells.place(count, max_x, max_y)
    self.drawer.set_background((0, 0, 255))  # bluw

  def run(self):
    while not self.done:
      self.drawer.fill()
      self.check_events()
      self.shells.draw()
      self.moana.draw()
      if self.shells.is_at(self.moana.pos()):
        self.shells.delete(self.moana.pos())
        print("Hurray!")
        if self.shells.count() == 0:
          print( "I did it!") 
          self.drawer.set_background((0, 255, 0))  # green
          pygame.mixer.music.load("sounds/ididit.wav")
          pygame.mixer.music.play()
      pygame.display.flip()
      self.clock.tick(60)

  def get_image(self, filename):
    image = self.image_lib.get(filename)
    if image == None:
      image = pygame.image.load("images/%s" % filename)
    return image

  def check_events(self):
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.done = True
      pressed = pygame.key.get_pressed()
      if pressed[pygame.K_UP]:
        self.moana.move_up()
      if pressed[pygame.K_DOWN]:
        self.moana.move_down()
      if pressed[pygame.K_LEFT]:
        self.moana.move_left()
      if pressed[pygame.K_RIGHT]:
        self.moana.move_right()
      if pressed[pygame.K_ESCAPE]:
        self.done = True

# Main.
# 64 pixels, 15 squares across, 7 squares down, 10 shells
game = AmazingGame(64, 15, 7, 10)
game.run()
