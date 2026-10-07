'''
import numpy as np
import matplotlib.pyplot as plt

def design_fir_filter(cutoff_freq, filter_length, window_type):
    # Design the ideal frequency response (low-pass filter)
    ideal_freq_response = np.ones(filter_length)
    ideal_freq_response[(cutoff_freq + 1):] = 0

    # Apply the selected window function
    window = np.hamming(filter_length)  # Change the window type as per your requirement
    filter_coefficients = ideal_freq_response * window

    # Normalize the filter coefficients
    filter_coefficients /= np.sum(filter_coefficients)

    return filter_coefficients

def plot_filter_response(filter_coefficients):
    # Compute the frequency response of the filter
    frequency_response = np.fft.fft(filter_coefficients)

    # Compute the magnitude response in dB
    magnitude_response = 20 * np.log10(np.abs(frequency_response))

    # Plot the magnitude response
    plt.figure(figsize=(10, 6))
    plt.plot(magnitude_response)
    plt.title('FIR Filter Magnitude Response')
    plt.xlabel('Frequency')
    plt.ylabel('Magnitude (dB)')
    plt.grid(True)
    plt.show()

    # Compute the impulse response of the filter
    impulse_response = np.fft.ifft(frequency_response)

    # Plot the impulse response
    plt.figure(figsize=(10, 6))
    plt.plot(impulse_response.real)
    plt.title('FIR Filter Impulse Response')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.show()

# Specify the desired filter specifications
cutoff_frequency = 0.2  # Normalized cutoff frequency (0.0 to 0.5)
filter_length = 51  # Number of filter coefficients
window_type = 'hamming'  # Type of window function

# Design the FIR filter using the windowing method
filter_coefficients = design_fir_filter(cutoff_frequency, filter_length, window_type)

# Plot the filter's magnitude response and impulse response
plot_filter_response(filter_coefficients)

# Save the filter coefficients (optional)
filter_path = 'fir_filter_coefficients.txt'
np.savetxt(filter_path, filter_coefficients, delimiter=',')
print(f"Filter coefficients saved at: {filter_path}")
'''
'''
import numpy as np
import matplotlib.pyplot as plt

def plot_signal_and_spectrum(signal, spectrum):
    # Create time axis for plotting
    time_axis = np.arange(len(signal))

    # Plot the original signal
    plt.subplot(2, 1, 1)
    plt.plot(time_axis, signal)
    plt.title('Original Signal')
    plt.xlabel('Time')
    plt.ylabel('Amplitude')

    # Plot the magnitude spectrum
    plt.subplot(2, 1, 2)
    plt.plot(time_axis, spectrum)
    plt.title('Magnitude Spectrum')
    plt.xlabel('Frequency')
    plt.ylabel('Magnitude')

    plt.tight_layout()
    plt.show()

# Define the discrete-time signal
time = np.linspace(0, 1, 500)
frequency1 = 5  # Frequency of the first sinusoidal component
frequency2 = 20  # Frequency of the second sinusoidal component
amplitude1 = 1  # Amplitude of the first sinusoidal component
amplitude2 = 0.5  # Amplitude of the second sinusoidal component
signal = amplitude1 * np.sin(2 * np.pi * frequency1 * time) + amplitude2 * np.sin(2 * np.pi * frequency2 * time)

# Compute the FFT of the signal
fft_result = np.fft.fft(signal)

# Compute the magnitude spectrum of the FFT result
magnitude_spectrum = np.abs(fft_result)

# Compute the IFFT of the FFT result
reconstructed_signal = np.fft.ifft(fft_result)

# Display the original signal, the magnitude spectrum, and the reconstructed signal
plot_signal_and_spectrum(signal, magnitude_spectrum)

# Save the magnitude spectrum plot (optional)
spectrum_path = 'magnitude_spectrum.png'
plt.plot(magnitude_spectrum)
plt.title('Magnitude Spectrum')
plt.xlabel('Frequency')
plt.ylabel('Magnitude')
plt.savefig(spectrum_path)
print(f"Magnitude spectrum plot saved at: {spectrum_path}")'''

