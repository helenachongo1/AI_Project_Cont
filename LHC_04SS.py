#TASK 4
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter

fs = 50000  # Sampling frequency in Hz
fc = 10000  # Carrier frequency in Hz
fm = 1000   # Modulating signal frequency in Hz
duration = 0.01  # Signal duration in seconds
t = np.linspace(0, duration, int(fs * duration), endpoint=False)  # Time vector
A_c = 1     # Carrier amplitude
A_m = 0.5   # Modulating signal amplitude
SNR = 20    # Signal-to-noise ratio in dB

# Generate modulating signal (1 kHz sine wave)
modulating_signal = A_m * np.sin(2 * np.pi * fm * t)

# Generate carrier signal (10 kHz sine wave)
carrier_signal = A_c * np.cos(2 * np.pi * fc * t)

# Perform amplitude modulation
modulated_signal = (1 + modulating_signal) * carrier_signal

# Add noise to the modulated signal
noise_power = np.mean(modulated_signal*2) / (10*(SNR / 10))
noise = np.sqrt(noise_power) * np.random.normal(size=modulated_signal.shape)
modulated_signal_noisy = modulated_signal + noise

# Coherent demodulation
demodulated_signal = modulated_signal_noisy * (2 * carrier_signal)  # Multiply by carrier

# Design low-pass filter
def butter_lowpass(cutoff, fs, order=6):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='low')
    return b, a

# Apply low-pass filter
cutoff = fm  # Low-pass filter cutoff frequency
b, a = butter_lowpass(cutoff, fs)
recovered_signal = lfilter(b, a, demodulated_signal)

# Plot results
plt.figure(figsize=(10, 8))

# Modulating signal
plt.subplot(4, 1, 1)
plt.plot(t, modulating_signal, label='Modulating Signal')
plt.title('Modulating Signal (1 kHz)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid()

# Modulated signal
plt.subplot(4, 1, 2)
plt.plot(t, modulated_signal, label='Modulated Signal')
plt.title('AM Modulated Signal (with Carrier)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid()

# Modulated signal with noise
plt.subplot(4, 1, 3)
plt.plot(t, modulated_signal_noisy, label='Noisy AM Signal')
plt.title('Noisy AM Signal')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid()

# Recovered signal
plt.subplot(4, 1, 4)
plt.plot(t, recovered_signal, label='Recovered Signal', color='g')
plt.title('Recovered Signal After Coherent Demodulation')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid()

plt.tight_layout()
plt.show()

