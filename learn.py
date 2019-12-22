import os

import pyaudio
import wave
import scipy.io.wavfile as swav
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d
import numpy as np
from tqdm import trange

from utils import *


def record_sample(time_length=30, buffer_chunk=1024, rate=44100, filename='raw_rec.wav'):

    format = pyaudio.paInt16
    channels = 2

    p = pyaudio.PyAudio()

    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=buffer_chunk)

    print("* recording")

    frames = []

    for i in range(0, int(rate / buffer_chunk * time_length)):
        data = stream.read(buffer_chunk)
        frames.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
    return


def split_sample(filename='raw_rec.wav', positive_time_range=None, negative_time_range=None, chunk_time_length=2, output_folder='samples', plot=True):

    assert positive_time_range is not None, 'You must provide positive_time_range as a tuple.'
    assert negative_time_range is not None, 'You must provide negative_time_range as a tuple.'

    rate, wav = swav.read(filename)
    wav = np.mean(wav, axis=1)
    chunk_sample_length = rate * chunk_time_length
    plot_downsample = get_downsample_interval(rate, 100)

    t_st, t_end = positive_time_range

    print('Processing positive segments...')
    for i, ind in enumerate(trange(t_st * rate, t_end * rate, chunk_sample_length)):
        this_wav_chunk = wav[ind:min([ind + chunk_sample_length, len(wav)])]
        swav.write(os.path.join(output_folder, 'pos_{:03d}.wav'.format(i)), rate, this_wav_chunk)
        if plot:
            # this_wav_chunk = gaussian_filter1d(this_wav_chunk, plot_downsample / 10)
            plt.figure()
            plt.plot(this_wav_chunk[::plot_downsample])
            plt.savefig(os.path.join(output_folder, 'plot_pos_{:03d}.png'.format(i)))

    t_st, t_end = negative_time_range

    print('Processing negative segments...')
    for i, ind in enumerate(trange(t_st * rate, t_end * rate, chunk_sample_length)):
        this_wav_chunk = wav[ind:min([ind + chunk_sample_length, len(wav)])]
        swav.write(os.path.join(output_folder, 'neg_{:03d}.wav'.format(i)), rate, this_wav_chunk)
        if plot:
            # this_wav_chunk = gaussian_filter1d(this_wav_chunk, plot_downsample / 10)
            plt.figure()
            plt.plot(this_wav_chunk[::plot_downsample])
            plt.savefig(os.path.join(output_folder, 'plot_neg_{:03d}.png'.format(i)))

    return


if __name__ == '__main__':

    split_sample('samples/raw_rec.wav', (24, 26), (0, 10))