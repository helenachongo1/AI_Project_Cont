import numpy as np
import matplotlib.pyplot as plt

num_bits = int(1e5)         # Number of bits to simulate
SNR_dB = np.arange(0, 21, 2)  # Range of SNR in dB
SNR_linear = 10 ** (SNR_dB / 10)  # Convert SNR to linear scale

# Generate random binary data
data = np.random.randint(0, 2, num_bits)  # Binary data (0s and 1s)

# BPSK Modulation (mapping 0 -> +1, 1 -> -1)
bpsk_signal = 2 * data - 1  # Map binary data to BPSK symbols

# Pre-allocate BER results
BER = np.zeros(len(SNR_dB))

# Loop through different SNR values
for i in range(len(SNR_dB)):
    # Add AWGN noise to the signal
    noise = (1 / np.sqrt(2 * SNR_linear[i])) * (np.random.randn(num_bits) + 1j * np.random.randn(num_bits))  # Complex Gaussian noise
    received_signal = bpsk_signal + np.real(noise)  # Add real noise part
    
    # BPSK Demodulation (decoding the received signal)
    demodulated_data = received_signal > 0  # Decision rule: +1 -> 0, -1 -> 1
    
    # Compute bit errors
    errors = np.sum(demodulated_data != data)
    
    # Compute Bit Error Rate (BER)
    BER[i] = errors / num_bits

# Plot the Bit Error Rate (BER) vs. SNR
plt.figure(figsize=(10, 6))
plt.semilogy(SNR_dB, BER, 'b-o', linewidth=2)
plt.grid(True)
plt.title('BPSK: Bit Error Rate (BER) vs. SNR')
plt.xlabel('SNR (dB)')
plt.ylabel('Bit Error Rate (BER)')
plt.axis([0, 20, 1e-5, 1])
plt.tight_layout()
plt.show()


