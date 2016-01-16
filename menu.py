from app import *

import color

import pygame

class MenuMaster(MasterApp):

  options = [ "First", "Second", "Third" ]

  def __init__(self, owner):
    """ owner is an object with a launch_app(app) method, called when an app is selected in the menu """
    self.selected = 0
    self.dirty = True
    super().__init__(owner)

  def sel_vert(self, diff):
    self.selected += diff
    self.selected = min(self.selected, len(self.options)-1)
    self.selected = max(self.selected, 0)
    self.send_message({'app':self.app_id, 'msg':1, 'data':self.selected})

  def push_state(self):
    if (not self.dirty): return
    self.dirty = False
    self.send_message({'app':self.app_id, 'msg':0, 'data':self.options})

  def event(self, ev):
    if ev.type == pygame.KEYDOWN:
      if (ev.key == pygame.K_UP):
        self.sel_vert(-1)
      if (ev.key == pygame.K_DOWN):
        self.sel_vert(+1)
    return None

  def run(self):
    self.push_state()
    return not self.stop


class MenuSlave(SlaveApp):

  textcolor = (255,255,255)
  fade = 0.2
  backcolor = (40, 40, 40)

  def __init__(self, owner):
    """ owner is an object with a launch_app(appobj) method, called when an app is selected in the menu """
    self.selected = 0
    self.options = []
    self.selected_font = pygame.font.SysFont("sans", 24)
    self.unselected_font = pygame.font.SysFont("sans", 16)
    super().__init__(owner)

  def message(self, msg):
    if (msg['msg'] == 0):   # List of selectable things
      self.options = msg['data']
    if (msg['msg'] == 1):   # Selection changed
      self.selected = msg['data']
    return None

  def centering(self,small, big):
    (w1, h1) = big.get_size()
    (w2, h2) = small.get_size()
    x = (w1 / 2) - (w2 / 2)
    y = (h1 / 2) - (h2 / 2)
    return (x, y)

  def run(self, screen):
    screen.fill(self.backcolor)
    # The selected thing is at the center
    # text is centered
    for i in range(len(self.options)):
      slot = i - self.selected
      tone = color.blend(self.backcolor, self.textcolor, self.fade * abs(slot))

      if (slot == 0): font = self.selected_font
      else: font = self.unselected_font

      text = "%d. %s" % (i, self.options[i])
      label = font.render(text, True, tone)

      (x, y) = self.centering(label, screen)
      lineheight = font.get_height() + 4
      screen.blit(label, (x, y + lineheight * slot))
    return not self.stop


App.register_app(MenuMaster, MenuSlave)
