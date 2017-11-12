#!/usr/bin/python3
import time

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
  def __init__(self, image, drawer, x=0, y=0):
    """Set up the icon that moves to find things.

    Args:
      image: (pygame.Surface) a loaded image
      drawer: (drawer.Drawer) an initialised Drawer to display images
    """
    self.drawer = drawer
    self.image = image
    self.x = x
    self.y = y
    self.score = 0

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


  def draw(self):
    """Instruct the drawer to draw this thing at some location."""
    self.drawer.draw(self.image, self.x, self.y)

  def move_up(self, avoid_obstacles=True):
    if self.drawer.in_bounds((self.x, self.y - 1), avoid_obstacles):
      self.y -= 1
      return True
    else:
      return False

  def move_down(self, avoid_obstacles=True):
    if self.drawer.in_bounds((self.x, self.y + 1), avoid_obstacles):
      self.y += 1
      return True
    else:
      return False

  def move_left(self, avoid_obstacles=True):
    if self.drawer.in_bounds((self.x - 1, self.y), avoid_obstacles):
      self.x -= 1
      return True
    else:
      return False

  def move_right(self, avoid_obstacles=True):
    if self.drawer.in_bounds((self.x + 1, self.y), avoid_obstacles):
      self.x += 1
      return True
    else:
      return False

class SelfMovingThing(MovingThing):
  """An icon that moves on its own."""
  
  def __init__(self, image, drawer, x=0, y=0, move_every=1):
    """Set up the icon that moves to find things.

    Args:
      image: (pygame.Surface) a loaded image
      drawer: (drawer.Drawer) an initialised Drawer to display images
      x, y: (int) starting co=ordinates
      move_every: (int) how often to move in seconds
    """
    super().__init__(image, drawer, x, y)
    self.last_move = time.time()
    self.moving = "down"
    self.move_every = move_every

  
  def move_up_and_down(self):
    now = time.time()
    if now - self.last_move < 1:
      return
    if self.moving == "down":
      if not self.move_down(avoid_obstacles=False):
        self.moving = "up"
    else:
      if not self.move_up(avoid_obstacles=False):
        self.moving = "down"
    self.last_move = time.time()
