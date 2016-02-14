import pygame
import ujson
from twisted.internet.protocol import Protocol

import sys

from menu import *

class Master:
  """
  The game master, which coordinates connections from both local and remote slaves
  """
  def __init__(self):
    pass

  def slave_register(self, slave):
    """ Called by new slaves """

  def slave_message(self, slave, msg):
    """ Called when a message arrives from a slave """


class RemoteMaster(Master, Protocol):
  """
  A remote master (exists only on the slave side)
  Initialize an object of this class to connect to the server
  Then call add_slave to set the local slave that this connection serves
  """
  def __init__(self):
    Master.__init__(self)
    self.slave = None
    pass

  def dataReceived(self, data):
    # Incoming message from the server
    utf = data.decode("UTF-8")

    for json in utf.split("\xef"):
      if (len(json) == 0): continue
      try:
        payload = ujson.loads(json)
        if (payload['app'] == 0):
          self.master_broadcast(payload)
        else:
          self.slave.master_message(payload)
      except:
        sys.stdout.write("Invalid message received: %s" % json)

  def master_broadcast(self, msg):
    # Broadcast message received from master (app: 0)
    if (msg['msg'] == 10):
      # Return to menu
      self.slave.master_goto_menu()
    if (msg['msg'] == 11):
      # Launch/switch to an application by ID
      self.slave.master_start_app(msg['data'])

  def slave_register(self, slave):
    self.slave = slave

  def slave_message(self, slave, msg):
    payload = ujson.dumps(msg) + "\xef"   # Delimiter character
    clean = payload.encode("UTF-8")
    self.transport.write(clean)


class LocalMaster(Master):
  """
  Actual master logic.
  Interacts with local or remote Slave objects to keep state consistent across screens
  """
  def __init__(self):
    super().__init__()
    print("Local Master initialized")
    self.slaves = []
    self.menu = MenuMaster(self)
    self.running_app = self.menu

  def shutdown(self):
    for s in self.slaves:
      s.master_shutdown()

  def push_state(self):
    """ Send an update to all connected slaves, starting with the running app id """
    for s in self.slaves:
      s.master_start_app(self.running_app.app_id)

    self.running_app.push_state()

  def launch_app(self, app_id):
    """ Called when the menu app has selected an app to start. Will also be called on slaves automatically. """
    app = App.get_master_app(app_id)

    if (app is None):
      print("Master failed to find appid %d." % app_id)
      return

    print("Master launching app: %s " % app)
    for s in self.slaves:
      s.master_start_app(app_id)

    self.running_app = app(self)

  def goto_menu(self):
    """ Command all slaves to start or return to the main menu """
    self.running_app = self.menu
    for s in self.slaves:
      s.master_goto_menu()
    self.push_state()

  def send_message(self, msg):
    """ Callback from apps. Send a message to all slaves """
    for s in self.slaves:
      s.master_message(msg)

  def slave_register(self, slave):
    self.slaves.append(slave)
    print("New slave registered: %s" % slave.describe())
    self.push_state()

  def run(self):

    # Handle local events, such as user input. Master is the only one to see these.
    for ev in pygame.event.get():
      if (ev.type == pygame.QUIT):
        self.shutdown()
      self.running_app.event(ev)

    terminate = not self.running_app.run()
    if (terminate):
      if (self.running_app == self.menu):
        shutdown()
      else:
        self.goto_menu()
