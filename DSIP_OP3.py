'''import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage import exposure, img_as_ubyte, img_as_float, color, measure
def process_image_q6(img_path, ref_path):
    # Read input and reference images
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    ref = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)

    # Histogram equalization methods
    heq = exposure.equalize_hist(img)
    clahe = exposure.equalize_adapthist(img, clip_limit=0.03)

    # Histogram matching 
    matched = exposure.match_histograms(img, ref, channel_axis=None)

    # Plot results
    plt.figure(figsize=(14, 10))

    plt.subplot(2, 2, 1)
    plt.title("Original")
    plt.imshow(img, cmap='gray')
    plt.axis("off")

    plt.subplot(2, 2, 2)
    plt.title("Histogram Equalization")
    plt.imshow(heq, cmap='gray')
    plt.axis("off")

    plt.subplot(2, 2, 3)
    plt.title("CLAHE")
    plt.imshow(clahe, cmap='gray')
    plt.axis("off")

    plt.subplot(2, 2, 4)
    plt.title("Histogram Matched")
    plt.imshow(matched, cmap='gray')
    plt.axis("off")

    plt.show()
process_image_q6("D:/ICT_2025/DSIP/images/ex1_2.png", "D:/ICT_2025/DSIP/images\ex1_5.png")'''

'''
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import color, filters, img_as_float
from skimage.restoration import denoise_bilateral
from scipy.signal import medfilt2d
image_paths = [
    "D:/ICT_2025/DSIP/images/img/smoothening data4.png" 
]

def load_gray(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = color.rgb2gray(img)
    return img_as_float(gray)

for path in image_paths:
    gray = load_gray(path)

    gauss_small = filters.gaussian(gray, sigma=0.5)
    gauss_large = filters.gaussian(gray, sigma=2.0)

    bilateral = denoise_bilateral(
        gray,
        sigma_color=0.05,
        sigma_spatial=10,
        channel_axis=None
    )

    median3 = medfilt2d((gray*255).astype(np.uint8), 3) / 255.0

    unsharp = filters.unsharp_mask(gray, radius=1, amount=1)

    lap = cv2.Laplacian((gray*255).astype(np.int16), cv2.CV_16S, ksize=3)
    lap_sharp = np.clip(gray + 0.002 * lap, 0, 1)

    lowp = filters.gaussian(gray, sigma=1)
    hb1 = np.clip(gray + 1.5 * (gray - lowp), 0, 1)
    hb2 = np.clip(gray + 3.0 * (gray - lowp), 0, 1)

    processed = [
        gauss_small, gauss_large, bilateral, median3,
        unsharp, lap_sharp, hb1, hb2
    ]

    titles = [
        "Gauss σ=0.5", "Gauss σ=2.0", "Bilateral", "Median 3×3",
        "Unsharp Mask", "Laplacian Sharpening",
        "HighBoost A=1.5", "HighBoost A=3.0"
    ]

    plt.figure(figsize=(20,10))

    # Original Image
    plt.subplot(3,3,1)
    plt.imshow(gray, cmap="gray")
    plt.title("Original")
    plt.axis("off")

    # Other filters
    for i, (img, title) in enumerate(zip(processed, titles)):
        plt.subplot(3,3, i + 2)
        plt.imshow(img, cmap="gray")
        plt.title(title)
        plt.axis("off")

    plt.tight_layout()
    plt.show()  
'''

'''
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import color, img_as_float
from scipy.ndimage import generic_filter
from scipy.signal import medfilt2d
from skimage.morphology import opening, closing, disk
image_paths = [
    "D:/ICT_2025/DSIP/images/ex1_4.png"  
]

def load_gray(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img_as_float(color.rgb2gray(img))

def alpha_trimmed(img, size=3, d=2):
    trim = d//2
    def f(window):
        w = np.sort(window)
        return w[trim:-trim].mean()
    return generic_filter(img, f, size=size)

def contraharmonic(img, size=3, Q=1.5):
    def f(window):
        num = np.sum(window**(Q+1))
        den = np.sum(window**Q) + 1e-12
        return num / den
    return generic_filter(img, f, size=size)

for path in image_paths:
    gray = load_gray(path)

    # Filters
    med3 = medfilt2d((gray * 255).astype(np.uint8), 3) / 255.0
    med5 = medfilt2d((gray * 255).astype(np.uint8), 5) / 255.0

    atm3 = alpha_trimmed(gray, 3, 2)
    atm5 = alpha_trimmed(gray, 5, 4)

    ch_pos = contraharmonic(gray, 3, Q=1.5)
    ch_neg = contraharmonic(gray, 3, Q=-1.5)

    opened = opening(gray, disk(1))
    closed = closing(gray, disk(1))

    # All results
    procs = [med3, med5, atm3, atm5, ch_pos, ch_neg, opened, closed]
    titles = ["Median 3×3", "Median 5×5", "ATM 3", "ATM 5",
              "CH (Q=1.5)", "CH (Q=-1.5)", "Opening", "Closing"]

    plt.figure(figsize=(20, 7))
    
    # Original
    plt.subplot(2, 5, 1)
    plt.imshow(gray, cmap="gray")
    plt.title("Original")
    plt.axis("off")

    for i, (img, title) in enumerate(zip(procs, titles)):
        plt.subplot(2, 5, i + 2)
        plt.imshow(img, cmap="gray")
        plt.title(title)
        plt.axis("off")

    plt.tight_layout()
    plt.show() '''


