#import numpy as np

'''x=[1,2,3,4]
h=[1,0,-1]
linaer_conv=np.convolve(x, h)
print("Linear Convolution:",linaer_conv)'''


'''x = [1, 2, 3, 4]
h = [1, 0, -1]

# Determine the length for circular convolution
N = max(len(x), len(h))
# Zero-pad the shorter sequence to match the length of the longer one
x_padded = np.pad(x, (0, N - len(x)), mode='constant')
h_padded = np.pad(h, (0, N - len(h)), mode='constant')
# Perform circular convolution using FFT
X_fft = np.fft.fft(x_padded)
H_fft = np.fft.fft(h_padded)
circular_conv = np.fft.ifft(X_fft * H_fft)
# Only the real part is considered (since the imaginary part should be zero)
circular_conv = np.real(circular_conv)
print("Circular Convolution: ", circular_conv)'''

#import matplotlib.pyplot as plt

'''# Define two signals
x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 3, 4, 5, 6])

# Perform cross-correlation using numpy
cross_corr = np.correlate(x, y, mode='full')

#print(cross_corr)
# Plot cross-correlation
plt.stem(cross_corr)
plt.title('Cross-Correlation')
plt.show()'''

'''x = np.array([1, 2, 3, 4, 5])
# Perform autocorrelation using numpy
auto_corr = np.correlate(x, x, mode='full')
# Plot autocorrelation
plt.stem(auto_corr)
plt.title('Autocorrelation')
plt.show()'''

#Q2
import numpy as np 
import scipy.signal as signal
import matplotlib.pyplot as plt
from scipy.io import wavfile

def load_audio(file_path):
    sample_rate, audio_data = wavfile.read(file_path)
    return sample_rate, audio_data

def convert_to_mono(audio_data):
    if len(audio_data.shape)==2:
        return np.mean(audio_data, axis=1)
    return audio_data

def autocorrelation(audio):
    return signal(audio, audio, mode='full')

def cross_correlation(signal1, signal2):
    return signal(signal1, signal2, mode='full')

def plot_correlation(audio, auto_corr, cross_corr,file_name):
    plt.figure(figsize=(12, 8))
    
    plt.subplot(3, 1, 1)
    plt.title(f"Original {file_name} Audio Signal")
    plt.plot(audio)
    
    plt.subplot(3, 1, 2)
    plt.title("Autocorrelation")
    plt.plot(auto_corr)
    
    plt.subplot(3, 1, 3)
    plt.title("Cross-correlation with clean audio")
    plt.plot(cross_corr)
    
    plt.tight_layout()
    plt.show()
    
sample_rate, clean_audio = load_audio("C:/Users/Acer/Downloads/Audio_2_Audio Denoise.wav")
_, noisy_audio = load_audio("C:/Users/Acer/Downloads/Audio_2.wav")
_, periodic_audio = load_audio("C:/Users/Acer/Downloads/senya.wav")

clean_audio = convert_to_mono(clean_audio)
noisy_audio = convert_to_mono(noisy_audio)
periodic_audio = convert_to_mono(periodic_audio)

auto_corr_clean = autocorrelation(clean_audio)
auto_corr_noisy = autocorrelation(noisy_audio)
auto_corr_periodic = autocorrelation(periodic_audio)

cross_corr_noisy = cross_correlation(clean_audio, noisy_audio)
cross_corr_periodic = cross_correlation(clean_audio, periodic_audio)

plot_correlation(clean_audio, auto_corr_clean, auto_corr_clean, 'Clean')
plot_correlation(noisy_audio, auto_corr_noisy, cross_corr_noisy, 'Noisy')
plot_correlation(periodic_audio, auto_corr_periodic, cross_corr_periodic, 'Periodic')



#Q1
'''with wave.open("C:/Users/Acer/Downloads/Audio_2.wav",'rb') as wav_file:
    sample_width = wav_file.getsampwidth()
    n_frames = wav_file.getnframes()
    
    frames = wav_file.readframes(n_frames)
    x = np.frombuffer(frames, dtype=np.int16)

#Linear Convolution
h=[1,1,1,1]
linear_conv=np.convolve(x, h)
print("Linear convolution:",linear_conv)

#Circular Convolution
N = max(len(x),len(h))
x_padded=np.pad(x,(0,N-len(x)),mode='constant')
h_padded=np.pad(h,(0,N-len(h)),mode='constant')

X_fft=np.fft.fft(x_padded)
H_fft=np.fft.fft(h_padded)
circular_conv=np.fft.ifft(X_fft*H_fft)
circular_conv=np.real(circular_conv)
print("Circular Convolution:",circular_conv)'''


'''with wave.open("Audio_2.m4a",'rb') as wav_file:
    sample_width = wav_file.getsampwidth()
    n_frames = wav_file.getnframes()
    
    frames = wav_file.readframes(n_frames)
    input_audio = np.frombuffer(frames, dtype=np.int16)

auto_corr = np.correlate(input_audio, input_audio, mode='full')
plt.stem(auto_corr)
plt.title('Autocorrelation')
plt.show()'''


