#!/usr/bin/env python3
#
#
# Main executable for all monitors.
# Provide --role (north, east, south or west) to indicate which of the four directions to display
# Provide --master <port> to run as a master ("server") instance
# Provide --slave <hostname>:<port> to run as a slave instance, connecting to a master


import os
import argparse
import pygame

from master import LocalMaster
from slave import LocalSlave

def setup_screen(conf):

  # Set up our game window
  # Pygame doesn't set window position programmatically. We have to hack it via an SDL environment variable. Wow.
  # This doesn't actually seem to work.
  os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (conf.xpos, conf.ypos)

  pygame.init()

  flags = 0
  if (conf.fullscreen):
    flags = pygame.FULLSCREEN

  screen = pygame.display.set_mode((conf.width, conf.height), flags)

  return screen

def main():
  parser = argparse.ArgumentParser(description="The Kjoob UI/Games for a single screen. Default is a game master on port 5678 displaying North.")

  parser.add_argument('-r', '--role', default='north', choices=['north', 'east', 'south', 'west'],
                      help="The screen direction of this game instance.")

  parser.add_argument('-m', '--master', metavar='port', type=int,
                      help="Act as a master, listning for slave connection on the provided port number")

  parser.add_argument('-s', '--slave', metavar='hostname:port',
                      help="Act as a slave, connecting to the named master")

  parser.add_argument('-W', '--width', default=320, type=int,
                      help="Width of the game window")

  parser.add_argument('-H', '--height', default=240, type=int,
                      help="Height of the game window")

  parser.add_argument('-x', '--xpos', default=0, type=int,
                      help="X location of the game window")

  parser.add_argument('-y', '--ypos', default=0, type=int,
                      help="Y location of the game window")

  parser.add_argument('-f', '--fullscreen', action='store_true',
                      help="Start in fullscreen mode")

  conf = parser.parse_args()

  # By default, act as master
  if (not conf.master and not conf.slave):
    conf.master = 5678

  # Without a direction, act as north
  if (not conf.role):
    conf.role = "north"

  screen = setup_screen(conf)

  if (conf.master):
    master = LocalMaster(conf.master)
    slave = LocalSlave(conf.role, master, conf)

    master.goto_menu()

    while slave.run(screen):
      master.run()

  if (conf.slave):
    # TODO: Connect to a remote master, then pass that to a LocalSlave
    pass

if __name__ == '__main__':
  main()