'''
import cv2

def perform_gray_level_operation(image, operation):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform the desired gray level operation
    if operation == 'contrast':
        # Perform contrast adjustment
        contrast_image = cv2.equalizeHist(gray_image)
        processed_image = cv2.cvtColor(contrast_image, cv2.COLOR_GRAY2BGR)
    elif operation == 'brightness':
        # Perform brightness correction
        alpha = 1.5  # brightness factor
        processed_image = cv2.convertScaleAbs(gray_image, alpha=alpha)
        processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)
    elif operation == 'thresholding':
        # Perform image thresholding
        _, threshold_image = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
        processed_image = cv2.cvtColor(threshold_image, cv2.COLOR_GRAY2BGR)
    else:
        print("Invalid operation. Available operations: 'contrast', 'brightness', 'thresholding'")
        return None

    return processed_image

# Load the input image
image_path = 'input_image.jpg'
input_image = cv2.imread(image_path)

# Perform gray level operation
operation_type = 'contrast'  # Change this to the desired operation: 'contrast', 'brightness', 'thresholding'
output_image = perform_gray_level_operation(input_image, operation_type)

if output_image is not None:
    # Display the processed image
    cv2.imshow('Processed Image', output_image)
    cv2.waitKey(0)

    # Save the processed image (optional)
    output_path = 'output_image.jpg'
    cv2.imwrite(output_path, output_image)
    print(f"Processed image saved at: {output_path}")'''

'''    
import cv2
import numpy as np
import matplotlib.pyplot as plt

def generate_histogram(image):
    # Calculate the histogram of the image
    histogram = cv2.calcHist([image], [0], None, [256], [0, 256])
    return histogram

def perform_histogram_equalization(image):
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply histogram equalization
    equalized_image = cv2.equalizeHist(gray_image)
    return equalized_image

def perform_histogram_matching(input_image, reference_image):
    # Convert images to grayscale
    gray_input = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    gray_reference = cv2.cvtColor(reference_image, cv2.COLOR_BGR2GRAY)

    # Calculate histograms
    input_hist = generate_histogram(gray_input)
    reference_hist = generate_histogram(gray_reference)

    # Perform histogram matching
    matched_image = cv2.matchHistograms(gray_input, gray_reference, method=cv2.HISTCMP_HELLINGER)

    return matched_image

# Load the input image
input_path = 'input_image.jpg'
input_image = cv2.imread(input_path)

# Generate and display the histogram of the input image
input_hist = generate_histogram(input_image)
plt.plot(input_hist)
plt.title("Input Image Histogram")
plt.xlabel("Intensity")
plt.ylabel("Frequency")
plt.show()

# Perform histogram equalization
equalized_image = perform_histogram_equalization(input_image)

# Generate and display the histogram of the equalized image
equalized_hist = generate_histogram(equalized_image)
plt.plot(equalized_hist)
plt.title("Equalized Image Histogram")
plt.xlabel("Intensity")
plt.ylabel("Frequency")
plt.show()

# Load the reference image for histogram matching
reference_path = 'reference_image.jpg'
reference_image = cv2.imread(reference_path)

# Perform histogram matching
matched_image = perform_histogram_matching(input_image, reference_image)

# Generate and display the histogram of the matched image
matched_hist = generate_histogram(matched_image)
plt.plot(matched_hist)
plt.title("Matched Image Histogram")
plt.xlabel("Intensity")
plt.ylabel("Frequency")
plt.show()'''

'''
import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_smoothing_filter(image, kernel_size):
    # Apply smoothing filter to the image
    smoothed_image = cv2.blur(image, (kernel_size, kernel_size))
    return smoothed_image

def apply_sharpening_filter(image):
    # Create a sharpening kernel
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])

    # Apply the sharpening kernel to the image
    sharpened_image = cv2.filter2D(image, -1, kernel)
    return sharpened_image

# Load the input image
image_path = 'input_image.jpg'
input_image = cv2.imread(image_path)

# Apply smoothing filter
smoothed_image = apply_smoothing_filter(input_image, kernel_size=5)

# Apply sharpening filter
sharpened_image = apply_sharpening_filter(input_image)

# Display the original image and the filtered images side by side
combined_image = np.hstack((input_image, smoothed_image, sharpened_image))
cv2.imshow("Original | Smoothed | Sharpened", combined_image)
cv2.waitKey(0)

# Save the filtered images (optional)
smoothed_path = 'smoothed_image.jpg'
sharpened_path = 'sharpened_image.jpg'
cv2.imwrite(smoothed_path, smoothed_image)
cv2.imwrite(sharpened_path, sharpened_image)
print(f"Smoothed image saved at: {smoothed_path}")
print(f"Sharpened image saved at: {sharpened_path}")'''

