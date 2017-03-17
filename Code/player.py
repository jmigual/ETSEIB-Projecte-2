#!/usr/bin/env python3
import fluidsynth
import socket
import struct
import time

from logger import *


class SocketPlayer:
    can_frame_fmt = "=IB3x8s"
    multicast_group = '224.3.29.71'
    server_address = ('', 10000)

    def __init__(self, velocity, track):
        self.logger = logging.getLogger()
        self.velocity = velocity
        self.track = track

        self.midi_player = MidiPlayer()
        self.logger.info("Loading MidiPlayer with SF2 {0}".format(self.midi_player.sfid_path))

        # Create a socket and bind it to the server address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(SocketPlayer.server_address)
        self.logger.info("Started socket at {0}".format(SocketPlayer.server_address))

    def run(self):
        group = socket.inet_aton(SocketPlayer.multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.logger.info("Begin listening at multicast {0}".format(SocketPlayer.multicast_group))

        # This is where all the magic happens
        while True:
            self.__wait_and_proces()

    def __wait_and_proces(self):
        # Blocks until data is received
        data, address = self.sock.recvfrom(1024)
        canidenrx, dlcrx, rx_msg = SocketPlayer.dissect_can_frame(data)
        self.logger.debug("Received {0} bytes from {1}", (len(data), address))

        # Get the note form the data and play it
        note = rx_msg[self.track]
        self.logger.debug("Playing note: {0}".format(note))
        self.midi_player.play(note, self.velocity)

    @staticmethod
    def dissect_can_frame(frame):
        can_id, can_dlc, data = struct.unpack(SocketPlayer.can_frame_fmt, frame)
        return can_id, can_dlc, data[:can_dlc]


class MidiPlayer:

    def __init__(self, sfid_path="/usr/share/sounds/sf2/FluidR3_GM.sf2"):
        self.__playing_note = None
        self.sfid_path = sfid_path.encode("ascii")
        self.fs = fluidsynth.Synth()
        self.fs.start()
        sfid = self.fs.sfload(self.sfid_path)
        self.fs.program_select(0, sfid, 0, 0)

    def play(self, note, velocity=40):
        if note == 0:
            return
        if note == 255 and not self.__playing_note is None:
            self.fs.noteoff(0, self.__playing_note)
            self.__playing_note = None
        else:
            self.fs.noteon(0, note, velocity)


def main():
    player = MidiPlayer()
    player.play(40)
    time.sleep(1)
    player.play(0)
    time.sleep(0.2)
    player.play(40)
    time.sleep(1)
    player.play(0)
    time.sleep(0.2)
    player.play(40)
    time.sleep(1)
    player.play(0)
    time.sleep(0.2)

if __name__ == "__main__":
    main()
