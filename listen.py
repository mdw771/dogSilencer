import os
from time import time, sleep
import datetime

import pyaudio
import wave
import scipy.io.wavfile as swav
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d
import numpy as np

from utils import *
from notification import *
from trigger import *
from generator import *
from record import *


def listen_to_surroundings(interval=2, buffer_chunk=1024, rate=44100, trigger=None, trigger_pars={}, response=None, response_pars={}, schedule=None):

    # ds_interval = get_downsample_interval(rate, 100)
    format = pyaudio.paInt16
    channels = 2

    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=buffer_chunk)

    ind = 0
    while True:
        if schedule is not None:
            t_tuple = datetime.datetime.now().timetuple()
            current_hour = t_tuple[3] + t_tuple[4] / 60.
            if current_hour < schedule[0] and current_hour > schedule[1]:
                print('OFF')
                sleep(60)
                continue
        wav = record_audio(stream, rate=rate, buffer_chunk=buffer_chunk, interval=interval, ds_interval=None)
        if trigger(wav, **trigger_pars):
            print('Positivity!')
            if response is not None:
                response(**response_pars)
            sleep(1)
        ind += 1
        sleep(0.1)



if __name__ == '__main__':

    trigger = spectral_peak_trigger
    trigger_pars = {'range': (800, 2e3), 'interval': 1./44100, 'threshold_ratio': 1.1, 'method': 'pbr'}
    response = generate_wave_from_file
    response_pars = {'path': 'samples/antidog_ultrasound.wav'}

    listen_to_surroundings(trigger=trigger, trigger_pars=trigger_pars, response=response, response_pars=response_pars, schedule=None)