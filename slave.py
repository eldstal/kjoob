from master import Master
from menu import *

import pygame

class Slave:

  def __init__(self):
    self.master = Master() # This is a dummy.
    self.identity = -1

  def set_master(self, master):
    """ Must be called before anything else. """
    self.master = master
    self.identity = master.slave_register(self)

  def master_goto_menu(self, appname):
    """ Called by the master to show the menu. Any running app is shut down. """
    print("Dummy slave goto_menu")

  def master_start_app(self, appname):
    """ Called by the master to start an application and pass control to it """
    print("Dummy slave start_app %s" % appname)

  def master_shutdown(self):
    """ Called by the master to stop the running app and shut down """
    print("Dummy slave shutting down...")

  def master_message(self, msg):
    """
    Called when there is an incoming message from the master.
    Incoming messages have an app_id which is 0 for global events and
    otherwise associated with specific apps.
    """
    print("Dummy slave received message: %s" % msg)


class RemoteSlave(Slave):
  """
  A remotely connected slave. (exists only on the master side)
  Assign it an incoming connection and set_master() with a LocalMaster,
  it will decode messages and call functions on its Master.
  """
  def __init__(self, conn):
    super().__init__()
    self.conn = conn
    self.identity = -1

  # TODO: Call master.slave_register() and return the identity
  # TODO: Receive messages and pass them to self.master.slave_message()

  def master_message(self, msg):
    # TODO: Parse the message and send it over the net
    pass


class LocalSlave(Slave):
  """
  Actual slave logic.
  Interacts with a remote or local master, draws the context etc.
  """
  def __init__(self, role, master, app_conf):
    super().__init__()
    self.conf = app_conf
    self.role = role
    self.running_app = None
    self.stop = False
    self.menu = MenuSlave(self)

    self.set_master(master)
    self.master.slave_set_role(self, role)
    print("Local slave started with ID %d" % self.identity)

  def launch_app(self, app):
    """ Called when the menu app has selected an app to start. """
    print("Slave launching app: %s " % app)
    self.running_app = app(owner=self)

  def master_goto_menu(self):
    print("Client returning to menu")
    if (self.running_app is not None):
      self.running_app.stop()

  def master_start_app(self, app_id):
    print("Client starting app %s" % app_id)
    appclass = App.get_slave_app(app_id)
    self.running_app = appclass(self)

  def master_shutdown(self):
    print("Client shutting down...")
    self.stop = True

  def master_message(self, msg):
    appid = msg['app']
    if self.running_app is not None:
      if (appid == self.running_app.app_id or appid == 0):
        self.running_app.message(msg)
    elif (appid == self.menu.app_id or appid == 0):
        self.menu.message(msg)
    pass

  def run(self, screen):
    """ Non-blocking, run one iteration of whatever you're doing. Return False if stopped, True if running """
    # Run whatever app is in the foreground
    if (not self.stop):
      if (self.running_app is not None):
        terminate = not self.running_app.run(screen)
        if (terminate): self.running_app = None
      else:
        terminate = not self.menu.run(screen)
        if (terminate): self.stop = True
      pygame.display.flip()
    return not self.stop