'''
import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_median_filter(image, kernel_size):
    # Apply median filter to remove noise
    filtered_image = cv2.medianBlur(image, kernel_size)
    return filtered_image

def apply_bilateral_filter(image, d, sigma_color, sigma_space):
    # Apply bilateral filter to remove noise
    filtered_image = cv2.bilateralFilter(image, d, sigma_color, sigma_space)
    return filtered_image

# Load the input image
image_path = 'input_image.jpg'
input_image = cv2.imread(image_path)

# Apply median filter
median_filtered_image = apply_median_filter(input_image, kernel_size=5)

# Apply bilateral filter
bilateral_filtered_image = apply_bilateral_filter(input_image, d=9, sigma_color=75, sigma_space=75)

# Display the original image and the filtered images side by side
combined_image = np.hstack((input_image, median_filtered_image, bilateral_filtered_image))
cv2.imshow("Original | Median Filtered | Bilateral Filtered", combined_image)
cv2.waitKey(0)

# Save the filtered images (optional)
median_filtered_path = 'median_filtered_image.jpg'
bilateral_filtered_path = 'bilateral_filtered_image.jpg'
cv2.imwrite(median_filtered_path, median_filtered_image)
cv2.imwrite(bilateral_filtered_path, bilateral_filtered_image)
print(f"Median filtered image saved at: {median_filtered_path}")
print(f"Bilateral filtered image saved at: {bilateral_filtered_path}")'''

'''
import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_gaussian_filter(image, sigma):
    # Convert image to float32 for Fourier Transform
    image = np.float32(image)

    # Perform Fourier Transform
    frequency_domain = cv2.dft(image, flags=cv2.DFT_COMPLEX_OUTPUT)

    # Shift the zero-frequency component to the center of the spectrum
    shifted_frequency_domain = np.fft.fftshift(frequency_domain)

    # Create Gaussian filter mask
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.zeros((rows, cols, 2), np.float32)
    for i in range(rows):
        for j in range(cols):
            mask[i, j] = np.exp(-((i - crow) ** 2 + (j - ccol) ** 2) / (2 * sigma ** 2))

    # Apply the Gaussian filter in the frequency domain
    filtered_frequency_domain = shifted_frequency_domain * mask

    # Shift the zero-frequency component back to the corner
    shifted_filtered_frequency_domain = np.fft.fftshift(filtered_frequency_domain)

    # Perform Inverse Fourier Transform to obtain the filtered image
    filtered_image = cv2.idft(shifted_filtered_frequency_domain, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)

    # Convert the filtered image back to uint8
    filtered_image = np.uint8(filtered_image)

    return filtered_image

def apply_sharpening_filter(image, strength):
    # Convert image to float32 for Fourier Transform
    image = np.float32(image)

    # Perform Fourier Transform
    frequency_domain = cv2.dft(image, flags=cv2.DFT_COMPLEX_OUTPUT)

    # Shift the zero-frequency component to the center of the spectrum
    shifted_frequency_domain = np.fft.fftshift(frequency_domain)

    # Create high-pass filter mask
    rows, cols = image.shape
    crow, ccol = rows // 2, cols // 2
    mask = np.zeros((rows, cols, 2), np.float32)
    mask[crow - strength:crow + strength, ccol - strength:ccol + strength] = 1

    # Apply the high-pass filter in the frequency domain
    filtered_frequency_domain = shifted_frequency_domain * mask

    # Shift the zero-frequency component back to the corner
    shifted_filtered_frequency_domain = np.fft.fftshift(filtered_frequency_domain)

    # Perform Inverse Fourier Transform to obtain the filtered image
    filtered_image = cv2.idft(shifted_filtered_frequency_domain, flags=cv2.DFT_SCALE | cv2.DFT_REAL_OUTPUT)

    # Convert the filtered image back to uint8
    filtered_image = np.uint8(filtered_image)

    return filtered_image

# Load the input image
image_path = "C:/Users/Acer/OneDrive/Pictures/Screenshots/React/react_1.png"
input_image = cv2.imread(image_path, 0)  # Load the image in grayscale

# Apply Gaussian filter
sigma = 20  # Adjust the value to control the amount of smoothing
smoothed_image = apply_gaussian_filter(input_image, sigma)

# Apply sharpening filter
strength = 20  # Adjust the value to control the strength of sharpening
sharpened_image = apply_sharpening_filter(input_image, strength)

# Display the original image and the filtered images side by side
combined_image = np.hstack((input_image, smoothed_image, sharpened_image))
plt.imshow(combined_image, cmap='gray')
plt.title("Original | Smoothed | Sharpened")
plt.axis('off')
plt.show()

# Save the filtered images (optional)
smoothed_path = 'smoothed_image.jpg'
sharpened_path = 'sharpened_image.jpg'
cv2.imwrite(smoothed_path, smoothed_image)
cv2.imwrite(sharpened_path, sharpened_image)
print(f"Smoothed image saved at: {smoothed_path}")
print(f"Sharpened image saved at: {sharpened_path}")'''

