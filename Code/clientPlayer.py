#!/usr/bin/env python3

import socket
import sys
import struct
import logging
import getopt
import player


def get_default_logger():
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(asctime)s] (%(levelname)s) %(message)s")
    handler_s = logging.StreamHandler()
    handler_f = logging.FileHandler("info.log")
    handler_s.setFormatter(formatter)
    handler_f.setFormatter(formatter)
    log.addHandler(handler_s)
    log.addHandler(handler_f)
    return log


can_frame_fmt = "=IB3x8s"
multicast_group = '224.3.29.71'
server_address = ('', 10000)
logger = get_default_logger()


def dissect_can_frame(frame):
    can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame)
    return can_id, can_dlc, data[:can_dlc]


def usage():
    print("clientPlayer -i number [-v number]")
    print("-i track number")
    print("-v volume")
    print("-d set debug mode")


def main():
    global logger

    try:
        opts, args = getopt.gnu_getopt(sys.argv, "")
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(1)

    track = 0
    velocity = 40

    for o, a in opts:
        if o == "-i":
            track = int(a)
        elif o == "v":
            velocity = int(a)
        elif o == "d":
            logger.setLevel(logging.DEBUG)
            logger.debug("Starting debug mode")
        else:
            logger.error("Unknown option {0}", o)

    midi_player = player.MidiPlayer()
    logger.info("Loading MidiPlayer with SF2 {0}".format(midi_player.sfid_path))

    # Create a socket and bind it to the server address
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    logger.info("Started socket at {0}".format(server_address))

    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    logger.info("Begin listening at multicast {0}".format(multicast_group))

    # This is where all the magic happens
    while True:
        # Blocks until data is received
        data, address = sock.recvfrom(1024)
        canidenrx, dlcrx, rx_msg = dissect_can_frame(data)
        logger.debug("Received {0} bytes from {1}", (len(data), address))

        # Get the note form the data and play it
        note = rx_msg[track]
        logger.debug("Playing note: {0}".format(note))
        midi_player.play(note, velocity)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Shutting down thanks for the ride")
