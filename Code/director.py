#!/usr/bin/env python3
# Music Director using Multicast Ethernet
# January 2016
# Manuel Moreno

from time import *
import socket
import struct
import bisect
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
    def __init__(self, time_start=-1., pitch=-1, velocity=-1, duration=-1.):
        self.pitch = pitch
        self.velocity = velocity
        self.duration = duration
        self.time = time_start
        self.time_start = time_start
        self.time_off = time_start + duration

    def __eq__(self, other):
        return self.time == other.time

    def __lt__(self, other):
        return self.time < other.time

    def __gt__(self, other):
        return self.time > other.time

    def __str__(self):
        return "From: " + str(self.time_start) + " To: " + str(self.time_off) + " Note: " + str(self.pitch)

    def to_off(self):
        """ Change the sorting value to the time_off
        """
        self.time = self.time_off
    __repr__ = __str__

class Director:
    """ Fist version using multicast ethernet
    """

    def __init__(self, txt_file):
        self.name = txt_file
        self.tracks = 8
        self.notes = [[] for i in range(self.tracks)]
        self.notes_playing = [[] for i in range(self.tracks)]

        minim = 100
        maxim = 0
        for track in range(self.tracks):
            with open(self.name + str(track) + '.txt') as f:
                for line in f:
                    data = line.split()
                    try:
                        note = PlayNote(float(data[0]), int(data[1]), int(data[2]), float(data[3]))
                    except Exception as e:
                        print(e)
                        print(data)
                        print(track, len(self.notes[track]))
                        print(self.name + str(track) + '.txt')
                    if note.time > maxim:
                        maxim = note.time
                    if 0. < note.duration < minim:
                        minim = note.duration
                    #print("Note:",note)
                    self.notes[track].append(note)
                #self.notes[track].sort()

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
        #print(str(self.notes[0]).replace(",", "\n"))

    def play(self):
        tx_msg = bytearray(8)
        canid = 0x100
        dlc = self.tracks
        t = 0
        print("Playing...")
        while t < self.t_end:
            flag = False
            for track in range(self.tracks):
                tx_msg[track] = 0
                if self.notes[track] and self.notes[track][0].time_start <= t:
                    # Send the note
                    note = self.notes[track].pop(0)
                    tx_msg[track] = note.pitch

                    # Remove the note and add it to the playing notes
                    note.to_off()
                    bisect.insort_left(self.notes_playing[track], note)

                if self.notes_playing[track] and self.notes_playing[track][0].time_off <= t and tx_msg[track] == 0:
                    # Stop playing the note
                    self.notes_playing[track].pop(0)
                    tx_msg[track] = 255

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
