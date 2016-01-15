import pygame

from menu import Menu

class Master:
  """
  The game master, which coordinates connections from both local and remote slaves
  """
  def __init__(self):
    pass

  def slave_register(self, slave):
    """ Called by new slaves to receive an ID """
    pass

  def slave_set_role(self, slave, role):
    """ Called by slaves to set their role (screen direction) """
    pass


class RemoteMaster(Master):
  """
  A remote master (exists only on the slave side)
  Initialize an object of this class to connect to the server
  Then call add_slave to set the local slave that this connection serves
  """
  def __init__(self, hostname, port):
    super.__init__()
    pass

  def slave_register(self, slave):
    # TODO: Send message
    # TODO: Return a unique identity
    return -2

  def slave_set_role(self, slave):
    # TODO: Send message
    pass


class LocalMaster(Master):
  """
  Actual master logic.
  Interacts with local or remote Slave objects to keep state consistent across screens
  """
  def __init__(self, port):
    super().__init__()
    print("Local Master initialized")
    self.slaves = []
    self.next_identity = 0
    self.menu = Menu(self)
    self.running_app = self.menu

  def shutdown(self):
    for s in self.slaves:
      s.master_shutdown()

  def launch_app(self, app):
    """ Called when the menu app has selected an app to start. Will also be called on slaves automatically. """
    print("Master launching app: %s " % app)
    if (app is not None):
      self.running_app = app
    else:
      self.running_app = self.menu

  def goto_menu(self):
    """ Command all slaves to start or return to the main menu """
    self.running_app = self.menu
    for s in self.slaves:
      s.master_goto_menu()

  def slave_register(self, slave):
    self.next_identity += 1
    self.slaves.append(slave)
    print("Slave registered with ID %d" % self.next_identity)
    return self.next_identity

  def slave_set_role(self, slave, role):
    slave.role = role

  def run(self):

    # Handle local events, such as user input. Master is the only one to see these.
    for ev in pygame.event.get():
      if (ev.type == pygame.QUIT):
        self.shutdown()
      self.running_app.master_event(ev)

    terminate = not self.running_app.master_run()
    if (terminate):
      if (self.running_app == self.menu):
        shutdown()
      else:
        self.running_app = self.menu
