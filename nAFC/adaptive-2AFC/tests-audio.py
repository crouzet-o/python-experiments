#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 14:33:36 2020

Tests for audio : portaudio and sounddevice

@author: crouzet-o
"""

"""
 PyAudio seems to dysfunction with Anaconda (but not tested with Debian Python)

"""

import pyaudio
#p = pyaudio.PyAudio()

import sounddevice as sd
import numpy as np

noise = np.random.normal(0, 1, 44100)
fs = 44100

sd.play(noise, fs)
sd.get_portaudio_version()

# Seem to work with alsa only
#import simpleaudio as sa
#play_obj = sa.play_buffer(noise, 1, 2, 44100)
#play_obj.wait_done()