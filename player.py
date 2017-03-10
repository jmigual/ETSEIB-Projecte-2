#!/usr/bin/env python3
import threading
import time
import fluidsynth

class PlayNote:
    def __init__(self, begin, end, note, velocity):
        self.begin = begin
        self.end = end
        self.note = note
        self.velocity = velocity

class MidiPlayer(threading.Thread):

    def __init__(self, **kwargs):
        super(MidiPlayer, self).__init__(kwargs=kwargs)
        self.notes = []
        self.cLock = threading.Condition()

    def play(self, time, instrument, note, duration, velocity = 40):
        """
        Plays a note during a certain time
        :param instrument: Instrument to be played
        :param note: Note to be played according to midi notes
        :param duration: Duration of the note to be played
        :param velocity: Velocity of the note, is directly proportional to the note's volume
        :return: None
        """
        self.cLock.acquire()
        self.notes.append(PlayNote())


def main():
    print("Hello world")

if __name__ == "__main__":
    main()
