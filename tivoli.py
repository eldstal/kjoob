import math
import itertools
import random

from app import *

import pygame
import animation
import color

class TivoliMaster(MasterApp):

  def __init__(self, owner):
    super().__init__(owner)

  def event(self, ev):
    if ev.type == pygame.KEYDOWN:
      if (ev.key == pygame.K_q):
        self.stop = True

  def run(self):
    return not self.stop



class TivoliSlave(SlaveApp):


  def __init__(self, owner):
    super().__init__(owner)
    self.clock = pygame.time.Clock()
    self.font = pygame.font.SysFont("sans", 16)

    # A terrible, animating background
    self.bspeed = 1200
    self.bcolors = itertools.cycle([ color.darken(c, 0.5) for c in color.RAINBOW])
    self.bblender = animation.Interpolate(next(self.bcolors), next(self.bcolors), self.bspeed)

    # Some text scrolling across the screen
    self.messages = itertools.cycle([
                      "The kjoob is alive with the sound of silence!",
                      "There isn't much else to show, really.",
                      "But let's do it anyway!"
                      ])
    self.message_text = next(self.messages)
    self.txpos = None
    self.txpos = None
    self.tcolor = (255, 255, 255)
    self.tperiod = 9000

    # The total width of the text message, one character at a time
    textwidth = 0
    for c in self.message_text:
      lbl = self.font.render(c, True, (1,1,1))
      textwidth += lbl.get_width()
    self.textwidth = textwidth

  def message(self, msg):
    return None

  def run(self, screen):
    self.clock.tick()

    # Smoothly changing background color
    bcolor = self.bblender.get()
    if (self.bblender.done()):
      # Pick a new destination color
      self.bblender = animation.Interpolate(bcolor, next(self.bcolors), self.bspeed)
    screen.fill(bcolor)

    # The scrolling text
    (w, h) = screen.get_size()
    if (self.txpos is None):
      # Initialize these values, now that we know the size of the window
      self.txpos = animation.Interpolate(w, -self.textwidth, self.tperiod)
      self.typos = h / 2
      self.tmagn = h / 6    # Sine wave magnitude
      self.tfreq = w / 2    # Sine wave frequency

    if (self.txpos.done()):
      self.message_text = next(self.messages)
      self.typos = (h / 2) * (0.5 + random.random())
      self.txpos.restart()

    xpos = self.txpos.get()
    for c in self.message_text:
      yoff = self.tmagn * math.sin(xpos * 2 * math.pi/ self.tfreq)
      label = self.font.render(c, True, self.tcolor)
      screen.blit(label, (xpos, self.typos + yoff))
      xpos += label.get_width()

    return not self.stop

App.register_app(TivoliMaster, TivoliSlave, name="Tivoli")
