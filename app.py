class App:
  """
  Things common to both Master-side and Slave-side apps.
  Don't inherit this, inherit MasterApp or SlaveApp instead!
  """

  # Book-keeping for globally assigned app ids
  next_app_id = 0   # 0 is for global things.
  known_apps = {}   # app_id : (masterclass, slaveclass, metadata)

  def __init__(self, owner):
    self.owner = owner
    self.stop = False
    self.transport = owner
    self.app_id = App.get_app_id(type(self))
    self.name = App.get_app_name(self.app_id)
    print("This app (%s) has id %d." % (type(self), self.app_id))

  @staticmethod
  def get_app_id(appclass):
    for (i, (m,s,metadata)) in App.known_apps.items():
      if (m == appclass or s == appclass): return i
    return None

  @staticmethod
  def get_app_name(appid):
    if (appid in App.known_apps):
      (m,s,metadata) = App.known_apps[appid]
      return metadata["name"]

  @staticmethod
  def register_app(masterclass, slaveclass, name="Unnamed"):
    """ Register a new app globally, assigning it an ID that must be the same on master and all slaves. """
    old_id = App.get_app_id(masterclass)
    if (old_id is not None): return old_id

    App.next_app_id += 1

    metadata = {}
    metadata["name"] = name
    metadata["app_id"] = App.next_app_id

    App.known_apps[App.next_app_id] = (masterclass, slaveclass, metadata)
    return App.next_app_id

  @staticmethod
  def get_slave_app(app_id):
    (m, s, metadata) = App.known_apps[app_id]
    return s

  @staticmethod
  def get_master_app(app_id):
    (m, s, metadata) = App.known_apps[app_id]
    return m

  @staticmethod
  def get_all_apps():
    """
      Return a list of apps, excluding the menu app
      Return value is a list. 
      Each item is an app's metadata dictionary
    """
    ret = [ metadata for i, (m, s, metadata) in App.known_apps.items() ]
    return ret

  def set_transport(self, transport):
    """ Register an object with a send_message(msg) method """
    self.transport = transport

  def send_message(self, msg):
    """ Send a message to the corresponding MasterApp or to all connected SlaveApps. """
    if (self.transport is not None): self.transport.send_message(msg)

  def event(self, ev):
    """ Application event handler. ev is pygame event """
    return None

  def message(self, msg):
    """ Application message handler. msg is a net message"""
    return None

  def shutdown(self):
    """ Signal that a shutdown is happening. run() will be called until it returns False, but finish quickly! """
    self.stop = True

class MasterApp(App):
  """
  The Master-side half of an application
  """

  def __init__(self, owner):
    super().__init__(owner)

  def run(self):
    """ Non-blocking main-loop kernel of the master-side application. Return True to keep running or False to terminate """
    return not self.stop


class SlaveApp(App):
  """
  The Slave-side half of an application
  """
  def __init__(self, owner):
    super().__init__(owner)

  def run(self, screen):
    """ Non-blocking main-loop kernel of the slave-side application. Return True to keep running or False to terminate """
    return not self.stop


