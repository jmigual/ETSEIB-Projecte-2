import time
import mido


# The default tempo is 120 BPM.
# (500000 microseconds per beat (quarter note).)
DEFAULT_TEMPO = 500000
DEFAULT_TICKS_PER_BEAT = 480


def to_abstime(messages, i):
    now = 0
    for msg in messages:
        now += msg.time
        yield msg.copy(time=now), i


def merge_tracks(tracks):
    messages = []
    for i, track in tracks:
        messages.extend(to_abstime(track, i))

    messages.sort(key=lambda x: x[0].time)
    return messages


class DirectorMidiFile(mido.MidiFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __iter__(self):
        if self.type == 2:
            raise TypeError("can't merge tracks in type 2 (asynchronous) file")

        tempo = DEFAULT_TEMPO
        for msg, track in merge_tracks(self.tracks):
            # Convert message time from absolute time
            # in ticks to relative time in seconds.
            if msg.time > 0:
                delta = mido.tick2second(msg.time, self.ticks_per_beat, tempo)
            else:
                delta = 0

            yield msg.copy(time=delta), track

            if msg.type == 'set_tempo':
                tempo = msg.tempo

    def play_tracks(self, meta_messages=False):
        sleep = time.sleep

        for msg, track in self:
            sleep(msg.time)

            if isinstance(msg, mido.MetaMessage) and not meta_messages:
                continue
            else:
                yield msg, track
