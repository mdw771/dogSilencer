import numpy as np
import matplotlib.pyplot as plt

from time import time
import datetime

import os

def integrated_volume_trigger(wav, threshold=200000):

    chunk_int = np.sum(abs(wav))
    print('{}: Integrated volume = {}.'.format(datetime.datetime.now(), chunk_int))

    if chunk_int >= threshold:
        try:
            os.makedirs('log')
        except:
            pass
        f = open(os.path.join('log', str(datetime.date.today()) + '.txt'), 'a')
        f.write('{}: Integrated volume = {}.\n'.format(datetime.datetime.now(), chunk_int))
        f.close()
    return chunk_int >= threshold


def frequeny_trigger(wav, range=(1000, 1e4), interval=1./44100, threshold=200000):

    f = abs(np.fft.fft(wav))
    freq = np.fft.fftfreq(f.size, interval)

    # Plotting spectrum
    plim = f.size // 2
    plt.ion()
    plt.show()
    plt.xlabel('Frequency (Hz)')
    plt.clf()
    plt.plot(freq[:plim], f[:plim])
    plt.draw()
    plt.pause(0.001)

    chunk_int = np.sum(f[(abs(freq) >= range[0]) * (abs(freq) <= range[1])])
    print('{}: Band energy = {:e}.'.format(datetime.datetime.now(), chunk_int))

    if chunk_int >= threshold:
        try:
            os.makedirs('log')
        except:
            pass
        f = open(os.path.join('log', str(datetime.date.today()) + '.txt'), 'a')
        f.write('{}: Band energy = {:e}.\n'.format(datetime.datetime.now(), chunk_int))
        f.close()
    return chunk_int >= threshold