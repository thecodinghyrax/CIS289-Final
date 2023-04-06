# Use Scipy filter module. Use either Bessel or Butterworth filter. Cut off should be 300 to 4000hz
# Research - Generate a spectogram to find the part of the recording that has the lowest average frequency response. 
    # subtract that from all other points in the audio sample
# Clip the audio

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import soundfile as sf


rng = np.random.default_rng()
t = np.linspace(-1, 1, 201)
x = (np.sin(2*np.pi*0.75*t*(1-t) + 2.1) +
     0.1*np.sin(2*np.pi*1.25*t + 1) +
     0.18*np.cos(2*np.pi*3.85*t))
# x, _ = sf.read('test_audio.wav')
# print(x)
xn = x + rng.standard_normal(len(t)) * 0.08

# Create an order 3 lowpass butterworth filter
b, a = signal.butter(3, 0.05)

# Apply the flter to xn. User IFilter_zi to choose the initial cdition ofth eter:

zi = signal.lfilter_zi(b, a)
z, _ = signal.lfilter(b, a, xn, zi=zi*xn[0])

# Apply the filter again to have a rslt flteerd at an order t sam s filtfilt:

z2, _ = signal.lfilter(b, a, xn, zi=zi*xn[0])

# use filtfilt o apply the filter
y = signal.filtfilt(b, a, xn)

# plot the original signal and the various filtered versions:

plt.figure
plt.plot(t, xn, 'b', alpha=0.75)
plt.plot(t, z, 'r--', t, z2, 'r', t, y, 'k')
plt.legend(('noisy signal', 'lfilter, once', 'lfilter, twice', 'filtfilt'), loc='best')
plt.grid(True)
plt.show()