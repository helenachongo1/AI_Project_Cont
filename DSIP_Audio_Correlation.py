import numpy as np
import librosa
from scipy.signal import correlate
import matplotlib.pyplot as plt

# Load the audio files
song1, sr1 = librosa.load("D:/ICT_2025/DSIP/Vande-Mataram-_Maa-Tujhe-Salaam_-_Mr-Jat.in_.wav", sr=None)  
#song2, sr2 = librosa.load("D:/ICT_2025/DSIP/Vande-Mataram-Karaoke-HQ.wav", sr=None)  
song3, sr3 = librosa.load("D:/ICT_2025/DSIP/Haan-Kar-De-_PenduJatt.Com.Se_.wav", sr=None)
#If sampling rates differ, resample song2 to match song1
if sr1 != sr3:
    print(f"Resampling song3 from {sr3} Hz to {sr1} Hz...")
    song3 = librosa.resample(song3, orig_sr=sr3, target_sr=sr1)
    sr3 = sr1

# Normalize (zero mean, unit variance)
song1 = (song1 - np.mean(song1)) / np.std(song1)
song3 = (song3 - np.mean(song3)) / np.std(song3)

# Perform cross-correlation
correlation = correlate(song1, song3, mode='full')
lags = np.arange(-len(song3)+1, len(song1))

# Find the best lag
best_lag = lags[np.argmax(correlation)]
time_lag = best_lag / sr1
max_corr = np.max(correlation) / len(song1)

print(f"Best lag = {best_lag} samples ({time_lag:.3f} sec)")
print(f"Max correlation = {max_corr:.3f}")

# Plot correlation
plt.figure(figsize=(10,5))
plt.plot(lags, correlation)
plt.title("Cross-correlation between two songs")
plt.xlabel("Lag (samples)")
plt.ylabel("Correlation")
plt.show()

