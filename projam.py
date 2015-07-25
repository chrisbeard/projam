#! /usr/bin/python

import hashlib
import math
import numpy
import subprocess
import sys
import time
import operator
import os
import wave

### Classes
class metadata:
    hits = 0
    freq = 0
    def __init__(self, _tok, _hits=1):
        self.hits = _hits
        h = hash_tok(_tok)
        self.freq = get_freq(h, h/10)

    def __repr__(self):
        return "{}".format(self.freq)

    def __strr__(self):
        return "{}".format(self.freq)

class SoundFile:
    def  __init__(self, signal, filename, duration=1, samplerate=44100):
        self.file = wave.open(filename, 'wb')
        self.signal = signal
        self.sr = samplerate
        self.duration = duration
  
    def write(self):
        self.file.setparams((1, 2, self.sr, self.sr*self.duration, 'NONE', 'noncompressed'))
        # setparams takes a tuple of: nchannels, sampwidth, framerate, nframes, comptype, compname
        self.file.writeframes(self.signal)
        self.file.close()


### Functions
def usage():
    print "Usage: projam.py <input>"

def get_signal_data(frequency=440, duration=1, volume=32768, samplerate=44100):
    samples = duration * samplerate
    period = samplerate / float(frequency)
    omega = numpy.pi * 2 / period
    t = numpy.arange(samples, dtype=numpy.float)
    y = volume * numpy.sin(t * omega)
    return y

def numpy_to_string(y):
    signal = "".join((wave.struct.pack('h', item) for item in y))
    return signal

def get_freq(freq, base=10):
    return int(base * round(float(freq) / base))

def hash_tok(tok):
    h = hashlib.sha1()
    h.update(tok)
    return int(h.hexdigest()[:4], 16) % 10000

def add_toks(tok_dict, wav_set, toks):
    for tok in toks:
        if tok in tok_dict:
            tok_dict[tok].hits += 1
        else:
            tok_dict[tok] = metadata(tok, 1)
            wav_set.add(tok_dict[tok].freq)

def read_file(f_in):
    tok_dict = {}
    wav_set = set()
    with open(f_in) as f:
        for line in f:
            toks = line.split()
            add_toks(tok_dict, wav_set, toks)
    f.close()
    return tok_dict, wav_set

def build_wavs(wav_set):
    for wav in wav_set:
        filename = "{}{}.wav".format(os.path.expanduser("~/Music"),'/wav/' + str(wav))
        if os.path.isfile(filename):
            continue
        duration = 5
        data = get_signal_data(wav, duration)
        signal = numpy_to_string(data)
        f = SoundFile(signal, filename, duration)
        f.write()
        print "Built: " + filename

def play_data(f_in, tok_dict, wav_set):
    with open(f_in) as f:
        base_path = os.path.expanduser("~/Music") + '/wav/'
        for line in f:
            toks = line.split()
            sounds = []
            for tok in toks:
                sys.stderr.write(tok + " ")
                freq = tok_dict[tok].freq
                wav_file = "{}{}.wav".format(base_path, str(freq))
                sounds.append(subprocess.Popen(['aplay', '-q', wav_file]))
                time.sleep(len(tok)/float(25))
            for s in sounds:
                s.kill()
            sys.stderr.write('\n')

def main():
    if len(sys.argv) == 2:
        f = sys.argv[1]
        tok_dict, wav_set = read_file(f)
        build_wavs(wav_set)
        play_data(f, tok_dict, wav_set)

### Main
if __name__ == '__main__':
    main()
