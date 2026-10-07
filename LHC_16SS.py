#task16 
import numpy as np
import matplotlib.pyplot as plt

# Parameters
fs = 1000  # Sampling frequency (Hz)
duration = 1  # Duration of the signals (seconds)
t = np.linspace(0, duration, int(fs * duration), endpoint=False)  # Time vector

# Generate two signals
signal1 = np.sin(2 * np.pi * 50 * t)  # A sine wave of 50 Hz
signal2 = np.sin(2 * np.pi * 50 * (t - 0.02))  # A sine wave of 50 Hz with a 20 ms delay

# Compute the auto-correlation of signal1
auto_corr_signal1 = np.correlate(signal1, signal1, mode='full')
lags = np.arange(-len(signal1) + 1, len(signal1)) / fs  # Lags for auto-correlation

# Compute the cross-correlation between signal1 and signal2
cross_corr = np.correlate(signal1, signal2, mode='full')
lags_cross = np.arange(-len(signal1) + 1, len(signal1)) / fs  # Lags for cross-correlation

# Find the delay between the signals
delay_index = np.argmax(cross_corr)  # Index of maximum correlation
delay = lags_cross[delay_index]  # Corresponding delay in seconds

# Plot the signals
plt.figure(figsize=(12, 8))

# Subplot 1: Signal 1 and Signal 2
plt.subplot(3, 1, 1)
plt.plot(t, signal1, label='Signal 1')
plt.plot(t, signal2, label='Signal 2', linestyle='--')
plt.title('Signal 1 and Signal 2')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)

# Subplot 2: Auto-correlation of Signal 1
plt.subplot(3, 1, 2)
plt.plot(lags, auto_corr_signal1)
plt.title('Auto-correlation of Signal 1')
plt.xlabel('Lag (s)')
plt.ylabel('Correlation')
plt.grid(True)

# Subplot 3: Cross-correlation between Signal 1 and Signal 2
plt.subplot(3, 1, 3)
plt.plot(lags_cross, cross_corr)
plt.title(f'Cross-correlation between Signal 1 and Signal 2 (Delay = {delay:.4f} s)')
plt.xlabel('Lag (s)')
plt.ylabel('Correlation')
plt.grid(True)

plt.tight_layout()
plt.show()

print(f"The delay between the signals is approximately {delay:.4f} seconds.")

