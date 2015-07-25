#! /usr/bin/python

import subprocess
import sys
import operator
import os

def usage():
    print "Usage: projam.py <input>"

def add_toks(histogram, toks):
    for tok in toks:
        if tok in histogram:
            histogram[tok] += 1
        else:
            histogram[tok] = 1

def read_file(f_in):
    histogram = {}
    with open(f_in) as f:
        for line in f:
            toks = line.split()
            add_toks(histogram, toks)
    f.close()
    return sorted(histogram.items(), key=operator.itemgetter(1), reverse=True)

def play_data(histogram):
    print histogram

def main():
    if len(sys.argv) == 2:
        histogram = read_file(sys.argv[1])
        play_data(histogram)

if __name__ == '__main__':
    main()
