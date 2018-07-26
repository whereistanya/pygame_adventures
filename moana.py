#!/usr/bin/python3
"""An extremely pointless game to learn pygame with."""

import pygame
import time

import drawer
import things

class AmazingMoanaGame(object):
  """OMG IT IS SO AMAZING.

  Square size is currently 128 but images are 64x64 because they were already
  that size and I was lazy. I'll fix it some time.
  """

  def __init__(self, square_size=128, max_x=15, max_y=7,
               moana_image="images/baby_moana_by_biz.jpg",
               moana_boat_image="images/moana_boat.jpg",
               maui_image="images/maui_bird_by_biz.jpg",
               sharkhead_image="images/maui_by_biz.jpg",
               crab_image="images/crab_by_biz.jpg",
               dad_image="images/moana_dad.jpg",
               lava_image="images/lava_monster_by_biz.jpg",
               island_image="images/tifiti_by_biz.jpg",
               hook_image="images/fishhook.jpg",
               boat_image="images/boat.jpg",
               heart_image="images/heart_by_biz.jpg",
               shell_bin_image="images/shell_bin_by_biz.jpg",
               shells_image="images/shell.png",
               mud_image="images/lava_by_biz.jpg"):
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
    """
    pygame.init()
    pygame.mixer.music.load("sounds/shells.wav")
    pygame.mixer.music.play()
    self.clock = pygame.time.Clock()
    self.image_lib = {}
    self.done = False
    self.drawer = drawer.Drawer(square_size, max_x, max_y)

    self.crab = things.SelfMovingThing(self.get_image(crab_image), self.drawer, x=int(max_x / 2))
    self.dad = things.SelfMovingThing(self.get_image(dad_image), self.drawer, y=int(max_y / 2))

    self.mud = things.StationaryThings(self.get_image(mud_image), self.drawer, obstacle=True)
    self.mud.place_randomly(15)
    self.shells = things.StationaryThings(self.get_image(shells_image), self.drawer)
    self.shells.place_randomly(50)

    self.hook = things.StationaryThings(self.get_image(hook_image), self.drawer)
    self.hook.place_randomly(1)
    self.boat = things.StationaryThings(self.get_image(boat_image), self.drawer)
    self.boat.place_randomly(1)

    self.heart = things.StationaryThings(self.get_image(heart_image), self.drawer)

    self.shell_bin = things.StationaryThings(self.get_image(shell_bin_image), self.drawer)
    self.shell_bin.place_randomly(1)

    self.moana = things.MovingThing(self.get_image(moana_image), self.drawer, x=0)
    self.moana.add_replacement_image(self.get_image(moana_boat_image))
    self.maui = things.MovingThing(self.get_image(sharkhead_image), self.drawer, x=max_x - 1)
    self.maui.add_replacement_image(self.get_image(maui_image))

    self.island = things.MovingThing(self.get_image(lava_image), self.drawer, x=0, y=0)
    self.island.add_replacement_image(self.get_image(island_image))

    self.drawer.set_background((255, 64, 0))  # orange
    self.drawer.update_score_text("Get the hook!")
    self.has_hook = False
    self.has_boat = False


  def run(self):
    """The main game loop. Draw stuff and look for events."""
    while not self.done:
      self.check_events()
      self.drawer.fill()
      self.heart.draw()
      self.island.draw()
      self.shells.draw()
      self.mud.draw()
      self.crab.move_up_and_down()
      self.dad.move_over_and_back()
      self.hook.draw()
      self.boat.draw()
      self.moana.draw()
      self.maui.draw()
      self.crab.draw()
      self.dad.draw()
      self.shell_bin.draw()

      if self.has_hook:
        if self.crab.is_at(self.maui.pos()):
          self.drawer.set_background((255, 64, 0))  # orange
          self.has_hook = False
          self.hook.place_randomly(1)
          self.maui.set_default_image()
          self.drawer.update_score_text("You LOST the hook!")

        if self.shells.is_at(self.maui.pos()):
          self.shells.delete(self.maui.pos())
          self.maui.carrying += 1
          if self.maui.carrying >= self.maui.capacity:
            self.shells.place_randomly(1)
            self.drawer.update_score_text("OH NO! MAUI DROPPED A SHELL! Put the shells in the shell bin!")
          else:
            self.maui.score += 1
            self.update_score_text()


      if self.has_boat:
        if self.dad.is_at(self.moana.pos()):
          self.drawer.set_background((255, 64, 0))  # orange
          self.has_boat = False
          self.boat.place_randomly(1)
          self.moana.set_default_image()
          self.drawer.update_score_text("You LOST the boat!")

        if self.shells.is_at(self.moana.pos()):
          self.shells.delete(self.moana.pos())
          self.moana.carrying += 1
          if self.moana.carrying >= self.moana.capacity:
            self.shells.place_randomly(1)
            self.drawer.update_score_text("OH NO! MOANA DROPPED A SHELL! Put the shells in the shell bin!")
          else:
            self.moana.score += 1
            self.update_score_text()


      if self.shell_bin.is_at(self.maui.pos()):
        self.maui.carrying = 0
        self.drawer.update_score_text("HURRAY! Now Maui can't lose shells any more!")

      if self.shell_bin.is_at(self.moana.pos()):
        self.moana.carrying = 0
        self.drawer.update_score_text("HURRAY! Now Moana can't lose shells any more!")


      # Only Moana can get the heart.
      if self.heart.is_at(self.moana.pos()):
        self.island.set_replacement_image()
        score_str = "TEFITI HAS HER HEART BACK! Moana: %d, Maui: %d" % (self.moana.score, self.maui.score)
        self.win(score_str)

      # Only Maui can get the hook.
      if self.hook.is_at(self.maui.pos()):
        self.hook.delete(self.maui.pos())
        self.maui.set_replacement_image()
        self.has_hook = True
        self.drawer.update_score_text("You got the hook!")
        if self.has_boat:
          # we're ready to begin!
          self.drawer.set_background((0, 0, 255))  # blue

      # Only Moana can get the boat.
      if self.boat.is_at(self.moana.pos()):
        self.boat.delete(self.moana.pos())
        self.moana.set_replacement_image()
        self.has_boat = True
        self.drawer.update_score_text("You got the boat!")
        if self.has_hook:
          # we're ready to begin!
          self.drawer.set_background((0, 0, 255))  # blue

      # If they walk into lava, they get frozen and lose their things.
      if self.mud.is_at(self.moana.pos()):
        self.moana.freeze()
        self.drawer.update_score_text("Moana is STUCK IN LAVA! Get her boat to save her!")
        self.mud.delete(self.moana.pos())
        if self.has_boat:
          self.boat.place_randomly(1)
          self.has_boat = False

      if self.mud.is_at(self.maui.pos()):
        self.maui.freeze()
        self.drawer.update_score_text("Maui is STUCK IN LAVA! Get his hook to save him!")
        self.mud.delete(self.maui.pos())
        if self.has_hook:
          self.hook.place_randomly(1)
          self.has_hook = False

      # If both are frozen, the game is over.
      if self.moana.frozen and self.maui.frozen:
        score_str = "Moana: %d, Maui: %d" % (self.moana.score, self.maui.score)
        self.lose(score_str)

      # They can unfreeze each other with each other's things.
      if self.hook.is_at(self.moana.pos()):
        self.maui.unfreeze()
        self.hook.delete(self.moana.pos())
        self.has_hook = True

      if self.boat.is_at(self.maui.pos()):
        self.moana.unfreeze()
        self.boat.delete(self.maui.pos())
        self.has_boat = True


      self.drawer.show_messages()
      pygame.display.flip()
      self.clock.tick(60)

  def win(self, score_str):
    """Set a winning message for winners."""
    pygame.mixer.music.load("sounds/we_did_it.wav")
    pygame.mixer.music.play()
    self.drawer.update_score_text(
        "You did it!! %s   GREAT TEAM WORK! Press y to play again, q to quit." %
        score_str)
    self.drawer.set_background((0, 255, 0))  # green
    self.crab.stop()
    self.dad.stop()

  def lose(self, score_str):
    """Set a losing message for losers."""
    self.drawer.update_score_text(
        "AWWW WE LOST. %s Press y to play again, q to quit." % score_str)
    self.drawer.set_background((0, 0, 0))  # black
    self.crab.stop()
    self.dad.stop()


  def update_score_text(self):
    count = self.shells.count()
    score_str = "Moana: %d (%d), Maui: %d (%d)" % (
      self.moana.carrying, self.moana.score, self.maui.carrying, self.maui.score)
    if count == 0:
      self.heart.place_randomly(1)
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
      if pressed[pygame.K_q]:
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
