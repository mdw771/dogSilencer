# dogSilencer
DogSilencer a Python-based program used to train/repel barking dogs automatically. Once dog barking is detected, a short ultrasonic (10 kHz) audio clip is played to deter or annoy the dog. The program also provides a scheduled on/off feature which can hopefully help train the dog not to bark at improper time and places. 

## How to use
Use `pip install` or `conda install` to install dependencies. Run `listen.py` to start monitoring the acoustic environment. 

Barking detection is realized using various types of trigger functions contained in `trigger.py`. `spectral_peak_trigger` using `method='pbr'` suffices in most cases, where the ultrasonic countermeasure is trigger once a peak in the set spectral (frequency) range is detected. After running `listen.py`, a power spectrum plot of the input audio signal is shown. Observe the spectrum when the dog barks, and identify the position of the characteristic peak. The trigger works best when the detection range contains the peak fully but tightly. 

Please feel free to submit a PR if you manage to find or train a good DNN model that can be used as another trigger option.  
