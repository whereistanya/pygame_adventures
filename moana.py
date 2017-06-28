#!/usr/bin/python3
"""An extremely pointless game to learn pygame with."""

import os
import pygame
import random


class LostThings:
  """Objects to be found on the grid."""

  def __init__(self, image, count, drawer):
    """Set up the icons that wait to be found.

    Args:
      image: (pygame.Surface) a loaded image.
      count: (int) how many things to put on the screen in random places.
      drawer: (Drawer) an initialised Drawer to display images.
    """
    self.things = set()   # Set of (x, y) tuples, indexed by grid pos, not pixels
    self.drawer = drawer
    self.image = image
    # Choose positions for the objects.
    while count > 0:
      pos = self.drawer.random_square()
      if pos in self.things:
        continue  # Don't reuse a square
      self.things.add(pos)
      count -= 1

  def count(self):
    """Return how many things there are."""
    return len(self.things)

  def is_at(self, pos):
    """Return whether one of the things is at this position.

    Args:
      pos: ((int, int)): tuple showing x, y position.
    """
    if pos in self.things:
      return True
    return False

  def draw(self):
    """Instruct the drawer to put the things on the screen."""
    for (x, y) in self.things:
      self.drawer.draw(self.image, x, y)

  def delete(self, pos):
    """Remove the thing at some position.

    Args:
      pos: ((int, int)): tuple showing x, y position.
    """

    self.things.remove(pos)


class ThingFinder:
  """The icon that moves around, finding the things."""
  def __init__(self, image, drawer):
    """Set up the icon that moves to find things.

    Args:
      image: (pygame.Surface) a loaded image
      drawer: (Drawer) an initialised Drawer to display images
    """
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
    if self.drawer.in_bounds(self.x, self.y - 1):
      self.y -= 1

  def move_down(self):
    if self.drawer.in_bounds(self.x, self.y + 1):
      self.y += 1

  def move_left(self):
    if self.drawer.in_bounds(self.x - 1, self.y):
      self.x -= 1

  def move_right(self):
    if self.drawer.in_bounds(self.x + 1, self.y):
      self.x += 1


class Drawer:
  """The class that does the drawing!"""
  def __init__(self, size, max_x, max_y, initial_text):
    """Set up the game screen.

    Args:
      size: (int) size of each square.
      max_x, max_y: (int) how many squares in each direction.
      initial_text: (String) text to display in the center of the screen.
    """
    self.screen = pygame.display.set_mode((max_x * size, max_y * size))
    self.background = (0, 0, 0)  # rgb (black)
    font = pygame.font.SysFont("verdana", 36)
    self.center_text = font.render(initial_text, True, (255, 255, 255))
    self.occupied = set()
    self.size = size
    self.max_x = max_x         # How many squares across.
    self.max_y = max_y         # How many qsuares down.

  def set_background(self, rgb):
    """Set the background color.
    Args:
      rgb: (short, short, short) tuple of 0-255 values for red, green, blue.
    """
    self.background = rgb

  def fill(self):
    """Completely fill the screen with the background color and any messages."""
    self.occupied.clear()
    self.screen.fill(self.background)
    if self.center_text:
      self.screen.blit(self.center_text,
                       ((self.max_x * self.size - self.center_text.get_width()) / 2,
                        (self.max_y * self.size - self.center_text.get_height()) / 2))


  def draw(self, image, x, y):
    """Put an image on the screen at some location.

    Args:
      image: (pygame.Surface) Already-loaded image to draw.
      x, y: (int) Grid position, in squares.
    """
    pos_x = self.pixels(x)
    pos_y = self.pixels(y)
    self.screen.blit(image, (pos_x, pos_y))
    self.occupied.add((pos_x, pos_y))

  def pixels(self, index):
     """Take a grid square and returns coords of its top left hand corner.

     Args:
      index: (int) How many squares across or down.
     Returns:
      (int) How many pixels.
     """
     return index * self.size

  def in_bounds(self, x, y):
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

  def win(self):
    """Set a winning message for winners."""
    self.set_background((0, 255, 0))  # green
    font = pygame.font.SysFont("verdana", 36)
    self.center_text = font.render("Hurray! Press y to play again.", True, (255, 255, 255))

  def random_square(self, avoid_occupied=True):
    """Return a random square, optionally one without anything in it."""
    while True:
      x = random.randint(0, self.max_x -1)
      y = random.randint(0, self.max_y -1)
      if avoid_occupied and (x, y) in self.occupied:
        # there's already a thing there; try again
        continue
      return (x, y)

class AmazingMoanaGame:
  """OMG IT IS SO AMAZING."""

  def __init__(self, square_size=64, max_x=15, max_y=7, count=5,
               moana_image="images/babymoana.jpg",
               shells_image="images/shell.png"):
    """Set up the screen.

    Args:
      square_size: (int) the size of each grid square. The images on the grid
                   should be square and should be this size or it'll look like a mess.
      max_x, max_y: (int) how many squares on each side of the grid.
      count: (int) how many lost things to put on the grid
      moana_image: (string) filename of the image that moves around finding things.
      shells_image: (string) filename of the image that gets found
    """
    pygame.init()
    self.clock = pygame.time.Clock()
    self.image_lib = {}
    self.done = False
    self.drawer = Drawer(square_size, max_x, max_y, "Find all the shells!")
    self.moana = ThingFinder(self.get_image(moana_image), self.drawer)
    self.shells = LostThings(self.get_image(shells_image), count, self.drawer)
    self.drawer.set_background((0, 0, 255))  # blue

  def run(self):
    """The main game loop. Draw stuff and look for events."""
    while not self.done:
      self.drawer.fill()
      self.check_events()
      self.shells.draw()
      self.moana.draw()
      if self.shells.is_at(self.moana.pos()):
        self.shells.delete(self.moana.pos())
        if self.shells.count() == 0:
          pygame.mixer.music.load("sounds/ididit.wav")
          pygame.mixer.music.play()
          self.drawer.win()

      pygame.display.flip()
      self.clock.tick(60)

  def check_events(self):
    """Check for keypresses and take actions based on them."""
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
      if pressed[pygame.K_y]:
        # start the game again
        self.__init__()

  def get_image(self, filename):
    """Pull an image from disk and cache it.

    Args:
      filename: (str) local path to image file on disk.
    Returns:
      (pygame.Surface) blittable image.
    """
    image = self.image_lib.get(filename)
    if image == None:
      image = pygame.image.load(filename)
    return image


# Main.
game = AmazingMoanaGame()
game.run()
