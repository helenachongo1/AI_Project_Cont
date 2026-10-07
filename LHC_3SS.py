import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt

f_low = 500    # Low cutoff frequency (500 Hz)
f_high = 2000  # High cutoff frequency (2 kHz)
fs = 10000     # Sampling frequency (10 kHz for better resolution)

f_low_norm = f_low / (0.5 * fs)  # Normalize by Nyquist frequency
f_high_norm = f_high / (0.5 * fs)

'''Design the band-pass filter using Butterworth filter'''
order, wn = signal.buttord([f_low_norm, f_high_norm], [f_low_norm * 0.8, f_high_norm * 1.2], 3, 40)
b, a = signal.butter(order, wn, btype='bandpass')

'''Generate a test signal with frequencies from 100 Hz to 5 kHz'''
t = np.linspace(0, 1, fs) 
signal_test = np.sum([np.sin(2 * np.pi * f * t) for f in [100, 500, 1000, 1500, 2000, 3000, 4000, 5000]], axis=0)

'''Apply the filter to the test signal'''
filtered_signal = signal.filtfilt(b, a, signal_test)

'''Frequency response of the filter'''
w, h = signal.freqz(b, a, worN=2000)
freq = w * fs / (2 * np.pi)

plt.figure(figsize=(12, 8))

'''Magnitude Response'''
plt.subplot(2, 1, 1)
plt.plot(freq, 20 * np.log10(abs(h)), 'b')
plt.title('Band-pass Filter Magnitude Response')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Magnitude [dB]')
plt.grid(True)
plt.xlim([0, 5000])

'''Phase Response'''
plt.subplot(2, 1, 2)
plt.plot(freq, np.angle(h), 'b')
plt.title('Band-pass Filter Phase Response')
plt.xlabel('Frequency [Hz]')
plt.ylabel('Phase [radians]')
plt.grid(True)
plt.xlim([0, 5000])

plt.tight_layout()
plt.show()

'''Filter Design:
We define the passband (500 Hz to 2 kHz) and the sampling frequency (10 kHz).
Using scipy.signal.butter(), a Butterworth band-pass filter is designed based on the normalized cutoff frequencies.
Test Signal:
A synthetic signal is generated with frequencies from 100 Hz to 5 kHz using a sum of sinusoidal components.
Filter Application:
The scipy.signal.filtfilt() function applies the filter to the generated signal, ensuring zero-phase distortion.
Frequency Response:
The frequency response (magnitude and phase) of the filter is obtained using scipy.signal.freqz(),
 and then plotted using Matplotlib.'''
