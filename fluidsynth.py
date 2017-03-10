"""
=============
pyFluidSynth
=============
Python bindings for FluidSynth

Author: Nathan Whitehead
Contact: nwhitehe@gmail.com
Version: 0.7
Date: 2015-02-24

Copyright 2008--2015, Nathan Whitehead <nwhitehe@gmail.com>
Released under the LGPL

This module contains python bindings for FluidSynth.  FluidSynth is a
software synthesizer for generating music.  It works like a MIDI
synthesizer.  You load patches, set parameters, then send NOTEON and
NOTEOFF events to play notes.  Instruments are defined in SoundFonts,
generally files with the extension SF2.  FluidSynth can either be used
to play audio itself, or you can call a function that returns chunks
of audio data and output the data to the soundcard yourself.
FluidSynth works on all major platforms, so pyFluidSynth should also.
"""

from ctypes import *
from ctypes.util import find_library
import os


# A short circuited or expression to find the FluidSynth library
# (mostly needed for Windows distributions of libfluidsynth supplied with QSynth)

lib = find_library('fluidsynth') or \
      find_library('libfluidsynth') or \
      find_library('libfluidsynth-1')

if lib is None:
    raise ImportError("Couldn't find the FluidSynth library.")
else:
    print(lib)

# Dynamically link the FluidSynth library
_fl = CDLL(lib)


# Helper function for declaring function prototypes
def cfunc(name, result, *args):
    """Build and apply a ctypes prototype complete with parameter flags
    :rtype : object
    """
    atypes = []
    aflags = []
    for arg in args:
        atypes.append(arg[1])
        aflags.append((arg[2], arg[0]) + arg[3:])
    return CFUNCTYPE(result, *atypes)((name, _fl), tuple(aflags))


# Bump this up when changing the interface for users
api_version = '1.2'


# Function prototypes for C versions of functions
new_fluid_settings = cfunc('new_fluid_settings', c_void_p)

new_fluid_synth = cfunc('new_fluid_synth', c_void_p,
                        ('settings', c_void_p, 1))

new_fluid_audio_driver = cfunc('new_fluid_audio_driver', c_void_p,
                               ('settings', c_void_p, 1),
                               ('synth', c_void_p, 1))

fluid_settings_setstr = cfunc('fluid_settings_setstr', c_int,
                              ('settings', c_void_p, 1),
                              ('name', c_char_p, 1),
                              ('str', c_char_p, 1))

fluid_settings_setnum = cfunc('fluid_settings_setnum', c_int,
                              ('settings', c_void_p, 1),
                              ('name', c_char_p, 1),
                              ('val', c_double, 1))

fluid_settings_setint = cfunc('fluid_settings_setint', c_int,
                              ('settings', c_void_p, 1),
                              ('name', c_char_p, 1),
                              ('val', c_int, 1))

delete_fluid_audio_driver = cfunc('delete_fluid_audio_driver', None,
                                  ('driver', c_void_p, 1))

delete_fluid_synth = cfunc('delete_fluid_synth', None,
                           ('synth', c_void_p, 1))

delete_fluid_settings = cfunc('delete_fluid_settings', None,
                              ('settings', c_void_p, 1))

fluid_synth_sfload = cfunc('fluid_synth_sfload', c_int,
                           ('synth', c_void_p, 1),
                           ('filename', c_char_p, 1),
                           ('update_midi_presets', c_int, 1))

fluid_synth_sfunload = cfunc('fluid_synth_sfunload', c_int,
                             ('synth', c_void_p, 1),
                             ('sfid', c_int, 1),
                             ('update_midi_presets', c_int, 1))

fluid_synth_program_select = cfunc('fluid_synth_program_select', c_int,
                                   ('synth', c_void_p, 1),
                                   ('chan', c_int, 1),
                                   ('sfid', c_int, 1),
                                   ('bank', c_int, 1),
                                   ('preset', c_int, 1))

fluid_synth_noteon = cfunc('fluid_synth_noteon', c_int,
                           ('synth', c_void_p, 1),
                           ('chan', c_int, 1),
                           ('key', c_int, 1),
                           ('vel', c_int, 1))

fluid_synth_noteoff = cfunc('fluid_synth_noteoff', c_int,
                            ('synth', c_void_p, 1),
                            ('chan', c_int, 1),
                            ('key', c_int, 1))

fluid_synth_pitch_bend = cfunc('fluid_synth_pitch_bend', c_int,
                               ('synth', c_void_p, 1),
                               ('chan', c_int, 1),
                               ('val', c_int, 1))

fluid_synth_cc = cfunc('fluid_synth_cc', c_int,
                       ('synth', c_void_p, 1),
                       ('chan', c_int, 1),
                       ('ctrl', c_int, 1),
                       ('val', c_int, 1))

