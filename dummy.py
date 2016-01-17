from app import *

import pygame
import color

class DummyMaster(MasterApp):

  def __init__(self, owner):
    super().__init__(owner)

  def event(self, ev):
    if ev.type == pygame.KEYDOWN:
      if (ev.key == pygame.K_q):
        self.stop = True

  def run(self):
    return not self.stop



class DummySlave(SlaveApp):

  def __init__(self, owner):
    super().__init__(owner)
    self.font = pygame.font.SysFont("sans", 36)
    self.label1 = self.font.render("Dummy app", True, (0xec, 0xbc, 0xbc))
    self.label2 = self.font.render("Press Q to return to menu", True, (0xec, 0xbc, 0xbc))

  def message(self, msg):
    return None

  def run(self, screen):
    screen.fill((0, 14, 24))

    lineheight = self.font.get_height() + 4
    screen.blit(self.label1, (4, lineheight))
    screen.blit(self.label2, (4, 2*lineheight))

    return not self.stop

App.register_app(DummyMaster, DummySlave, name="Dummy App")
