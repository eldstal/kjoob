class App:
  """
  An application that can be started from the menu
  """

  def __init__(self):
    self.stop = False

  def slave_run(self, screen):
    """ Non-blocking main-loop kernel of the slave-side application. Return True to keep running or False to terminate """
    return not self.stop

  def master_run(self):
    """ Non-blocking main-loop kernel of the master-side application. Return True to keep running or False to terminate """
    return not self.stop

  def master_event(self, ev):
    """ Master-side application event handler. Called once for every event the master registers while running this app """
    return None

  def shutdown(self):
    """ Signal that a shutdown is happening. run() will be called until it returns False, but finish quickly! """
    self.stop = True

