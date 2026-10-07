import numpy as np
from PIL import Image
from scipy.ndimage import convolve

# Step 1: Load the image
original_image = Image.open("C:/Users/Acer/Downloads/digital_images_week3_quizzes_original_quiz.jpg").convert('L')  # Convert to grayscale
original_image = np.array(original_image, dtype=np.float64)  # Convert to double

# Step 2: Create a 3x3 low-pass filter
low_pass_filter = np.ones((3, 3)) / 9  # 3x3 filter with coefficients equal to 1/9

# Perform low-pass filtering
filtered_image = convolve(original_image, low_pass_filter, mode='nearest')

# Step 3: Down-sample the image by removing every other row and column
down_sampled_image = filtered_image[::2, ::2]  # Resulting image is 240x180

# Step 4: Create an all-zero array of original size
upsampled_image = np.zeros((359, 479), dtype=np.float64)  # Size of the original image

# Insert values from the down-sampled image
rows, cols = down_sampled_image.shape
for i in range(rows):
    for j in range(cols):
        upsampled_image[2*i, 2*j] = down_sampled_image[i, j]

# Step 5: Define the bilinear interpolation filter
bilinear_filter = np.array([[0.25, 0.5, 0.25],
                             [0.5, 1, 0.5],
                             [0.25, 0.5, 0.25]])

# Convolve with the bilinear filter to get the up-sampled image
final_image = convolve(upsampled_image, bilinear_filter, mode='nearest')

# Step 6: Compute PSNR
# Read the original image again to ensure it is in the same format
original_image_uint8 = Image.open("C:/Users/Acer/Downloads/digital_images_week3_quizzes_original_quiz.jpg").convert('L')
original_image_uint8 = np.array(original_image_uint8, dtype=np.float64)  # Convert to double

# Compute the PSNR
mse = np.mean((final_image - original_image_uint8) ** 2)  # Mean Squared Error
if mse == 0:
    psnr_value = float('inf')  # If MSE is 0, PSNR is infinite
else:
    psnr_value = 10 * np.log10(255 ** 2 / mse)  # Calculate PSNR

# Display the PSNR
print(f'PSNR: {psnr_value:.2f} dB')


