#!/usr/bin/env python3
#
#
# Main executable for all monitors.
# Provide --role (north, east, south or west) to indicate which of the four directions to display
# Provide --master <port> to run as a master ("server") instance
# Provide --slave <hostname>:<port> to run as a slave instance, connecting to a master


import os
import argparse

def main():
	parser = argparse.ArgumentParser(description="The Kjoob UI/Games for a single screen. Default is a game master on port 5678 displaying North.")

	parser.add_argument('-r', '--role', default='north', choices=['north', 'east', 'south', 'west'],
											help="The screen direction of this game instance.")

	parser.add_argument('-m', '--master', metavar='port', type=int,
											help="Act as a master, listning for slave connection on the provided port number")

	parser.add_argument('-s', '--slave', metavar='hostname:port',
											help="Act as a slave, connecting to the named master")

	conf = parser.parse_args()

	# By default, act as master
	if (not conf.master and not conf.slave):
		conf.master = 5678

	# Without a direction, act as north
	if (not conf.role):
		conf.role = "north"


if __name__ == '__main__':
	main()
