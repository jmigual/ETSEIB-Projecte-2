#!/usr/bin/env python3

import socket
import sys
import struct
import logging
import getopt
import fluidsynth
import player

can_frame_fmt = "=IB3x8s"
multicast_group = '224.3.29.71'
server_address = ('', 10000)


def dissect_can_frame(frame):
    can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame)
    return can_id, can_dlc, data[:can_dlc]


def usage():
    print("clientPlayer -i number [-v number]")
    print("-i track number")
    print("-v volume")
    print("-d set debug mode")


def get_default_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formater = logging.Formatter("[%(asctime)s] (%(levelname)s) %(message)s")
    handler_s = logging.StreamHandler()
    handler_f = logging.FileHandler("info.log")
    handler_s.setFormatter(formater)
    handler_f.setFormatter(formater)
    logger.addHandler(handler_s)
    logger.addHandler(handler_f)
    return logger


def main():
    logger = get_default_logger()

    try:
        opts, args = getopt.gnu_getopt(sys.argv, "")
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(1)

    track = 0

    logging.basicConfig(filename="info.log", level=logging.DEBUG,
                        format="[%(asctime)s] (%(levelname)s) %(message)s")

    # Create a socket and bind it to the server address
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(server_address)
    logging.info("Started socket at {0}".format(server_address))

    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    logging.info("Begin listening at multicast {0}".format(multicast_group))

    while True:
        data, address = sock.recvfrom(1024)
        canidenrx, dlcrx, rx_msg = dissect_can_frame(data)
        logging.debug("Received {0} bytes from {1}", (len(data), address))
        note = rx_msg[track]
        logging.debug("Playing note: {0}".format(note))
        play_note(note)


if __name__ == "__main__":
    main()
