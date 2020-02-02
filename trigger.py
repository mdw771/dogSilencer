import numpy as np
import matplotlib.pyplot as plt
import scipy as sp
import scipy.signal as sps
import scipy.ndimage as spi

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
    print(np.max(f[:plim]))
    plt.vlines(range[0], 0, np.max(f[:plim]))
    plt.vlines(range[1], 0, np.max(f[:plim]))
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


def spectral_peak_trigger(wav, range=(1000, 1e4), method='cwt', interval=1./44100, threshold_ratio=1.2, widths=None):

    f = abs(np.fft.fft(wav))
    freq = np.fft.fftfreq(f.size, interval)
    plim = f.size // 2
    f = f[:plim]
    freq = freq[:plim]
    f = spi.uniform_filter1d(f, 100)

    if method == 'cwt':
        if widths is None:
            widths = np.linspace(f.size / 50, f.size / 10, 10)
        peaks_inds = sps.find_peaks_cwt(f, widths)
    else:
        x_left, x_right = range
        mask = (abs(freq) >= range[0]) * (abs(freq) <= range[1])
        x_left_ind, x_right_ind = np.nonzero(mask)[0][0], np.nonzero(mask)[0][-1]
        f_left = np.mean(f[x_left_ind:x_left_ind + 5])
        f_right = np.mean(f[x_right_ind - 5:x_right_ind])
        peaks_inds = np.nonzero(freq >= int(np.mean(range)))[0][0]

    # Plotting spectrum
    plt.ion()
    plt.show()
    plt.xlabel('Frequency (Hz)')
    plt.clf()
    plt.plot(freq, f)
    plt.vlines(range[0], 0, np.max(f))
    plt.vlines(range[1], 0, np.max(f))
    plt.scatter(freq[peaks_inds], f[peaks_inds] + np.max(f) * 0.02)
    plt.xlim(0, None)
    plt.ylim(0, None)
    plt.draw()
    plt.pause(0.001)

    trigger = False
    if method == 'cwt':
        if np.count_nonzero((peaks_inds >= range[0]) * (peaks_inds <= range[1])) > 0:
            trigger = True
    else:
        base_int = (f_left + f_right) * (x_right_ind - x_left_ind + 1) / 2
        chunk_int = np.sum(f[mask])
        peak_ratio = chunk_int / base_int
        if peak_ratio >= threshold_ratio:
            trigger = True
        print('{}: Integration ratio = {}.'.format(datetime.datetime.now(), peak_ratio))

    if trigger:
        try:
            os.makedirs('log')
        except:
            pass
        f = open(os.path.join('log', str(datetime.date.today()) + '.txt'), 'a')
        f.write('{}: Integration ratio = {}.\n'.format(datetime.datetime.now(), peak_ratio))
        f.close()
    return trigger