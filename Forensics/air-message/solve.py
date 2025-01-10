import numpy as np
from scipy.io import wavfile

sample_rate, data = wavfile.read('out.wav')

fs = 900e3 # sample rate
fc = 169e3 # Carrier Frequency 
N_fft = 83440
t = np.arange(N_fft)/fs #time scale

s = data
c = np.cos(2*np.pi*fc*t)

# Find Demodulated Signal
x = c*s # multiplication of carrier and received signals to perform demodulation

# Convolve with window function to remove noise
f_cutoff = 0.1 # Cutoff frequency as a fraction of the sampling rate
b = 0.08  # Transition band, as a fraction of the sampling rate (in (0, 0.5)).

N = int(np.ceil((4 / b)))
if not N % 2: N += 1  # N is odd.
n = np.arange(N)

h = np.sinc(2 * f_cutoff * (n - (N - 1) / 2)) # Compute sinc filter.
w = np.blackman(N) # Compute Blackman window.
h = h * w # Multiply sinc filter by window.
h = h / np.sum(h) # Normalize to get unity gain.

u = np.convolve(x, h)

scaled = np.uint8(u/np.max(np.abs(u)) * 255) # scale to 8 bit PCM audio 
wavfile.write('demoded.wav', 8000, scaled)
