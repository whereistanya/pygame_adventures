#!/usr/bin/python3
"""An extremely pointless game to learn pygame with."""

import pygame
import time

import drawer
import things

class AmazingMoanaGame(object):
  """OMG IT IS SO AMAZING."""

  def __init__(self, square_size=64, max_x=15, max_y=7,
               moana_image="images/babymoana.jpg",
               maui_image="images/maui.jpg",
               crab_image="images/crab.jpg",
               hook_image="images/fishhook.jpg",
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
    self.drawer = drawer.Drawer(square_size, max_x, max_y)
    self.moana = things.MovingThing(self.get_image(moana_image), self.drawer)
    self.maui = things.MovingThing(self.get_image(maui_image), self.drawer, x=max_x - 1)
    self.crab = things.SelfMovingThing(self.get_image(crab_image), self.drawer, x=int(max_x / 2))
    self.hook = things.StationaryThings(self.get_image(hook_image), self.drawer)
    self.hook.place_randomly(1)
    self.mud = things.StationaryThings(self.get_image(mud_image), self.drawer, obstacle=True)
    self.mud.place_randomly(15)
    self.shells = things.StationaryThings(self.get_image(shells_image), self.drawer)
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
