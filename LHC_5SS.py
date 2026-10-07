import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
from numpy.fft import fft, fftfreq

# Parameters
fs = 1000  # Sampling frequency (Hz)
duration = 1  # Duration of the signal (seconds)
t = np.linspace(0, duration, int(fs * duration), endpoint=False)  # Time vector

# Signal properties
carrier_freq = 100  # Carrier frequency (Hz)
modulating_freq = 10  # Modulating signal frequency (Hz)
modulation_index = 2  # Modulation index

# Generate the modulating signal (message signal)
modulating_signal = np.sin(2 * np.pi * modulating_freq * t)

# Frequency modulation (FM)
fm_signal = np.cos(2 * np.pi * carrier_freq * t + modulation_index * np.sin(2 * np.pi * modulating_freq * t))

# Frequency-domain analysis using FFT
nfft = len(fm_signal)
f = fftfreq(nfft, 1/fs)  # Frequency vector
fm_signal_fft = np.abs(fft(fm_signal, nfft))  # Magnitude of FFT

# Demodulation (FM to AM demodulation using frequency discriminator)
# First, differentiate the FM signal
diff_fm_signal = np.diff(fm_signal)
# Low-pass filter design to recover the modulating signal
b, a = butter(4, modulating_freq / (fs / 2), btype='low')
demodulated_signal = filtfilt(b, a, diff_fm_signal)  # Apply the filter

# Plot results
plt.figure(figsize=(10, 8))

# Time-domain: Modulating signal
plt.subplot(3, 1, 1)
plt.plot(t, modulating_signal, 'b')
plt.title('Modulating Signal (Message Signal)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)

# Time-domain: FM signal
plt.subplot(3, 1, 2)
plt.plot(t, fm_signal, 'r')
plt.title('FM Signal (Frequency Modulated Signal)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)

# Frequency-domain: FFT of FM signal
plt.subplot(3, 1, 3)
plt.plot(f[:nfft // 2], fm_signal_fft[:nfft // 2], 'k')
plt.title('Frequency Spectrum of FM Signal')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude')
plt.grid(True)

plt.tight_layout()
plt.show()

# Plot the demodulated signal (Recovered modulating signal)
plt.figure(figsize=(6, 4))
plt.plot(t[1:], demodulated_signal, 'g')
plt.title('Recovered Modulating Signal (Demodulated)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()