import cv2
import numpy as np
import matplotlib.pyplot as plt
def detect_bright_specks(img, threshold=20):
    """Detect small bright spots using Top-Hat transform."""
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    tophat = cv2.morphologyEx(img, cv2.MORPH_TOPHAT, se)
    count = np.sum(tophat > 30)
    return count > threshold

def detect_dark_cracks(img, threshold=20):
    """Detect thin dark cracks using Black-Hat transform."""
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    bothat = cv2.morphologyEx(img, cv2.MORPH_BLACKHAT, se)
    count = np.sum(bothat > 30)
    return count > threshold
def auto_morphology(img):
    # Ensure grayscale
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img.copy()

    # Detect noise types
    specks = detect_bright_specks(gray)
    cracks = detect_dark_cracks(gray)

    operations = []  # operations to return
    se = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    # Apply morphological operations based on detection
    if specks and cracks:
        gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, se)
        operations.append("Opening")

        gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, se)
        operations.append("Closing")

    elif specks:
        gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, se)
        operations.append("Opening")

    elif cracks:
        gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, se)
        operations.append("Closing")

    else:
        operations.append("None")

    return gray, operations
# Load image 
img = cv2.imread("C:/Users/Acer/Downloads/Datasets Practical Exam-1/Datasets Practical Exam/Image processing/The-noisy-satellite-image-impulse-noise-with-denoised-image.png")
# "D:/ICT_2025/DSIP/image_3.jpg"
result, ops = auto_morphology(img)

print("Operations performed:", ops)

# Plot the original and result images
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("Original Image")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(result, cmap="gray")
plt.title("Processed Image\n" + ", ".join(ops))
plt.axis("off")

plt.tight_layout()
plt.show()

'''
import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy import fftpack
from skimage import color, img_as_float
from skimage.feature import canny
from skimage.morphology import binary_closing, binary_opening, disk
def to_gray_float(img):
    if img.ndim == 3:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        gray = color.rgb2gray(img_rgb)
    else:
        gray = img / 255.0
    return img_as_float(gray)
def fft_lowpass(imgf, cutoff_ratio=0.06):
    rows, cols = imgf.shape
    F = fftpack.fftshift(fftpack.fft2(imgf))
    crow, ccol = rows // 2, cols // 2

    y, x = np.ogrid[:rows, :cols]
    r2 = (y - crow)**2 + (x - ccol)**2
    sigma = cutoff_ratio * np.sqrt(crow**2 + ccol**2)
    H = np.exp(-r2 / (2 * sigma**2))

    F_lp = F * H
    result = np.real(fftpack.ifft2(fftpack.ifftshift(F_lp)))

    return np.clip(result, 0, 1), H
def high_boost_freq(imgf, H_low, boost=1.3):
    F = fftpack.fftshift(fftpack.fft2(imgf))
    F_lp = F * H_low
    lowpassed = np.real(fftpack.ifft2(fftpack.ifftshift(F_lp)))
    lowpassed = np.clip(lowpassed, 0, 1)

    high = imgf - lowpassed
    restored = imgf + boost * high

    return np.clip(restored, 0, 1)
def extract_boundaries(imgf):
    edges = canny(imgf, sigma=1.0, low_threshold=0.08, high_threshold=0.18)
    se = disk(1)
    clean = binary_closing(edges, se)
    clean = binary_opening(clean, se)
    return clean
paths = [
    #"/content/ex1_1.png",
    #"/content/ex1_2.png",
    #"/content/ex1_3.png",
    #"/content/ex1_4.png",
    "D:/ICT_2025/DSIP/images/ex1_5.png",
]

for p in paths:
    img = cv2.imread(p)
    if img is None:
        print("Could not load:", p)
        continue

    gray = to_gray_float(img)
    smoothed, H = fft_lowpass(gray)
    restored = high_boost_freq(gray, H)
    edges = extract_boundaries(restored)
plt.figure(figsize=(12, 4))

plt.subplot(1, 4, 1)
plt.imshow(gray, cmap='gray')
plt.title("Gray")
plt.axis('off')

plt.subplot(1, 4, 2)
plt.imshow(smoothed, cmap='gray')
plt.title("Low-pass Filtered")
plt.axis('off')

plt.subplot(1, 4, 3)
plt.imshow(restored, cmap='gray')
plt.title("High-boost Sharpened")
plt.axis('off')

plt.subplot(1, 4, 4)
plt.imshow(edges, cmap='gray')
plt.title("Extracted Boundaries")
plt.axis('off')

plt.suptitle(f"Results for {p.split('/')[-1]}", fontsize=12)
plt.tight_layout()
plt.show()'''




