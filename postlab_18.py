import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt
from scipy.io import wavfile

def load_audio(file_path):
    try:
        sample_rate, audio_data = wavfile.read(file_path)
        return sample_rate, audio_data
    except Exception as e:
        print(f"Error loading audio file {file_path}: {e}")
        return None, None

def convert_to_mono(audio_data):
    if len(audio_data.shape) == 2:
        return np.mean(audio_data, axis=1)
    return audio_data

def normalize_audio(audio_data):
    max_val = np.max(np.abs(audio_data))
    return audio_data / max_val if max_val > 0 else audio_data

def autocorrelation(audio):
    return signal.correlate(audio, audio, mode='full')

def cross_correlation(signal1, signal2):
    return signal.correlate(signal1, signal2, mode='full')

def plot_correlation(audio, auto_corr, cross_corr, file_name):
    plt.figure(figsize=(12, 8))
    
    plt.subplot(3, 1, 1)
    plt.title(f"Original {file_name} Audio Signal")
    plt.plot(audio, color='blue')
    plt.grid(True)
    
    plt.subplot(3, 1, 2)
    plt.title("Autocorrelation")
    plt.plot(auto_corr, color='orange')
    plt.grid(True)
    
    plt.subplot(3, 1, 3)
    plt.title("Cross-correlation with clean audio")
    plt.plot(cross_corr, color='green')
    plt.grid(True)
    
    plt.tight_layout()
    plt.show()

# Load audio files
sample_rate, clean_audio = load_audio("C:/Users/Acer/Downloads/Audio_2_Audio Denoise.wav")
_, noisy_audio = load_audio("C:/Users/Acer/Downloads/Audio_2.wav")
_, periodic_audio = load_audio("C:/Users/Acer/Downloads/senya.wav")

# Convert to mono and normalize
clean_audio = normalize_audio(convert_to_mono(clean_audio))
noisy_audio = normalize_audio(convert_to_mono(noisy_audio))
periodic_audio = normalize_audio(convert_to_mono(periodic_audio))

# Calculate correlations
auto_corr_clean = autocorrelation(clean_audio)
auto_corr_noisy = autocorrelation(noisy_audio)
auto_corr_periodic = autocorrelation(periodic_audio)

cross_corr_noisy = cross_correlation(clean_audio, noisy_audio)
cross_corr_periodic = cross_correlation(clean_audio, periodic_audio)

# Plot results
plot_correlation(clean_audio, auto_corr_clean, cross_corr_noisy, 'Clean')
plot_correlation(noisy_audio, auto_corr_noisy, cross_corr_noisy, 'Noisy')
plot_correlation(periodic_audio, auto_corr_periodic, cross_corr_periodic, 'Periodic')


