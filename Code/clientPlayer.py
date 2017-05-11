#!/usr/bin/env python3

import getopt
import sys

import player
from logger import *


def usage():
    print("clientPlayer -t number [-v number]")
    print("-t track number")
    print("-v volume")
    print("-d set debug mode")


def main():
    logger = logging.getLogger()

    try:
        opts, args = getopt.gnu_getopt(sys.argv, "t:dv:")
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(1)

    track = [0]
    velocity = 40

    for o, a in opts:
        if o == "-t":
            track = [int(x) for x in a.split(",")]
        elif o == "-v":
            velocity = int(a)
        elif o == "-d":
            logger.setLevel(logging.DEBUG)
            logger.debug("Starting debug mode")
        else:
            logger.error("Unknown option {0}", o)

    logger.info("Playing tracks: " + ",".join(map(str, track)))

    # Start playing
    sock_player = player.SocketPlayer(track=track, velocity=velocity)
    sock_player.run()


if __name__ == "__main__":
    set_default_logger("player.log")
    try:
        main()
    except KeyboardInterrupt:
        logging.getLogger().info("Shutting down, Thanks for the ride!")
