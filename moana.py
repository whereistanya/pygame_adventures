#!/usr/bin/python3
"""An extremely pointless game to learn pygame with."""

import pygame
import time

class StationaryThings(object):
  """Any type of unmoving thing that appears on the grid."""
  def __init__(self, image, drawer, obstacle=False):
    """Set up the thing to be drawn.

    Args:
      image: (pygame.Surface) a loaded image.
      drawer: (Drawer) an initialised Drawer to display images.
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
      drawer: (Drawer) an initialised Drawer to display images
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
      drawer: (Drawer) an initialised Drawer to display images
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
    self.screen.blit(image, (pos_x, pos_y))
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

  def random_square(self, avoid_occupied=True):
    """Return a random square, optionally one without anything in it."""
    while True:
      x = random.randint(0, self.max_x -1)
      y = random.randint(0, self.max_y -1)
      if avoid_occupied and (x, y) in self.occupied:
        # there's already a thing there; try again
        continue
      return (x, y)

class AmazingMoanaGame(object):
  """OMG IT IS SO AMAZING."""

  def __init__(self, square_size=64, max_x=15, max_y=7,
               moana_image="images/babymoana.jpg",
               maui_image="images/maui.jpg",
               crab_image="images/crab.jpg",
               hook_image="images/hook.jpg",
               shells_image="images/shell.png",
               mud_image="images/mud.png"):
    """Set up the game.

    Add one Moana character, a bunch of shells and a bunch of obstacles. Beware:
    this does nothing intelligent about making sure all shells are reachable or
    checking that the character doesn't get trapped in a corner surrounded by
    obstacles. No pathfinding algorithms were invoked in the writing of this
    game.

    Args:
      square_size: (int) the size of each grid square. The images on the grid
                   should be square and should be this size or it'll look like a mess.
      max_x, max_y: (int) how many squares on each side of the grid.
      moana_image, maui_image: (string) filenames of the images that move around finding things.
      shells_image: (string) filename of the image that gets found
      mud_image: (string) filename of the image that represents an obstacle
    """
    pygame.init()
    pygame.mixer.music.load("sounds/shells.wav")
    pygame.mixer.music.play()
    self.clock = pygame.time.Clock()
    self.image_lib = {}
    self.done = False
    self.drawer = Drawer(square_size, max_x, max_y)
    self.moana = MovingThing(self.get_image(moana_image), self.drawer)
    self.maui = MovingThing(self.get_image(maui_image), self.drawer, x=max_x - 1)
    self.crab = SelfMovingThing(self.get_image(crab_image), self.drawer, x=int(max_x / 2))
    self.hook = StationaryThings(self.get_image(hook_image), self.drawer)
    self.hook.place_randomly(1)
    self.mud = StationaryThings(self.get_image(mud_image), self.drawer, obstacle=True)
    self.mud.place_randomly(15)
    self.shells = StationaryThings(self.get_image(shells_image), self.drawer)
    self.shells.place_randomly(50)
    self.drawer.set_background((0, 0, 255))  # blue
    self.drawer.update_score_text("Get the hook!")
    self.has_hook = False

  def run(self):
    """The main game loop. Draw stuff and look for events."""
    while not self.done:
      self.check_events()
      self.drawer.fill()
      self.mud.draw()
      self.shells.draw()
      self.crab.move_up_and_down()
      self.moana.draw()
      self.maui.draw()
      self.crab.draw()
      self.hook.draw()

      if self.has_hook:
        if self.crab.is_at(self.moana.pos()) or self.crab.is_at(self.maui.pos()):
          self.drawer.set_background((0, 0, 255))  #blue
          self.has_hook = False
          self.hook.place_randomly(1)
          self.drawer.update_score_text("You LOST the hook!")

        if self.shells.is_at(self.moana.pos()):
          self.shells.delete(self.moana.pos())
          self.moana.score += 1
          self.update_score_text()
        if self.shells.is_at(self.maui.pos()):
          self.shells.delete(self.maui.pos())
          self.maui.score += 1
          self.update_score_text()

      if self.hook.is_at(self.moana.pos()):
        self.drawer.set_background((255, 102, 255))  # pink
        self.hook.delete(self.moana.pos())
        self.has_hook = True
        self.drawer.update_score_text("You got the hook!")
      if self.hook.is_at(self.maui.pos()):
        self.drawer.set_background((255, 102, 255))  # pink
        self.hook.delete(self.maui.pos())
        self.has_hook = True
        self.drawer.update_score_text("You got the hook!")

      self.drawer.show_messages()
      pygame.display.flip()
      self.clock.tick(60)

  def win(self):
    """Set a winning message for winners."""
    pygame.mixer.music.load("sounds/we_did_it.wav")
    pygame.mixer.music.play()
    self.drawer.set_background((0, 255, 0))  # green

  def update_score_text(self):
    count = self.shells.count()
    score_str = "Moana: %d, Maui: %d" % (self.moana.score, self.maui.score)
    if count == 0:
      self.drawer.update_score_text(
          "You did it!! %s   GREAT TEAM WORK! Press y to play again." %
          score_str)
      self.win()
      return
    if count == 1:
      self.drawer.update_score_text("Only 1 shell left! %s" % score_str)
      return
    self.drawer.update_score_text("%d shells left! %s" % (count, score_str))

  def check_events(self):
    """Check for keypresses and take actions based on them."""
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        self.done = True
      pressed = pygame.key.get_pressed()
      # move maui
      if pressed[pygame.K_UP]:
        self.maui.move_up()
      if pressed[pygame.K_DOWN]:
        self.maui.move_down()
      if pressed[pygame.K_LEFT]:
        self.maui.move_left()
      if pressed[pygame.K_RIGHT]:
        self.maui.move_right()
      # move moana
      if pressed[pygame.K_w]:
        self.moana.move_up()
      if pressed[pygame.K_s]:
        self.moana.move_down()
      if pressed[pygame.K_a]:
        self.moana.move_left()
      if pressed[pygame.K_d]:
        self.moana.move_right()

      # quit/restart
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
    if image is None:
      image = pygame.image.load(filename)
    return image


# Main.
game = AmazingMoanaGame()
game.run()
