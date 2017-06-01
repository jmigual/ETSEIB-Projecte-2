#!/usr/bin/env python3

import argparse

import player
from logger import *


def main():
    parser = argparse.ArgumentParser(description="Play some music with network orchestra")
    parser.add_argument("-t", "--tracks", default=[0], nargs="+", type=int, metavar="t",
                        help="Tracks to be played by this player")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode logging")
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Starting in DEBUG mode")
    logging.info("Playing tracks: " + ",".join(map(str, args.tracks)))

    # Start playing
    sock_player = player.SocketPlayer(track=args.tracks)
    sock_player.run()


if __name__ == "__main__":
    set_default_logger("player.log")
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Shutting down Client, Thanks for the ride!")
