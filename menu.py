from app import App

import pygame

class Menu(App):

  options = [ "First", "Second", "Third" ]

  def __init__(self, callback):
    """ callback is an object with a launch_app(app) method, called when an app is selected in the menu """
    self.selected = 0
    super().__init__()

  def master_event(self, ev):
    if (type(ev) is pygame.event.EventType):
      if ev.type == pygame.KEYDOWN:
        if (ev.key == pygame.K_UP):
          self.selected -= 1
        if (ev.key == pygame.K_DOWN):
          self.selected += 1

    self.selected = min(self.selected, len(self.options)-1)
    self.selected = max(self.selected, 0)
    print("Menu selection: %d. %s" % (self.selected, self.options[self.selected]))
    return None

  def slave_run(self, screen):
    # TODO: Draw things
    return not self.stop

  def master_run(self):
    return not self.stop

