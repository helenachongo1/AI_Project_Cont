
'''import numpy as np
import librosa
import librosa.display
import soundfile as sf
import os
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve

# Impulse Response Synthesis

def synth_decay_ir(fs, length_s=1.0, decay=3.0):
    t = np.linspace(0, length_s, int(fs * length_s))
    ir = np.exp(-decay * t)
    ir += 0.02 * np.random.randn(len(t))  # early reflections
    return ir / np.linalg.norm(ir)


# Audio Utilities

def load_audio(path, sr=22050):
    y, sr = librosa.load(path, sr=sr, mono=True)
    return y, sr


def convolve_audio(sig, ir):
    return fftconvolve(sig, ir, mode='same')


def inverse_filter(obs, ir, eps=1e-4):
    """
    Frequency-domain inverse filtering
    with Tikhonov regularization
    """
    N = len(obs)
    n = 1 << (int(np.ceil(np.log2(N))) + 1)

    Obs = np.fft.rfft(obs, n)
    IR = np.fft.rfft(ir, n)

    inv = (np.conj(IR) / (IR * np.conj(IR) + eps)) * Obs
    x_est = np.fft.irfft(inv, n)[:N]

    return x_est


# Visualization

def plot_spectrogram(y, sr, title):
    S = np.abs(librosa.stft(y, n_fft=2048, hop_length=512))
    plt.figure(figsize=(7, 3))
    librosa.display.specshow(
        librosa.amplitude_to_db(S, ref=np.max),
        sr=sr,
        hop_length=512,
        y_axis='log',
        x_axis='time'
    )
    plt.title(title)
    plt.colorbar(format="%+2.0f dB")
    plt.tight_layout()


# File Paths (CHANGE THESE)

mixed_path = r"D:/ICT_2025/DSIP/Vande-Mataram-_Maa-Tujhe-Salaam_-_Mr-Jat.in_.wav"
karaoke_path = r"D:/ICT_2025/DSIP/Vande-Mataram-Karaoke-HQ.wav"  

if not os.path.exists(mixed_path):
    raise FileNotFoundError("Set mixed_path to a valid audio file")

# Main Processing

mixed, sr = load_audio(mixed_path, sr=22050)

IRs = [
    synth_decay_ir(sr, length_s=0.5, decay=6.0),
    synth_decay_ir(sr, length_s=1.2, decay=3.0),
    synth_decay_ir(sr, length_s=0.6, decay=10.0),
]

output_dir = "q1_outputs"
os.makedirs(output_dir, exist_ok=True)

for i, ir in enumerate(IRs):
    print(f"\nProcessing IR {i+1}")

    # 1) Convolution
    conv = convolve_audio(mixed, ir)
    sf.write(os.path.join(output_dir, f"mixed_convolved_ir{i+1}.wav"), conv, sr)

    # 2) Deconvolution
    deconv = inverse_filter(conv, ir, eps=1e-3)
    sf.write(os.path.join(output_dir, f"deconv_ir{i+1}.wav"), deconv, sr)

    # 3) Spectrograms
    plot_spectrogram(mixed, sr, "Original (Mixed)")
    plot_spectrogram(conv, sr, f"Convolved (IR {i+1})")
    plot_spectrogram(deconv, sr, f"Deconvolved (IR {i+1})")
    plt.show()


# Optional: Compare with Karaoke Track

if os.path.exists(karaoke_path):
    kara, _ = load_audio(karaoke_path, sr=sr)

    def corr(a, b):
        a = (a - a.mean()) / (a.std() + 1e-9)
        b = (b - b.mean()) / (b.std() + 1e-9)
        L = min(len(a), len(b))
        return np.mean(a[:L] * b[:L])

    for i in range(len(IRs)):
        deconv = sf.read(os.path.join(output_dir, f"deconv_ir{i+1}.wav"))[0]
        print(f"Correlation (karaoke vs deconv IR {i+1}) = {corr(kara, deconv):.4f}")
'''

