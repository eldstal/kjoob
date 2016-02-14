from twisted.internet.protocol import Factory, ClientFactory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

from master import RemoteMaster
from slave import RemoteSlave

class GameServer(Factory):
  """ Blocking network server. Runs its own main via Twisted's reactor """

  def __init__(self, master, slave, screen, port=5678):
    self.master = master
    self.local_slave = slave
    self.screen = screen
    self.port = port

  def start(self):
    self.endpoint = TCP4ServerEndpoint(reactor, self.port)
    self.endpoint.listen(self)

    # Make sure reactor's main thread calls our main() as well
    reactor.callFromThread(self.main)
    reactor.run()

  def stop(self):
    print("Shutting down server...")
    reactor.stop()

  def main(self):

    if self.local_slave.run(self.screen):
      self.master.run()

      # Schedule another call, at some point in the future
      reactor.callFromThread(self.main)
    else:
      self.stop()

  def buildProtocol(self, addr):
    return RemoteSlave(self.master)


class GameClient(ClientFactory):
  """ Blocking TCP client, connects and runs a LocalSlave """

  def __init__(self, hostname, port, slave, screen):
    self.hostname = hostname
    self.port = port
    self.local_slave = slave
    self.master = None
    self.screen = screen

  def start(self):
    if (self.master is None):
      reactor.connectTCP(self.hostname, self.port, self)
      reactor.run()

  def stop(self):
    print("Shutting down client...")
    reactor.stop()

  def main(self):
    if (self.local_slave.run(self.screen)):
      # Run another iteration of the main loop, later
      reactor.callFromThread(self.main)
    else:
      self.stop()

  def buildProtocol(self, addr):
    self.master = RemoteMaster()
    self.local_slave.set_master(self.master)

    # Make sure we get to take part in the main loop
    reactor.callFromThread(self.main)
    return self.master