fluid_synth_program_change = cfunc('fluid_synth_program_change', c_int,
                                   ('synth', c_void_p, 1),
                                   ('chan', c_int, 1),
                                   ('prg', c_int, 1))

fluid_synth_bank_select = cfunc('fluid_synth_bank_select', c_int,
                                ('synth', c_void_p, 1),
                                ('chan', c_int, 1),
                                ('bank', c_int, 1))

fluid_synth_sfont_select = cfunc('fluid_synth_sfont_select', c_int,
                                 ('synth', c_void_p, 1),
                                 ('chan', c_int, 1),
                                 ('sfid', c_int, 1))

fluid_synth_program_reset = cfunc('fluid_synth_program_reset', c_int,
                                  ('synth', c_void_p, 1))

fluid_synth_system_reset = cfunc('fluid_synth_system_reset', c_int,
                                 ('synth', c_void_p, 1))

fluid_synth_write_s16 = cfunc('fluid_synth_write_s16', c_void_p,
                              ('synth', c_void_p, 1),
                              ('len', c_int, 1),
                              ('lbuf', c_void_p, 1),
                              ('loff', c_int, 1),
                              ('lincr', c_int, 1),
                              ('rbuf', c_void_p, 1),
                              ('roff', c_int, 1),
                              ('rincr', c_int, 1))

fluid_synth_get_polyphony = cfunc('fluid_synth_get_polyphony', c_int,
                                  ('synth', c_void_p, 1))

fluid_synth_set_polyphony = cfunc('fluid_synth_set_polyphony', c_int,
                                  ('synth', c_void_p, 1),
                                  ('polyphony', c_int, 1))

fluid_synth_get_active_voice_count = cfunc('fluid_synth_get_active_voice_count', c_int,
                                           ('synth', c_void_p, 1))

fluid_synth_get_gain = cfunc('fluid_synth_get_gain', c_float,
                             ('synth', c_void_p, 1))

fluid_synth_set_gain = cfunc('fluid_synth_set_gain', c_void_p,
                             ('synth', c_void_p, 1),
                             ('gain', c_float, 1))

fluid_synth_get_cpu_load = cfunc('fluid_synth_get_cpu_load', c_double,
                                 ('synth', c_void_p, 1))


# This adds an Struct-like info variable to be used in fluid_synth_get_channel_info
class ChannelInfo(Structure):
    _fields_ = [
        ('assigned', c_int),
        ('sfont_id', c_int),
        ('bank', c_int),
        ('program', c_int),
        ('name', c_char * 32),
        ('reserved', c_char * 32),
    ]


fluid_get_stdout = cfunc('fluid_get_stdout', c_int)

new_fluid_cmd_handler = cfunc('new_fluid_cmd_handler', c_void_p,
                              ('synth', c_void_p, 1))

fluid_command = cfunc('fluid_command', c_int,
                      ('handler', c_void_p, 1),
                      ('cmd', c_char_p, 1),
                      ('out', c_int, 1))

fluid_synth_get_channel_info = cfunc('fluid_synth_get_channel_info', c_int,
                                     ('synth', c_void_p, 1),
                                     ('chan', c_int, 1),
                                     ('info', POINTER(ChannelInfo), 1))


# Create a new MIDI driver instance.
new_fluid_midi_driver = cfunc('new_fluid_midi_driver', c_void_p,
                              ('settings', c_void_p, 1),
                              ('handler', c_void_p, 1),
                              ('event_handler_data', c_void_p, 1))

# Delete a MIDI driver instance.
delete_fluid_midi_driver = cfunc('delete_fluid_midi_driver', c_void_p,
                                 ('driver', c_void_p, 1))

fluid_synth_handle_midi_event = cfunc('fluid_synth_handle_midi_event', c_int,
                                      ('data', c_void_p, 1),
                                      ('event', c_void_p, 1))


def fluid_synth_write_s16_stereo(synth, len):
    """Return generated samples in stereo 16-bit format

    Return value is a Numpy array of samples.

    """
    import numpy

    buf = create_string_buffer(len * 4)
    fluid_synth_write_s16(synth, len, buf, 0, 2, buf, 1, 2)
    return numpy.fromstring(buf[:], dtype=numpy.int16)


# Object-oriented interface, simplifies access to functions