'''
import numpy as np, librosa, soundfile as sf
from scipy import fftpack
from scipy.signal import butter, filtfilt, firwin, lfilter
import matplotlib.pyplot as plt
def plot_fft(y, sr, title="FFT"):
    N = len(y)
    Y = np.fft.rfft(y)
    freqs = np.fft.rfftfreq(N, 1/sr)
    plt.figure(figsize=(8,3))
    plt.semilogy(freqs, np.abs(Y))
    plt.xlim(0, sr/2)
    plt.title(title)
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("|Y(f)|")
def plot_waveform(y, sr, title="Waveform"):
    t = np.linspace(0, len(y)/sr, len(y))
    plt.figure(figsize=(8,3))
    plt.plot(t, y)
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
# load files
clean, sr = librosa.load("D:/ICT_2025/DSIP/Vande-Mataram-_Maa-Tujhe-Salaam_-_Mr-Jat.in_.wav", sr=None, mono=True)
noisy, _ = librosa.load("C:/Users/Acer/Downloads/onlinesound.net_white_gaussian_noise.wav", sr=sr, mono=True)

plot_fft(clean, sr, "Clean speech FFT")
plot_fft(noisy, sr, "Noisy speech FFT")
plt.show()

plot_waveform(clean, sr, "Clean Speech Waveform")
plot_waveform(noisy, sr, "Noisy Speech Waveform")
plt.show()

# IIR design 
b,a = butter(4, [300/(sr/2), 3400/(sr/2)], btype='band')
iir_out = filtfilt(b,a,noisy)
sf.write("q4_iir_filtered.wav", iir_out, sr)

plot_waveform(iir_out, sr, "IIR Filtered Speech Waveform")
plot_fft(iir_out, sr, "IIR Filtered Speech FFT")
plt.show()

# FIR design: firwin bandpass
numtaps = 513
fir = firwin(numtaps, [300, 3400], pass_zero=False, fs=sr)
fir_out = lfilter(fir, 1.0, noisy)
sf.write("q4_fir_filtered.wav", fir_out, sr)

plot_waveform(fir_out, sr, "FIR Filtered Speech Waveform")
plot_fft(fir_out, sr, "FIR Filtered Speech FFT")
plt.show()

# correlation with clean
def pearson(a,b):
    L = min(len(a), len(b))
    a=a[:L]; b=b[:L]
    a=(a-a.mean())/(a.std()+1e-9); b=(b-b.mean())/(b.std()+1e-9)
    return np.mean(a*b)

print("Corr (clean, noisy):", pearson(clean, noisy))
print("Corr (clean, iir_out):", pearson(clean, iir_out))
print("Corr (clean, fir_out):", pearson(clean, fir_out)) '''

from skimage import io, exposure, img_as_ubyte, color
import numpy as np
import os
import matplotlib.pyplot as plt
def process_image(path, outdir="q5_results"):
    os.makedirs(outdir, exist_ok=True)
    im = io.imread(path)

    # Convert to grayscale if RGB
    if im.ndim == 3:
        if im.shape[2] == 4:         
            im = im[:, :, :3]
        gray = color.rgb2gray(im)
    else:
        gray = im / 255.0

    
    heq = exposure.equalize_hist(gray)
    p2, p98 = np.percentile(gray, (2, 98))
    cons = exposure.rescale_intensity(gray, in_range=(p2, p98))
    log_img = exposure.adjust_log(gray, 1)
    gamma = exposure.adjust_gamma(gray, 0.7)
    clahe = exposure.equalize_adapthist(gray, clip_limit=0.03)

    
    base = os.path.basename(path).split('.')[0]
    io.imsave(os.path.join(outdir, base + "_heq.png"), img_as_ubyte(heq))
    io.imsave(os.path.join(outdir, base + "_stretch.png"), img_as_ubyte(cons))
    io.imsave(os.path.join(outdir, base + "_log.png"), img_as_ubyte(log_img))
    io.imsave(os.path.join(outdir, base + "_gamma.png"), img_as_ubyte(gamma))
    io.imsave(os.path.join(outdir, base + "_clahe.png"), img_as_ubyte(clahe))

    
    plt.figure(figsize=(14, 10))

    images = [gray, heq, cons, log_img, gamma, clahe]
    titles = [
        "Original (Gray)",
        "Histogram Equalization",
        "Contrast Stretching",
        "Log Transform",
        "Gamma Correction",
        "CLAHE"
    ]

    for i, (img, title) in enumerate(zip(images, titles), 1):
        plt.subplot(2, 3, i)
        plt.imshow(img, cmap='gray')
        plt.title(title)
        plt.axis("off")

    plt.suptitle(f"Enhancement Results for {base}", fontsize=16)
    plt.tight_layout()
    plt.show()

    return {
        "heq": heq,
        "stretch": cons,
        "log": log_img,
        "gamma": gamma,
        "clahe": clahe
    }
process_image("D:/ICT_2025/DSIP/images\ex1_5.png")





