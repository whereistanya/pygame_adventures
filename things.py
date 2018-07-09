#!/usr/bin/python3
import time
import pygame

class StationaryThings(object):
  """Any type of unmoving thing that appears on the grid."""
  def __init__(self, image, drawer, obstacle=False):
    """Set up the thing to be drawn.

    Args:
      image: (pygame.Surface) a loaded image.
      drawer: (drawer.Drawer) an initialised Drawer to display images.
      obstacle: (bool) Does this thing prevent moveable things from passing it?
    """
    self.things = set()   # Set of (x, y) tuples, indexed by grid pos, not pixels
    self.drawer = drawer
    self.image = image
    self.obstacle = obstacle

  def add_at(self, pos):
    """Add a thing at a square on the grid.

    Args:
      pos: ((int, int)): x, y tuple for position on grid.
    """
    if self.drawer.in_bounds(pos):
      self.things.add(pos)

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
      self.drawer.draw(self.image, x, y, self.obstacle)

  def delete(self, pos):
    """Remove the thing at some position.

    Args:
      pos: ((int, int)): tuple showing x, y position.
    """
    self.things.remove(pos)

  def place_randomly(self, count):
    """Place count things randomly on the grid."""
    # Choose positions for the objects.
    while count > 0:
      pos = self.drawer.random_square()
      if pos in self.things:
        continue  # Don't reuse a square
      self.add_at(pos)
      count -= 1
    self.draw()  # Initial draw to make the drawer consider these squares
                 # occupied


class MovingThing(object):
  """An icon that moves around."""
  def __init__(self, image, drawer, x=-1, y=-1, capacity=8):
    """Set up the icon that moves to find things.

    Args:
      image: (pygame.Surface) a loaded image
      drawer: (drawer.Drawer) an initialised Drawer to display images
      x: (int) which column to randomly draw this in
    """
    self.drawer = drawer
    self.image = image
    self.images = { "default" : image}
    dark = pygame.Surface(self.image.get_size()).convert_alpha()
    dark.fill((0, 0, 0, .8 * 255))
    self.images["frozen"] = dark

    self.frozen = False
    self.capacity = capacity
    self.carrying = 0

    self.score = 0
    (self.x, self.y) = self.drawer.random_square(default_x=x, default_y=y)
    self.draw()  # Initial draw to make the drawer consider these squares
                   # occupied

  def pos(self):
    """Return current location.

    Returns:
      (int, int): tuple of x, y co-ordinates.
    """
    return (self.x, self.y)

  def is_at(self, pos):
    """Return whether the thing is at this position.

    Args:
      pos: ((int, int)): tuple showing x, y position.
    """
    if pos == (self.x, self.y):
      return True
    return False

  def add_replacement_image(self, image):
    """Add an alternative image to use in some situations.

    This could be expanded to have multiple named images but for now it's just
    the default or the replacement.

    Args:
      image: (pygame.Surface) a loaded image
    """
    self.images["replacement"] = image

  def set_replacement_image(self):
    """Replace the MovingThing's image with the alternate."""
    try:
      self.image = self.images["replacement"]
    except KeyError:
      print("No replacement image.")

  def set_default_image(self):
    """Replace the MovingThing's image with the default."""
    try:
      self.image = self.images["default"]
    except KeyError:
      print("No default image.")

  def freeze(self):
      self.frozen = True
      self.image = self.images["frozen"]

  def unfreeze(self):
      self.frozen = False
      self.image = self.images["default"]

  def draw(self):
    """Instruct the drawer to draw this thing at some location."""
    self.drawer.draw(self.image, self.x, self.y)

  def move_up(self, avoid_obstacles=False):
    if self.frozen:
      return

    if self.drawer.in_bounds((self.x, self.y - 1), avoid_obstacles):
      self.y -= 1
      return True
    else:
      return False

  def move_down(self, avoid_obstacles=False):
    if self.frozen:
      return
    if self.drawer.in_bounds((self.x, self.y + 1), avoid_obstacles):
      self.y += 1
      return True
    else:
      return False

  def move_left(self, avoid_obstacles=False):
    if self.frozen:
      return
    if self.drawer.in_bounds((self.x - 1, self.y), avoid_obstacles):
      self.x -= 1
      return True
    else:
      return False

  def move_right(self, avoid_obstacles=False):
    if self.frozen:
      return
    if self.drawer.in_bounds((self.x + 1, self.y), avoid_obstacles):
      self.x += 1
      return True
    else:
      return False

class SelfMovingThing(MovingThing):
  """An icon that moves on its own."""

  def __init__(self, image, drawer, x=-1, y=-1, move_every=1):
    """Set up the icon that moves to find things.

    Args:
      image: (pygame.Surface) a loaded image
      drawer: (drawer.Drawer) an initialised Drawer to display images
      x, y: (int) starting co=ordinates
      move_every: (int) how often to move in seconds
    """
    super().__init__(image, drawer, x, y)
    self.last_move = time.time()
    self.direction = "down"
    self.move_every = move_every
    self.stopped = False

  def stop(self):
    self.stopped = True

  def move_up_and_down(self):
    if self.stopped:
      return
    now = time.time()
    if now - self.last_move < 1:
      return
    if self.direction == "down":
      if not self.move_down(avoid_obstacles=False):
        self.direction = "up"
    else:
      if not self.move_up(avoid_obstacles=False):
        self.direction = "down"
    self.last_move = time.time()

  def move_over_and_back(self):
    if self.stopped:
      return
    now = time.time()
    if now - self.last_move < 1:
      return
    if self.direction == "right":
      if not self.move_right(avoid_obstacles=False):
        self.direction = "left"
    else:
      if not self.move_left(avoid_obstacles=False):
        self.direction = "right"
    self.last_move = time.time()
