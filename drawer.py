#!/usr/bin/python3

import pygame
import random

class Drawer(object):
  """The class that does the drawing!"""
  def __init__(self, size, max_x, max_y):
    """Set up the game screen.

    Args:
      size: (int) size of each square.
      max_x, max_y: (int) how many squares in each direction.
    """
    self.scorecard_size = 40
    self.display = pygame.display.set_mode(
        (max_x * size, max_y * size + self.scorecard_size))
    self.screen = pygame.Surface((max_x * size, max_y * size)).convert()
    self.scorecard = pygame.Surface((max_x * size, 64)).convert()

    self.background = (0, 0, 0)  # rgb (black)
    self.occupied = set()
    self.obstacles = set()
    self.size = size
    self.max_x = max_x         # How many squares across.
    self.max_y = max_y         # How many qsuares down.
    self.score_text = None

  def set_background(self, rgb):
    """Set the background color.
    Args:
      rgb: (short, short, short) tuple of 0-255 values for red, green, blue.
    """
    self.background = rgb

  def update_score_text(self, message):
    """Set the scorecard message.

    Args:
      message: (str) text to display.
    """
    font = pygame.font.SysFont("verdana", 16)
    self.score_text = font.render(message, True, (255, 255, 255))

  def fill(self):
    """Completely fill the screen with the background color and any messages."""
    self.display.blit(self.screen, (0, 0))
    self.display.blit(self.scorecard, (0, self.max_y * self.size))
    self.occupied.clear()
    self.obstacles.clear()
    self.screen.fill(self.background)
    self.scorecard.fill((0, 0, 0))

  def show_messages(self):
    if self.score_text:
      self.scorecard.blit(self.score_text,
                          ((self.max_x * self.size - self.score_text.get_width()) / 2,
                           (self.scorecard_size - self.score_text.get_height()) / 2))

  def draw(self, image, x, y, obstacle=False):
    """Put an image on the screen at some location.

    Args:
      image: (pygame.Surface) Already-loaded image to draw.
      x, y: (int) Grid position, in squares.
      obstacle: (bool) whether the drawn thing stops other things from passing
                over it.
    """
    pos_x = self.pixels(x)
    pos_y = self.pixels(y)
    # Hack alert! We're doubling the size of all the images here because they're
    # 64px, we moved to 128px squares, and I'm too lazy to resize them. The
    # square size is set in the constructor of moana.AmazingMoanaGame.
    self.screen.blit(pygame.transform.scale2x(image), (pos_x, pos_y))
    self.occupied.add((x, y))
    if obstacle:
      self.obstacles.add((x, y))

  def pixels(self, index):
    """Take a grid square and returns coords of its top left hand corner.

    Args:
      index: (int) How many squares across or down.
    Returns:
      (int) How many pixels.
    """
    return index * self.size

  def in_bounds(self, pos, avoid_obstacles=True):
    """Return whether the coordinates are inside the screen dimensions.
    Args:
      pos: ((int, int)) x, y of squares on grid.
    Returns:
      (bool) Whether the location is inside the bounds of the grid.
    """
    x, y = pos
    if x < 0 or y < 0:
      return False
    if x >= self.max_x or y >= self.max_y:
      return False

    if avoid_obstacles and pos in self.obstacles:
      return False
    return True

  def random_square(self, avoid_obstacles=True, default_x=-1, default_y=-1):
    """Return a random square, optionally one without anything in it.

    TODO: This will loop forever if a column and avoid_obstacles are both
          specified and every square in the column is an obstable.

    Args:
      avoid_obstacles: (bool) only choose squares that don't already have
                      something
      column: (int) choose a square with this x-value.
    Return:
      ((int, int)): tuple of (x, y) coordinate.
    """
    if default_x >=0 and default_y >= 0:
      # we'll "randomly" choose the exact square you told us to.
      return (default_x, default_y)

    while True:
      x = default_x
      y = default_y
      if x < 0:
        x = random.randint(0, self.max_x -1)
      if y < 0:
        y = random.randint(0, self.max_y -1)
      if avoid_obstacles and (x, y) in self.obstacles:
        # there's already a thing there; try again
        continue

      return (x, y)
