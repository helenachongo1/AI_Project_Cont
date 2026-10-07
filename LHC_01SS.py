#task1 
import numpy as np
import matplotlib.pyplot as plt

fs = 10000  # Sampling frequency in Hz

"""A longer duration increases the number of samples proportionally."""
duration = 1 # Duration in seconds
t = np.linspace(0, duration, int(fs * duration), endpoint=False)  # Time vector

f1 = 500  # Frequency of first sine wave in Hz
f2 = 1000  # Frequency of second sine wave in Hz
signal = np.sin(2 * np.pi * f1 * t) + np.sin(2 * np.pi * f2 * t)

# Add Gaussian noise with specified SNR
snr_db = 10 # Signal-to-noise ratio in dB
signal_power = np.mean(signal**2)
noise_power = signal_power / (10**(snr_db / 10))
noise = np.sqrt(noise_power) * np.random.randn(len(signal))
noisy_signal = signal + noise

# Frequency-domain representation
freqs = np.fft.rfftfreq(len(t), 1 / fs)
fft_signal = np.fft.rfft(noisy_signal)
magnitude = np.abs(fft_signal)

# Plot time-domain representation
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(t, noisy_signal, label="Noisy Signal", color="blue", alpha=0.7)
plt.plot(t, signal, label="Original Signal", color="orange", alpha=0.7)
plt.title("Time-Domain Representation")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()

# Plot frequency-domain representation
plt.subplot(2, 1, 2)
plt.stem(freqs, magnitude, basefmt=" ", label="FFT Magnitude")
plt.title("Frequency-Domain Representation")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.legend()

plt.tight_layout()
plt.show()

