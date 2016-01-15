from master import Master
from menu import Menu

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
    self.menu = Menu(self)

    self.set_master(master)
    self.master.slave_set_role(self, role)
    print("Local slave started with ID %d" % self.identity)

  def launch_app(self, app):
    """ Called when the menu app has selected an app to start. """
    print("Slave launching app: %s " % app)
    self.running_app = app

  def master_goto_menu(self):
    print("Client returning to menu")
    if (self.running_app is not None):
      self.running_app.stop()

  def master_start_app(self, appname):
    print("Client starting app %s" % appname)

  def master_shutdown(self):
    print("Client shutting down...")
    self.stop = True

  def run(self, screen):
    """ Non-blocking, run one iteration of whatever you're doing. Return False if stopped, True if running """
    # Run whatever app is in the foreground
    if (not self.stop):
      if (self.running_app is not None):
        terminate = not self.running_app.slave_run(screen)
        if (terminate): self.running_app = None
      else:
        terminate = not self.menu.slave_run(screen)
        if (terminate): self.stop = True
    return not self.stop

