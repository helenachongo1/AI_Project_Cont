
import numpy as np
import matplotlib.pyplot as plt

#Q1
'''fs=1000
f=5
t = np.linspace(0, 1, fs, endpoint=True)
sine_wave = np.sin(2 * np.pi * f * t)
cosine_wave = np.cos(2 * np.pi * f* t)
#plt.figure(figsize=(10, 5))
plt.subplot(2, 1, 1)
plt.plot(t, sine_wave)
plt.title('Sine Wave')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.subplot(2, 1, 2)
plt.plot(t, cosine_wave)
plt.title('Cosine wave')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.tight_layout()
plt.show()'''

#Q2
'''f=2
T=0.1
n = np.arange(0, 20) 
t_continuous = np.linspace(0, 1, 1000)  
signal = np.sin(2 * np.pi * f * T * n)
continuous_signal = np.sin(2 * np.pi * f * t_continuous)
plt.subplot(2, 1, 1)
plt.stem(n, signal)
plt.title('Discrete Signal')
plt.xlabel('n (Discrete Time)')
plt.ylabel('Amplitude')
plt.subplot(2, 1, 2)
plt.plot(t_continuous, continuous_signal)
plt.title('Continuous-Time Signal (Sine Wave)')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.show()'''

#Q3
#a,b,c

'''t = np.arange(0, 10)
x=((np.e)**(-t)) * np.sin(2* np.pi * t)
x_rev = (((np.e)**t) * np.sin(2* np.pi * (-t)))
x_1 = (2 * x) + x_rev
plt.plot(t, x_1)
plt.title('x(t) = 2x(t)+x(-t)')
plt.xlabel('t')
plt.ylabel('x(t)')
plt.show()'''

#no. 4
'''import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve

def perform_convolution(signal1, signal2):
    convolved_signal = convolve(signal1, signal2, mode='full')
    return convolved_signal

def plot_signals(signal1, signal2, convolved_signal):
    plt.figure(figsize=(14, 8))

    plt.subplot(3, 1, 1)
    plt.plot(signal1, label='Signal 1')
    plt.title('Original Signal 1')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 2)
    plt.plot(signal2, label='Signal 2')
    plt.title('Original Signal 2')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(convolved_signal, label='Convolved Signal')
    plt.title('Convolved Signal')
    plt.xlabel('Sample')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()

t = np.linspace(0, 1, 500, endpoint=False)
signal1 = np.sin(2 * np.pi * 5 * t) 
signal2 = np.sin(2 * np.pi * 10 * t)  

convolved_signal = perform_convolution(signal1, signal2)
plot_signals(signal1, signal2, convolved_signal)'''

#no. 5
import numpy as np
import matplotlib.pyplot as plt

fc = 100  
fm = 5   
t = np.linspace(0, 1, 1000)  

c_t = np.sin(2 * np.pi * fc * t)
m_t = 0.5 * np.sin(2 * np.pi * fm * t)
s_t = (1 + m_t) * c_t

plt.figure(figsize=(12, 8))

plt.subplot(3, 1, 1)
plt.plot(t, c_t, label='$c(t) = \sin(2\pi f_c t)$', color='b')
plt.title('Carrier Signal $c(t)$')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 2)
plt.plot(t, m_t, label='$m(t) = 0.5 \sin(2\pi f_m t)$', color='r')
plt.title('Message Signal $m(t)$')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)

plt.subplot(3, 1, 3)
plt.plot(t, s_t, label='$s(t) = (1 + m(t)) \cdot c(t)$', color='g')
plt.title('Modulated Signal $s(t)$')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()