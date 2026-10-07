import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from scipy.signal import butter, cheby1, bilinear, lfilter, spectrogram

# Design Filters
def design_butterworth_filter(filter_order, cutoff_frequency, sampling_frequency):
    analog_b, analog_a = butter(filter_order, cutoff_frequency, analog=True, btype='low')
    digital_b, digital_a = bilinear(analog_b, analog_a, sampling_frequency)
    return digital_b, digital_a

def design_chebyshev_filter(filter_order, cutoff_frequency, sampling_frequency, ripple):
    analog_b, analog_a = cheby1(filter_order, ripple, cutoff_frequency, analog=True, btype='low')
    digital_b, digital_a = bilinear(analog_b, analog_a, sampling_frequency)
    return digital_b, digital_a

# Filter specifications 
filter_order = 4
cutoff_frequency = 1000
sampling_frequency = 8000
ripple = 0.5

# Design the filters
butter_b, butter_a = design_butterworth_filter(filter_order, cutoff_frequency, sampling_frequency)
cheby_b, cheby_a = design_chebyshev_filter(filter_order, cutoff_frequency, sampling_frequency, ripple)

# Load the song 
audio = AudioSegment.from_mp3("D:/ICT_2025/DSIP/Vande Mataram Karaoke -HQ.mp3")
audio = audio.set_channels(1).set_frame_rate(sampling_frequency)  # match filter sampling rate
samples = np.array(audio.get_array_of_samples()).astype(np.float32)

# Apply filters
butter_filtered = lfilter(butter_b, butter_a, samples)
cheby_filtered = lfilter(cheby_b, cheby_a, samples)

# Plot time-domain waveforms
plt.figure(figsize=(14, 8))

plt.subplot(3, 1, 1)
plt.plot(samples[:2000])
plt.title("Original Input (Time Domain)")
plt.xlabel("Samples")
plt.ylabel("Amplitude")

plt.subplot(3, 1, 2)
plt.plot(butter_filtered[:2000])
plt.title("Butterworth Filter Output (Time Domain)")
plt.xlabel("Samples")
plt.ylabel("Amplitude")

plt.subplot(3, 1, 3)
plt.plot(cheby_filtered[:2000])
plt.title("Chebyshev Filter Output (Time Domain)")
plt.xlabel("Samples")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()

# Plot spectrograms
plt.figure(figsize=(14, 8))

f, t, Sxx = spectrogram(samples, fs=sampling_frequency)
plt.subplot(3, 1, 1)
plt.pcolormesh(t, f, 10*np.log10(Sxx))
plt.title("Original Input (Spectrogram)")
plt.ylabel("Frequency [Hz]")

f, t, Sxx = spectrogram(butter_filtered, fs=sampling_frequency)
plt.subplot(3, 1, 2)
plt.pcolormesh(t, f, 10*np.log10(Sxx))
plt.title("Butterworth Filter Output (Spectrogram)")
plt.ylabel("Frequency [Hz]")

f, t, Sxx = spectrogram(cheby_filtered, fs=sampling_frequency)
plt.subplot(3, 1, 3)
plt.pcolormesh(t, f, 10*np.log10(Sxx))
plt.title("Chebyshev Filter Output (Spectrogram)")
plt.ylabel("Frequency [Hz]")
plt.xlabel("Time [sec]")

plt.tight_layout()
plt.show()
