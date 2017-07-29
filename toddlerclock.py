#!/usr/bin/python3
"""A clock to tell your toddler whether they can wake you."""

import os
import time
import pygame

from signal import alarm, signal, SIGALRM


WHITE = ((255, 255, 255))
BLACK = ((0, 0, 0))
RED = ((255, 0, 0))
BLUE = ((5, 20, 114))
GREEN = ((52, 114, 5))
ORANGE = ((239, 103, 19))
PINK = ((178, 53, 161))
INDIGO = ((59, 33, 135))

class Alarm(Exception):
  """A deadline for things that get wedged."""
  pass

def alarm_handler(signum, frame):
  raise Alarm


class ToddlerClock(object):
  """Display the time with a message."""

  def __init__(self):
    """ """
    # Needed to talk to the raspberry pi's PiTFT display.
    os.putenv('SDL_FBDEV', '/dev/fb1')
    os.putenv('SDL_MOUSEDRV', 'TSLIB')
    os.putenv('SDL_MOUSEDEV', '/dev/input/touchscreen')

    self.x = 320
    self.y = 240
    self.bottom = 200
    pygame.init()
    pygame.mouse.set_visible(False)
    #  If this hangs, it's because something else is using the screen. Ctrl-C
    #  here will bypass that.
    signal(SIGALRM, alarm_handler)
    alarm(2)
    try:
      print("Attempting to initialise the display. Waiting up to two seconds.")
      self.screen = pygame.display.set_mode((self.x, self.y))
      alarm(0)
    except Alarm:
      raise KeyboardInterrupt
    self.clocksurface = pygame.Surface((self.x, self.bottom)).convert()
    self.messagesurface = pygame.Surface((self.x, self.y - self.bottom)).convert()

    self.bigfont = pygame.font.SysFont("verdana", 90)
    self.smallfont = pygame.font.SysFont("verdana", 18)
    self.clock = pygame.time.Clock()

  def run(self):
    """The main loop."""
    while True:
      self.screen.blit(self.clocksurface, ((0, 0)))
      self.screen.blit(self.messagesurface, ((0, self.bottom)))

      now = time.localtime()
      nowstr = self.bigfont.render("%.2d:%.2d" % (now.tm_hour, now.tm_min),
                                   True, WHITE)

      hour = now.tm_hour
      minute = now.tm_min
      day = now.tm_wday  # monday is 0

      if hour < 6:
        color = BLACK
        message = self.smallfont.render(
            "Too early. Go back to sleep, Biz.", True, RED)
      elif hour < 7:
        color = BLUE
        message = self.smallfont.render(
            "Time to read, Biz.", True, WHITE)
      elif hour < 8:
        color = GREEN
        message = self.smallfont.render(
            "It's morning! Wake up, parents!", True, WHITE)
      elif hour < 9 and day <= 4:
        color = RED
        message = self.smallfont.render(
            "Time for school, Biz!", True, WHITE)
      elif hour < 18:
        color = ORANGE
        message = self.smallfont.render(
            "Go have fun, Biz!", True, WHITE)
      elif hour == 18 and minute <= 30:
        color = ORANGE
        message = self.smallfont.render(
            "Time for dinner, Biz!", True, WHITE)
      elif hour < 20:
        color = PINK
        message = self.smallfont.render(
            "Time for bed, Biz!", True, WHITE)
      else:
        color = BLACK
        message = self.smallfont.render(
            "Too early. Go back to sleep, Biz.", True, RED)

      self.draw(color, nowstr, message)
      self.clock.tick(1) # every 1s

  def draw(self, color, nowstr, message):
    """Draw the clock with a message!"""
    self.clocksurface.fill(color)
    self.messagesurface.fill(color)

    self.clocksurface.blit(nowstr,
                           ((self.x - nowstr.get_width()) / 2,
                            (self.bottom - nowstr.get_height()) / 2))
    self.messagesurface.blit(message,
                             ((self.x - message.get_width()) / 2,
                              (self.y - self.bottom - message.get_height()) / 2))
    pygame.display.flip()


# Main.
toddlerclock = ToddlerClock()
toddlerclock.run()
