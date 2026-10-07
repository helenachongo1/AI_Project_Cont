'''
import numpy as np
import matplotlib.pyplot as plt

def simulate_discrete_sine_wave(num_samples, sampling_frequency, amplitude, frequency, phase):
    time = np.arange(num_samples) / sampling_frequency
    sine_wave = amplitude * np.sin(2 * np.pi * frequency * time + phase)
    return sine_wave


# Define the number of samples, sampling frequency, and parameters for the discrete sine wave signal
num_samples = 30  
sampling_frequency = 10  
amplitude = 1  
frequency = 2  
phase = 0  

discrete_sine_wave = simulate_discrete_sine_wave(num_samples, sampling_frequency, amplitude, frequency, phase)

plt.stem(discrete_sine_wave)
plt.title('Discrete Sine Wave Signal')
plt.xlabel('Sample')
plt.ylabel('Amplitude')

plt.tight_layout()
plt.show()

def linear_convolution(signal1, signal2):
    # Compute the linear convolution
    linear_conv = np.convolve(signal1, signal2, mode='full')
    return linear_conv

# Define the discrete-time signals
signal1 = np.array(discrete_sine_wave)
signal2 = np.array([1, 0, 1, 0, 1])

# Compute the linear convolution
linear_conv = linear_convolution(signal1, signal2)

plt.stem(linear_conv)
plt.title('Linear Convolution')
plt.xlabel('Sample')
plt.ylabel('Amplitude')
'''

import numpy as np
import matplotlib.pyplot as plt

def simulate_function(time):
    y = np.zeros_like(time)
    y[time == 0] = 0
    y[time == -1] += -1
    y[time == -2] += -2
    y[time == -3] += -3
    y[time == -4] += -4
    y[time == -5] += 5
    y[time == -6] += 4
    y[time == -7] += 3
    y[time == -8] += 2
    y[time == -9] += 1
    y[time == -10] += 0
    y[time == -11] += -1
    y[time == -12] += -2
    y[time == -13] += -3
    y[time == -14] += -4
    y[time == -15] += -5
    
    y[time == 1] = 1
    y[time == 2] += 2
    y[time == 3] += 3
    y[time == 4] += 4
    y[time == 5] += 5
    y[time == 6] = -5
    y[time == 7] += -4
    y[time == 8] += -3
    y[time == 9] += -2
    y[time == 10] += -1
    
    y[time == 11] = 0
    y[time == 12] += 1
    y[time == 13] += 2
    y[time == 14] += 3
    y[time == 15] += 4
    
    return y

# Define the time range
time = np.arange(-15, 15)

# Simulate the function
function_values = simulate_function(time)

# Plot and display the function
plt.stem(time, function_values)
plt.title('Function y(t) = Delta(t) + delta(t-1) + 3*delta(t+5)')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.ylim([-0.5, 4.5])
plt.grid(True)
plt.show()

plt.tight_layout()
plt.show()

def linear_convolution(signal1, signal2):
    # Compute the linear convolution
    linear_conv = np.convolve(signal1, signal2, mode='full')
    return linear_conv

# Define the discrete-time signals
signal1 = np.array([-5,-4,-3,-2,-1,0,1,2,3,4,5])
signal2 = np.array([1, 0, 1, 0, 1])

# Compute the linear convolution
linear_conv = linear_convolution(signal1, signal2)

plt.stem(linear_conv)
plt.title('Linear Convolution')
plt.xlabel('Sample')
plt.ylabel('Amplitude')


