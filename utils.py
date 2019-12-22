import numpy as np
import scipy.io.wavfile as swav
import matplotlib.pyplot as plt
from scipy.ndimage.filters import gaussian_filter1d
import pyaudio as pa
from pyfftw.interfaces.numpy_fft import fft, ifft


def get_downsample_interval(rate, pps=100):

    return int(rate / pps)


def phase_correlation(signal, ref):

    fft_s = fft(signal)
    fft_r = fft(ref)
    prod_of_ffts = (fft_s * np.conjugate(fft_r))
    pc = prod_of_ffts / np.abs(prod_of_ffts)
    return abs(ifft(pc))
