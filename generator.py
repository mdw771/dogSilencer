import pyaudio
import numpy as np
import wave

import os


def generate_sinusoidal(hz=1e4, length=6, rate=44100):

    t = np.linspace(0, length, rate * length)
    wav = np.sin(2 * np.pi * hz * t)
    return wav


def generate_wave_from_file(path, chunk=1024):

    wf = wave.open(path)
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(chunk)

    while len(data) > 0:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()

    p.terminate()

    return


if __name__ == '__main__':

    generate_wave_from_file(os.path.join('samples', 'antidog_ultrasound.wav'))