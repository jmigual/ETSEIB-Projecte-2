#!/usr/bin/env python3
# Music Director using Multicast Ethernet
# January 2016
# Manuel Moreno

from time import *
import socket
import struct
from logger import *

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


class PlayNote:
    def __init__(self, time_start=-1, pitch=-1, velocity=-1, duration=-1, takes_off=-1):
        self.time = time_start
        self.pitch = pitch
        self.velocity = velocity
        self.duration = duration
        self.takes_off = takes_off

    def __eq__(self, other):
        print(other.time, other.takes_off, self.time, self.takes_off)
        return self.time == other.time or self.takes_off == other.takes_off

    def get_pitch(self, time_now):
        if time_now == self.time:
            return self.pitch
        elif time_now == self.takes_off:
            return 255
        return 0


class Director:
    """ Fist version using multicast ethernet
    """

    def __init__(self, txt_file):
        self.name = txt_file
        self.tracks = 8
        self.notes = [[]]*self.tracks

        minim = 100
        maxim = 0
        for track in range(self.tracks):
            with open(self.name + str(track) + '.txt') as f:
                for line in f:
                    data = line.split()
                    note = PlayNote()
                    try:
                        note.time = float(data[0])
                    except Exception as e:
                        print(e)
                        print(data)
                        print(track, len(self.notes[track]))
                        print(self.name + str(track) + '.txt')
                    if note.time > maxim:
                        maxim = note.time
                    note.pitch = int(data[1])
                    note.velocity = int(data[2])
                    note.duration = float(data[3])
                    if 0 < note.duration < minim:
                        minim = note.duration
                    note.takes_off = note.time + note.duration
                    self.notes[track].append(note)

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
            time_note = PlayNote(time_start=t, takes_off=t)
            for track in range(self.tracks):
                tx_msg[track] = 0
                note_index = self.notes[track].index(time_note)
                note = self.notes[track][note_index]

                tx_msg[track] = note.get_pitch(t)
                flag |= tx_msg[track] != 0

            if flag:  # new event
                print(t, tx_msg[0], tx_msg[1], tx_msg[2], tx_msg[3], tx_msg[4], tx_msg[5],
                      tx_msg[6], tx_msg[7])
                sent = self.s.sendto(build_can_frame(canid, tx_msg), self.multicast_group)

            sleep(self.step)  # step between notes
            t += self.step

        # Last Message to stop music
        sleep(self.step)
        for track in range(self.tracks):
            tx_msg[track] = 255
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
