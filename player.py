#!/usr/bin/env python3
import fluidsynth
import time


class MidiPlayer:

    def __init__(self, sfid_path="/usr/share/sounds/sf2/FluidR3_GM.sf2"):
        self.__playing_note = None
        self.fs = fluidsynth.Synth()
        self.fs.start()
        sfid = self.fs.sfload(sfid_path)
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
