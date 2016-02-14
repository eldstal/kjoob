import pygame
import ujson
from twisted.internet.protocol import Protocol

from master import Master
from menu import *

class Slave:

  def __init__(self):
    self.master = Master() # This is a dummy.

  def describe(self):
    """ Descriptive string of this particular slave """
    return "Dummy Slave"

  def set_master(self, master):
    """ Must be called before anything else. """
    self.master = master
    master.slave_register(self)

  def master_goto_menu(self):
    """ Called by the master to show the menu. Any running app is shut down. """
    print("Dummy slave goto_menu")

  def master_start_app(self, app_id):
    """ Called by the master to start an application and pass control to it """
    print("Dummy slave start_app %d" % app_id)

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


class RemoteSlave(Slave, Protocol):
  """
  A remotely connected slave. (exists only on the master side)
  Assign it an incoming connection and set_master() with a LocalMaster,
  it will decode messages and call functions on its Master.
  """
  def __init__(self, master):
    Slave.__init__(self)
    self.pending_master = master
    print("Remote slave initialized.")

  def describe(self):
    """ Descriptive string of this particular slave """
    return self.transport.getPeer()

  def connectionMade(self):
    self.set_master(self.pending_master)

  def dataReceived(self, data):
    # Incoming message from the slave
    utf = data.decode("UTF-8")
    for json in utf.split("\xef"):
      try:
        print("Master received: %s" % utf)
        payload = ujson.loads(utf)
        self.master.slave_message(self, payload)
      except:
        sys.stdout.write("Invalid message received.")

  def master_goto_menu(self):
    self.master_message({"app":0, "msg":10})

  def master_start_app(self, app_id):
    self.master_message({"app":0, "msg":11, "data": app_id})

  def slave_register(self, slave):
    self.slave = slave

  def master_message(self, msg):
    payload = ujson.dumps(msg) + "\xef"   # Delimiter character
    clean = payload.encode("UTF-8")
    self.transport.write(clean)


class LocalSlave(Slave):
  """
  Actual slave logic.
  Interacts with a remote or local master, draws the context etc.
  """
  def __init__(self, role, app_conf):
    super().__init__()
    self.conf = app_conf
    self.role = role
    self.running_app = None
    self.stop = False
    self.menu = MenuSlave(self)

  def describe(self):
    return "Local"

  def launch_app(self, app):
    """ Called when the menu app has selected an app to start. """
    print("Slave launch_app: %s " % app)
    self.running_app = app(owner=self)

  def master_goto_menu(self):
    print("Client returning to menu")
    if (self.running_app is not None):
      self.running_app.shutdown()

  def master_start_app(self, app_id):
    if (self.running_app is None or
        self.running_app.app_id != app_id):
      print("Slave start_app %d" % app_id)
      app = App.get_slave_app(app_id)
      self.running_app = app(owner=self)

  def master_shutdown(self):
    print("Client shutting down...")
    self.stop = True

  def master_message(self, msg):
    appid = msg['app']
    if self.running_app is not None:
      if (appid == self.running_app.app_id or appid == 0):
        self.running_app.message(msg)
    elif (appid == self.menu.app_id):
      self.menu.message(msg)
    else:
      print("Slave ignoring message sent to non-running app.")

  def send_message(self, msg):
    """ Send message to the master """
    self.master.slave_message(self, msg)

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

