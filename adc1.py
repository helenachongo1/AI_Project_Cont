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
    return 2 * bitstream - 1  # 0 -> -1, 1 -> 1

def bpsk_demodulate(received_signal):
    return (received_signal >= 0).astype(np.uint8)

def awgn(signal, snr_db):
    """Add AWGN noise to signal at specified SNR (in dB)."""
    snr_linear = 10 ** (snr_db / 10)
    power_signal = np.mean(signal ** 2)
    power_noise = power_signal / snr_linear
    noise = np.sqrt(power_noise) * np.random.randn(*signal.shape)
    return signal + noise

# Load audio file (mono, 16kHz recommended)
audio, fs = sf.read("C:/Users/Acer/Downloads/sample-3s.wav")
if audio.ndim > 1:
    audio = audio[:, 0]  # Take first channel if stereo

# Truncate to a few seconds if needed
audio = audio[:fs*3]

# Encode
pcm_bits, quantized = pcm_encode(audio, bits=8)
modulated = bpsk_modulate(pcm_bits)

# Add noise
noisy = awgn(modulated, snr_db=10)

# Demodulate and decode
demodulated = bpsk_demodulate(noisy)
reconstructed_audio = pcm_decode(demodulated[:len(pcm_bits)], bits=8)

# Save result
sf.write("reconstructed_audio.wav", reconstructed_audio, fs)

# Plot for fun
plt.figure()
plt.title("Original vs Reconstructed")
plt.plot(audio[:1000], label="Original")
plt.plot(reconstructed_audio[:1000], label="Reconstructed", alpha=0.7)
plt.legend()
plt.show()


