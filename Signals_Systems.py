import numpy as np
from PIL import Image
from scipy.ndimage import convolve

# Step 1: Read and convert the image
original_image = Image.open("C:/Users/Acer/OneDrive/Desktop/Voice Recorder/digital_images_week2_quizzes_lena.gif").convert('L')  # Convert to grayscale
original_image_array = np.array(original_image, dtype=np.float64)

# Step 2: Create the low-pass filter
low_pass_filter = np.ones((5, 5), dtype=np.float64) / 25.0

# Step 3: Filter the image
filtered_image_array = convolve(original_image_array, low_pass_filter, mode='nearest')

# Step 4: Compute MSE
mse_value = np.mean((original_image_array - filtered_image_array) ** 2)

# Step 5: Compute PSNR
MAX_I = 255.0
psnr_value = 10 * np.log10((MAX_I ** 2) / mse_value)

# Step 6: Display PSNR
print(f'PSNR Value: {psnr_value:.2f} dB')


