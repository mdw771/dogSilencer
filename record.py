import numpy as np
import pyaudio


def record_audio(stream, rate=44100, buffer_chunk=1024, interval=2, ds_interval=None):

    wav = []
    for i in range(0, int(rate / buffer_chunk * interval)):
        data = stream.read(buffer_chunk, exception_on_overflow=False)
        wav.append(data)

    wav = np.fromstring(b''.join(wav), 'int16')[::2]

    if ds_interval is not None:
        wav = wav[::ds_interval]

    return wav