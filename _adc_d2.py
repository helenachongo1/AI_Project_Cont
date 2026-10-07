import numpy as np
import soundfile as sf
from scipy import signal
import matplotlib.pyplot as plt

def pcm_encode(audio, bits=8):
    """Quantize and encode audio signal to PCM binary stream."""
    levels = 2 ** bits
    audio_normalized = (audio - np.min(audio)) / (np.max(audio) - np.min(audio))
    quantized = np.round(audio_normalized * (levels - 1)).astype(np.uint8)
    pcm = np.unpackbits(quantized)
    return pcm, quantized

def pcm_decode(pcm_bits, bits=8):
    """Decode PCM binary stream back to audio signal."""
    bytes_array = np.packbits(pcm_bits)
    audio_dequantized = bytes_array.astype(np.float32) / (2**bits - 1)
    audio_dequantized = 2 * audio_dequantized - 1  # back to [-1, 1]
    return audio_dequantized

def bpsk_modulate(bitstream):
    """Modulate bitstream using BPSK."""
    return 2 * bitstream - 1  # Here, 0 is represented by -1, and 1 by 1

def bpsk_demodulate(received_signal):
    """Demodulate BPSK signal back to bitstream."""
    return (received_signal >= 0).astype(np.uint8)

def awgn(signal, snr_db):
    """Add AWGN noise to signal at specified SNR (in dB)."""
    snr_linear = 10 ** (snr_db / 10)
    power_signal = np.mean(signal ** 2)
    power_noise = power_signal / snr_linear
    noise = np.sqrt(power_noise) * np.random.randn(*signal.shape)
    return signal + noise

# Load audio file
audio, fs = sf.read("C:/Users/Acer/Downloads/sample-3s.wav")
if audio.ndim > 1:
    audio = audio[:, 0]  # Take first channel if stereo

audio = audio[:fs*3]

# PCM Encode
pcm_bits, quantized = pcm_encode(audio, bits=8)

# BPSK Modulation
modulated = bpsk_modulate(pcm_bits)

noisy_signal = awgn(modulated, snr_db=10) # Adding AWGN 

# Demodulation
demodulated_bits = bpsk_demodulate(noisy_signal)

reconstructed_audio = pcm_decode(demodulated_bits[:len(pcm_bits)], bits=8)# PCM demodulation

sf.write("reconstructed_audio.wav", 0.9 * reconstructed_audio, fs) # Renconstructed audio

# Plot original and reconstructed audio
plt.figure(figsize=(10, 4))
plt.title("Original vs Reconstructed Audio")
plt.plot(audio[:1000], label="Original")
plt.plot(reconstructed_audio[:1000], label="Reconstructed", alpha=0.7)
plt.xlabel("Sample Index")
plt.ylabel("Amplitude")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()


