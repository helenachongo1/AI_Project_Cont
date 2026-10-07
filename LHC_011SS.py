import numpy as np
import matplotlib.pyplot as plt

# Time from 0 to 1 second
t = np.linspace(0, 1, 1000)

# Fundamental frequency
f0 = 1  
omega0 = 2 * np.pi * f0  # Fundamental angular frequency

# Original square wave
original_square_wave = np.sign(np.sin(2 * np.pi * f0 * t))

# Fourier Series approximation up to the 10th harmonic
N = 10
reconstructed_wave = np.zeros_like(t)  # Initialize with zeros, same shape as t

for k in range(1, N + 1):
    if k % 2 == 1:  # Only odd harmonics (1, 3, 5, ...)
        reconstructed_wave += (4 / (np.pi * k)) * np.sin(k * omega0 * t)

# Plotting the results
plt.figure(figsize=(10, 6))

# Plot original square wave
plt.subplot(2, 1, 1)
plt.plot(t, original_square_wave, 'r', linewidth=1.5)
plt.title('Original Square Wave')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)

# Plot Fourier series approximation
plt.subplot(2, 1, 2)
plt.plot(t, reconstructed_wave, 'b', linewidth=1.5)
plt.title('Fourier Series Approximation (up to 10th Harmonic)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)

# Show the plots
plt.tight_layout()
plt.show()


