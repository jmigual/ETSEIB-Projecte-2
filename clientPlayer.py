#!/usr/bin/env python3

import socket
import sys
import struct
import logging

can_frame_fmt = "=IB3x8s"
multicast_group = '224.3.29.71'
server_address = ('', 10000)


def dissect_can_frame(frame):
    can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame)
    return can_id, can_dlc, data[:can_dlc]


def main():
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


if __name__ == "__main__":
    main()
