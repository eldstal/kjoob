import pygame

import color

class Interpolate:

  def __init__(self, a, b, t, timer=pygame.time.get_ticks):
    """
    Two values or tuples and a transition time in ms
    timer is a monotonously increasing function
    """
    self.a = a
    self.b = b
    self.t = t
    self.timer = timer
    self.start = self.timer()

  def get(self):
    progress = min((self.timer() - self.start) / self.t, 1)
    if (progress < 1):
      return color.blend(self.a, self.b, progress)
    else:
      return self.b

  def done(self):
    return self.timer() >= (self.start + self.t)

  def restart(self):
    self.start = self.timer()

  def reverse(self):
    b = self.b
    self.b = self.a
    self.a = b
    self.restart()

