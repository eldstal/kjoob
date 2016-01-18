import math

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
    self.bcolors = color.RAINBOW
    self.bdest = 1
    self.bblender = animation.Interpolate(self.bcolors[0], self.bcolors[1], self.bspeed)

    # Some text scrolling across the screen
    self.message_text = "The kjoob is alive with the sound of silence!"
    self.tpos = None
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
      self.bdest = (self.bdest + 1) % len(self.bcolors)
      self.bblender = animation.Interpolate(bcolor, self.bcolors[self.bdest], self.bspeed)
    screen.fill(bcolor)

    # The scrolling text
    (w, h) = screen.get_size()
    if (self.tpos is None):
      # Initialize these values, now that we know the size of the window
      self.tpos = animation.Interpolate(w, -self.textwidth, self.tperiod)
      self.tmagn = h / 6    # Sine wave magnitude
      self.tfreq = w / 2    # Sine wave frequency

    if (self.tpos.done()):
      self.tpos.restart()

    xpos = self.tpos.get()
    for c in self.message_text:
      ypos = self.tmagn * math.sin(xpos * 2 * math.pi/ self.tfreq)
      label = self.font.render(c, True, self.tcolor)
      screen.blit(label, (xpos, (screen.get_height() / 2) + ypos))
      xpos += label.get_width()

    return not self.stop

App.register_app(TivoliMaster, TivoliSlave, name="Tivoli")
