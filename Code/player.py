#!/usr/bin/env python3
import fluidsynth
import socket
import struct
import json

from logger import *


class SocketPlayer:
    can_frame_fmt = "=IB3x8s"
    multicast_group = '224.3.29.71'
    server_address = ('', 10000)

    def __init__(self, velocity, track, sfid_path="/usr/share/sounds/sf2/FluidR3_GM.sf2"):
        self.sfid_path = sfid_path.encode("ascii")
        self.fs = fluidsynth.Synth()
        self.fs.start()
        self.fs.program_select(0, self.fs.sfload(self.sfid_path), 0, 0)

        self.logger = logging.getLogger()
        self.velocity = velocity

        # Convert to list if it's not
        try:
            iter(track)
        except TypeError:
            track = [track]
        self.tracks = track

        self.logger.info("Loading Player with SF2 {0}".format(self.sfid_path))
        self.sock = None

    def run(self):
        # Create a socket and bind it to the server address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(SocketPlayer.server_address)
        self.logger.info("Started socket at {0}".format(SocketPlayer.server_address))

        group = socket.inet_aton(SocketPlayer.multicast_group)
        mreq = struct.pack('4sL', group, socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        self.logger.info("Begin listening at multicast {0}".format(SocketPlayer.multicast_group))

        # This is where all the magic happens
        while True:
            self.__wait_and_process()

    def __wait_and_process(self):
        # Blocks until data is received
        data, address = self.sock.recvfrom(1024)
        tracks, notes_in_all, notes_out_all = SocketPlayer.dissect_frame(data)
        self.logger.debug("Received %s bytes from %s", len(data), address[0])

        # Get the note form the data and play it
        for track in self.tracks:
            notes_in = notes_in_all.get(str(track), [])
            for note in notes_in:
                self.logger.info("Playing note: %s", note)
                self.fs.noteon(0, note, self.velocity)

            notes_out = notes_out_all.get(str(track), [])
            for note in notes_out:
                self.logger.debug("Stopping note: %s", note)
                self.fs.noteoff(0, note)

        self.logger.debug("Sending acknowledgment to %s", address)
        self.sock.sendto(b'ack', address)

    @staticmethod
    def dissect_frame(frame):
        msg = json.loads(frame.decode())
        return msg["tracks"], msg["in"], msg["out"]
