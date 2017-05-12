#!/usr/bin/env python3

import argparse

import player
from logger import *


def main():
    logger = logging.getLogger()

    parser = argparse.ArgumentParser(description="Play some music with network orchestra")
    parser.add_argument("-t", "--tracks", default=[0], nargs="+", type=int, metavar="t",
                        help="Tracks to be played by this player")
    parser.add_argument("-v", "--velocity", default=127, type=int, metavar="v",
                        help="Velocity (volume) to use when playing")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode logging")
    args = parser.parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Starting in DEBUG mode")
    logger.info("Playing tracks: " + ",".join(map(str, args.tracks)))

    # Start playing
    sock_player = player.SocketPlayer(track=args.tracks, velocity=args.velocity)
    sock_player.run()


if __name__ == "__main__":
    set_default_logger("player.log")
    try:
        main()
    except KeyboardInterrupt:
        logging.getLogger().info("Shutting down, Thanks for the ride!")
