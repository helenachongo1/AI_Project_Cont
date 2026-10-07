import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, freqz

# Sampling frequency
fs = 10000  
# Cutoff frequency (slightly below Nyquist frequency)
fc = 4999   
# Filter order
order = 6    

# Normalize the cutoff frequency by the Nyquist frequency
wn = fc / (fs / 2)  # Normalized cutoff frequency

# Design low-pass Butterworth filter
b, a = butter(order, wn, 'low')

# Frequency response of the filter
f, H = freqz(b, a, worN=1024, fs=fs)

# Plot magnitude and phase response
plt.figure(figsize=(10, 6))

# Magnitude response
plt.subplot(2, 1, 1)
plt.plot(f, np.abs(H))
plt.title('Magnitude Response')
plt.xlabel('Frequency (Hz)')
plt.ylabel('|H(f)|')
plt.grid(True)

# Phase response
plt.subplot(2, 1, 2)
plt.plot(f, np.angle(H))
plt.title('Phase Response')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Phase (radians)')
plt.grid(True)

plt.tight_layout()
plt.show()