'''
import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_dilation(image, kernel):
    # Apply dilation operation to the image
    dilated_image = cv2.dilate(image, kernel, iterations=1)
    return dilated_image

def apply_erosion(image, kernel):
    # Apply erosion operation to the image
    eroded_image = cv2.erode(image, kernel, iterations=1)
    return eroded_image

def apply_opening(image, kernel):
    # Apply opening operation to the image (erosion followed by dilation)
    opened_image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
    return opened_image

def apply_closing(image, kernel):
    # Apply closing operation to the image (dilation followed by erosion)
    closed_image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return closed_image

# Load the input image
image_path = "C:/Users/Acer/OneDrive/Pictures/Screenshots/React/react_1.png"
input_image = cv2.imread(image_path, 0)  # Load the image in grayscale

# Create structuring elements for dilation, erosion, opening, and closing operations
kernel_dilation = np.ones((5, 5), np.uint8)
kernel_erosion = np.ones((5, 5), np.uint8)
kernel_opening = np.ones((5, 5), np.uint8)
kernel_closing = np.ones((5, 5), np.uint8)

# Apply dilation operation
dilated_image = apply_dilation(input_image, kernel_dilation)

# Apply erosion operation
eroded_image = apply_erosion(input_image, kernel_erosion)

# Apply opening operation
opened_image = apply_opening(input_image, kernel_opening)

# Apply closing operation
closed_image = apply_closing(input_image, kernel_closing)

# Display the original image and the resulting images after each operation
fig, axs = plt.subplots(2, 2)
axs[0, 0].imshow(input_image, cmap='gray')
axs[0, 0].set_title('Original Image')

axs[0, 1].imshow(dilated_image, cmap='gray')
axs[0, 1].set_title('Dilated Image')

axs[1, 0].imshow(eroded_image, cmap='gray')
axs[1, 0].set_title('Eroded Image')

axs[1, 1].imshow(opened_image, cmap='gray')
axs[1, 1].set_title('Opened Image')

for ax in axs.flat:
    ax.axis('off')

plt.show()

# Save the resulting images (optional)
dilated_path = 'dilated_image.jpg'
eroded_path = 'eroded_image.jpg'
opened_path = 'opened_image.jpg'
cv2.imwrite(dilated_path, dilated_image)
cv2.imwrite(eroded_path, eroded_image)
cv2.imwrite(opened_path, opened_image)
print(f"Dilated image saved at: {dilated_path}")
print(f"Eroded image saved at: {eroded_path}")
print(f"Opened image saved at: {opened_path}")
'''

'''
import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_hit_or_miss(image, foreground, background):
    # Apply Hit or Miss transformation
    hit_or_miss_image = cv2.morphologyEx(image, cv2.MORPH_HITMISS, np.array([foreground, background], dtype=np.uint8))
    return hit_or_miss_image

# Load the input image
image_path = "C:/Users/Acer/OneDrive/Pictures/Screenshots/React/react_1.png"
input_image = cv2.imread(image_path, 0)  # Load the image in grayscale

# Define the foreground and background structuring elements
foreground = np.array([[0, 1, 0], [0, 1, 1], [0, 0, 0]], dtype=np.uint8)
background = np.array([[1, 0, 1], [1, 0, 0], [1, 1, 1]], dtype=np.uint8)

# Apply Hit or Miss transformation
result_image = apply_hit_or_miss(input_image, foreground, background)

# Display the original image and the resulting image after the transformation
fig, axs = plt.subplots(1, 2)
axs[0].imshow(input_image, cmap='gray')
axs[0].set_title('Original Image')

axs[1].imshow(result_image, cmap='gray')
axs[1].set_title('Hit or Miss Transformation')

for ax in axs:
    ax.axis('off')

plt.show()

# Save the resulting image (optional)
result_path = 'result_image.jpg'
cv2.imwrite(result_path, result_image)
print(f"Resulting image saved at: {result_path}")'''

import cv2
import numpy as np
import matplotlib.pyplot as plt

def extract_boundary(image):
    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply morphological dilation to the grayscale image
    kernel = np.ones((3, 3), np.uint8)
    dilated_image = cv2.dilate(grayscale_image, kernel, iterations=1)

    # Subtract the grayscale image from the dilated image to obtain the boundary image
    boundary_image = dilated_image - grayscale_image

    return boundary_image

# Load the input image
image_path = "C:/Users/Acer/OneDrive/Pictures/Screenshots/React/react_1.png"
input_image = cv2.imread(image_path)

# Extract the boundary from the input image
boundary_image = extract_boundary(input_image)

# Display the original image and the boundary image
fig, axs = plt.subplots(1, 2)
axs[0].imshow(cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB))
axs[0].set_title('Original Image')

axs[1].imshow(boundary_image, cmap='gray')
axs[1].set_title('Boundary Image')

for ax in axs:
    ax.axis('off')

plt.show()

# Save the boundary image (optional)
boundary_path = 'boundary_image.jpg'
cv2.imwrite(boundary_path, boundary_image)
print(f"Boundary image saved at: {boundary_path}")






    