class Synth:
    """Synth represents a FluidSynth synthesizer"""

    def __init__(self, gain=0.2, samplerate=44100, polyphony=128, channels=256):
        """Create new synthesizer object to control sound generation

        Optional keyword arguments:
          gain : scale factor for audio output, default is 0.2
                 lower values are quieter, allow more simultaneous notes
          samplerate : output samplerate in Hz, default is 44100 Hz
          polyphony: total polyphony of the output
          channels: number of MIDI channels.

        """
        st = new_fluid_settings()
        fluid_settings_setnum(st, b'gain', 1)#gain)
        fluid_settings_setnum(st, b'synth.sample-rate', samplerate)
        # We limit the polyphony to 128 for safety purposes
        fluid_settings_setint(st, b"synth.polyphony", polyphony)
        # No reason to limit ourselves to 16 channels
        fluid_settings_setint(st, b'synth.midi-channels', channels)
        self.settings = st
        self.synth = new_fluid_synth(self.settings)
        self.audio_driver = None
        self.midi_driver = None

    def start(self, audiodriver=b'alsa'):
        """Start audio output driver in separate background thread

        Call this function any time after creating the Synth object.
        If you don't call this function, use get_samples() to generate
        samples.

        Optional keyword argument:
          audiodriver : which audio driver to use for output
                   Possible choices:
                     'alsa', 'oss', 'jack', 'portaudio'
                     'sndmgr', 'coreaudio', 'Direct Sound',
                     'pulseaudio'

        Not all drivers will be available for every platform, it
        depends on which drivers were compiled into FluidSynth for
        your platform.

        """
        if audiodriver is not None:
            assert (audiodriver in [b'alsa', b'oss', b'jack', b'portaudio',
                                    b'sndmgr', b'coreaudio', b'Direct Sound', b'pulseaudio'])
            fluid_settings_setstr(self.settings, b'audio.driver', audiodriver)
        self.audio_driver = new_fluid_audio_driver(self.settings, self.synth)

    def delete(self):
        if self.audio_driver is not None:
            delete_fluid_audio_driver(self.audio_driver)
        if self.midi_driver is not None:
            delete_fluid_midi_driver(self.midi_driver)
        delete_fluid_synth(self.synth)
        delete_fluid_settings(self.settings)

    def sfload(self, filename, update_midi_preset=0):
        """Load SoundFont and return its ID"""
        return fluid_synth_sfload(self.synth, filename, update_midi_preset)

    def sfunload(self, sfid, update_midi_preset=0):
        """Unload a SoundFont and free memory it used"""
        return fluid_synth_sfunload(self.synth, sfid, update_midi_preset)

    def program_select(self, chan, sfid, bank, preset):
        """Select a program"""
        return fluid_synth_program_select(self.synth, chan, sfid, bank, preset)

    def noteon(self, chan, key, vel):
        """Play a note"""
        if key < 0 or key > 128:
            return False
        if chan < 0:
            return False
        if vel < 0 or vel > 128:
            return False
        return fluid_synth_noteon(self.synth, chan, key, vel)

    def noteoff(self, chan, key):
        """Stop a note"""
        if key < 0 or key > 128:
            return False
        if chan < 0:
            return False
        return fluid_synth_noteoff(self.synth, chan, key)

    def pitch_bend(self, chan, val):
        """Adjust pitch of a playing channel by small amounts

        A pitch bend value of 0 is no pitch change from default.
        A value of -2048 is 1 semitone down.
        A value of 2048 is 1 semitone up.
        Maximum values are -8192 to +8192 (transposing by 4 semitones).

        """
        return fluid_synth_pitch_bend(self.synth, chan, val + 8192)

    def cc(self, chan, ctrl, val):
        """Send control change value

        The controls that are recognized are dependent on the
        SoundFont.  Values are always 0 to 127.  Typical controls
        include:
          1 : vibrato
          7 : volume
          10 : pan (left to right)
          11 : expression (soft to loud)
          64 : sustain
          91 : reverb
          93 : chorus
        """
        return fluid_synth_cc(self.synth, chan, ctrl, val)

    def program_change(self, chan, prg):
        """Change the program"""
        return fluid_synth_program_change(self.synth, chan, prg)

    def bank_select(self, chan, bank):
        """Choose a bank"""
        return fluid_synth_bank_select(self.synth, chan, bank)

    def sfont_select(self, chan, sfid):
        """Choose a SoundFont"""
        return fluid_synth_sfont_select(self.synth, chan, sfid)

    def program_reset(self):
        """Reset the programs on all channels"""
        return fluid_synth_program_reset(self.synth)

    def system_reset(self):
        """Stop all notes and reset all programs"""
        return fluid_synth_system_reset(self.synth)

    def get_samples(self, len=1024):
        """Generate audio samples

        The return value will be a NumPy array containing the given
        length of audio samples.  If the synth is set to stereo output
        (the default) the array will be size 2 * len.

        """
        return fluid_synth_write_s16_stereo(self.synth, len)

    def get_polyphony(self):
        """ Gets the current polyphony
        :return: Current polyphony (int)
        """
        return fluid_synth_get_polyphony(self.synth)

    def set_polyphony(self, polyphony):
        """ Set synthesizer polyphony (max number of voices).
        :param polyphony: New polyphony to set
        :return: -1 if incorrect, 1 if correct
        """
        return fluid_synth_set_polyphony(self.synth, polyphony)

    def count_active_voices(self):
        """ Get current number of active voices.
        :return: Number of active voices
        """
        return fluid_synth_get_active_voice_count(self.synth)

    def get_gain(self):
        """ Gets synth output gain value
        :return: Curent gain (float)
        """
        return fluid_synth_get_gain(self.synth)

    def set_gain(self, gain):
        """ Set synth output gain value
        :param gain: Live sets the output gain
        :return: void
        """
        return fluid_synth_set_gain(self.synth, gain)

    def get_cpu_load(self):
        """ Get the synth CPU load value.
        :return: Float containing the CPU load.
        """
        return fluid_synth_get_cpu_load(self.synth)

    def get_channel_info(self, chan):
        """ Gets a struct with the information of the preset loaded in a channel.
        :param chan: Channel number of which we want to get the information
        :return: information structure with fields (synth, bank, preset, name)
        """
        information = ChannelInfo()
        fluid_synth_get_channel_info(self.synth, chan, information)
        return information

    def get_instrument_list(self, sfontid):
        """ Gets the instrument list and
        :param sfontid: Soundfont ID
        :return: A dictionary with keys BBB-PPP (bank-preset) and
        the name of the instrument preset. Example of how to access a preset's name:
            inst[str(bank).zfill(3) + '-' + str(program).zfill(3)]
        """
        fname = ".instSF" + str(sfontid)  # TEmporary file with the info of the SF2
        handler = new_fluid_cmd_handler(self.synth)

        instruments = dict()  # It builds the list as a dictionary
        # First, check if .instSF is created before and avoid repeating the process.
        try:
            for line in open(fname):
                instruments[line[0:7]] = line[8:-1]  # If possible, returns the instrument list
        except IOError:  # Creates the instrument list if it doesn't exist
            newshell = StdoutHandler(fname)
            newshell.freopen()
            fluid_command(handler, "inst " + str(sfontid), fluid_get_stdout())
            newshell.freclose()
            for line in open(fname):
                instruments[line[0:7]] = line[8:-1]

        return instruments

    def start_midi(self, mididriver=b'alsa_seq'):
        """
        Starts the MIDI driver to allow the MIDI keyboard interaction.
        :param mididriver: name of the midi driver, that can be one of these:
            'alsa_raw', 'alsa_seq', 'coremidi', 'jack',
            'midishare', 'oss', 'winmidi'
        :return:
        """
        if mididriver is not None:
            assert (mididriver in [b'alsa_raw', b'alsa_seq', b'coremidi', b'jack',
                                   b'midishare', b'oss', b'winmidi'])
            fluid_settings_setstr(self.settings, b'midi.driver', mididriver)
            # Optionally: sets the real time priority to 99.
            fluid_settings_setnum(self.settings, b'midi.realtimeprio', 99)
        self.midi_driver = new_fluid_midi_driver(self.settings, fluid_synth_handle_midi_event, self.synth)
        return self.midi_driver

    def stop_midi(self):
        """
        Stops the current midi Driver.
        :return: Nothing
        """
        if self.midi_driver is not None:  # Checks if there actually is a midi_driver
            delete_fluid_midi_driver(self.midi_driver)
            self.midi_driver = None


