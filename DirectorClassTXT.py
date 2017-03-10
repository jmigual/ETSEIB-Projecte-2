#!/usr/bin/env python3
# Music Director using Multicast Ethernet
# January 2016
# Manuel Moreno

from ctypes import *
from time import *
import socket
import struct
import sys

# 8 music voices
# message = identifier, length of data, 8 notes (one per instrument)
# note = 0 means hold the last note
# note = 255 means silence, stop the last note


dim = 1000
can_frame_fmt = "=IB3x8s"


def build_can_frame(can_id, data):
    can_dlc = len(data)
    data = data.ljust(8, b'\x00')
    return struct.pack(can_frame_fmt, can_id, can_dlc, data)


class Director:
    """ Fist version using multicast ethernet
    """

    def __init__(self, txt_file):
        self.name = txt_file
        self.tracks = 8
        self.t = [[-1 for x in range(dim)] for x in range(self.tracks)]  # time
        self.n = [[-1 for x in range(dim)] for x in range(self.tracks)]  # note
        self.v = [[-1 for x in range(dim)] for x in range(self.tracks)]  # velocity
        self.d = [[-1 for x in range(dim)] for x in range(self.tracks)]  # duration
        self.takes_off = [[-1 for x in range(dim)] for x in range(self.tracks)]  # off

        minim = 100
        maxim = 0
        for i in range(self.tracks):
            j = 0
            with open(self.name + str(i) + '.txt') as f:
                for line in f:
                    data = line.split()
                    try:
                        self.t[i][j] = float(data[0])
                    except Exception as e:
                        print(e)
                        print(data)
                        print(i, j)
                        print(self.name + str(i) + '.txt')
                    if self.t[i][j] > maxim:
                        maxim = self.t[i][j]
                    self.n[i][j] = int(data[1])
                    self.v[i][j] = int(data[2])
                    self.d[i][j] = float(data[3])
                    if 0 < self.d[i][j] < minim:
                        minim = self.d[i][j]
                    self.takes_off[i][j] = self.t[i][j] + self.d[i][j]
                    j += 1

        self.step = minim

        self.t_end = maxim
        print(self.t_end)
        print(self.step)

        # create a raw socket
        print("Init Multicast socket")
        self.multicast_group = ('224.0.0.1', 10000)
        # Create the datagram socket
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Set a timeout so the socket does not block indefinitely when trying
        # to receive data.
        self.s.settimeout(0.2)
        # Set the time-to-live for messages to 1 so they do not go past the
        # local network segment.
        ttl = struct.pack('b', 1)
        self.s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    def play(self):
        tx_msg = bytearray(8)
        canid = 0x100
        dlc = self.tracks
        t = 0
        print("Playing...")
        while t < self.t_end:
            flag = False
            for i in range(self.tracks):
                tx_msg[i] = 0
                if t in self.t[i]:  # note on
                    tx_msg[i] = self.n[i][self.t[i].index(t)]
                    flag = True
                if t in self.takes_off[i] and tx_msg[i] == 0:
                    tx_msg[i] = 255  # note off
                    flag = True

            if flag:  # new event
                print(t, tx_msg[0], tx_msg[1], tx_msg[2], tx_msg[3], tx_msg[4], tx_msg[5], tx_msg[6], tx_msg[7])
                sent = self.s.sendto(build_can_frame(canid, tx_msg), self.multicast_group)

            sleep(self.step)  # step between notes
            t += self.step

        # Last Message to stop music
        sleep(self.step)
        for i in range(self.tracks):
            tx_msg[i] = 255
        sent = self.s.sendto(build_can_frame(canid, tx_msg), self.multicast_group)
        print("Play Over")
        self.s.close()


if __name__ == '__main__':
    dir1 = Director('sheets/BachConcerto')
    dir1.play()
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("End of execution")