def raw_audio_string(data):
    """Return a string of bytes to send to soundcard

    Input is a numpy array of samples.  Default output format
    is 16-bit signed (other formats not currently supported).
    
    """
    import numpy

    return (data.astype(numpy.int16)).tostring()


class StdoutHandler(object):
    """Helper class for the capture of the Standard Output Stream.
    This is needed for some functions of class Synth.
    """

    def __init__(self, f):
        """Create new stdouthandler, for management of stdin and
        stdout (some methods of Synth DO need to capture stdout stream).
        """
        self.prevOutFd = os.dup(1)
        self.prevInFd = os.dup(0)
        self.prevErrFd = os.dup(2)
        self.newf = open(f, 'w')
        self.newfd = self.newf.fileno()  # The new file output

    def freopen(self):
        """
        Redirects the standard input, output and error stream
        to the established newfd.
        :return:
        """
        os.dup2(self.newfd, 0)
        os.dup2(self.newfd, 1)
        os.dup2(self.newfd, 2)

    def freclose(self):
        """
        Closes the modified input, output and error stream
        :return:
        """
        self.newf.close()
        os.dup2(self.prevOutFd, 1)
        os.close(self.prevOutFd)
        os.dup2(self.prevInFd, 0)
        os.close(self.prevInFd)
        os.dup2(self.prevErrFd, 2)
        os.close(self.prevErrFd)
