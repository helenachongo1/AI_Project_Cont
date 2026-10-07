import cv2
import numpy as np
from matplotlib import pyplot as plt
#from google.colab.patches import cv2_imshow

# Load the input grayscale image
image = cv2.imread("D:/ICT_2025/DSIP/images/ex1_2.png", cv2.IMREAD_GRAYSCALE)

# Check if the image is loaded successfully
if image is None:
    print("Error: Could not open or find the image.")
    exit()

# Function to perform image negation
def image_negation(input_image):
    negated_image = 255 - input_image
    return negated_image

# Function to perform image thresholding
def image_thresholding(input_image, threshold_value):
    _, thresholded_image = cv2.threshold(input_image, threshold_value, 255, cv2.THRESH_BINARY)
    return thresholded_image

# Function to perform image gamma correction
def image_gamma_correction(input_image, gamma):
    gamma_corrected_image = np.power(input_image / 255.0, gamma) * 255.0
    gamma_corrected_image = np.uint8(gamma_corrected_image)
    return gamma_corrected_image

# Perform gray level operations
negated_image = image_negation(image)
thresholded_image = image_thresholding(image, 128)
gamma_corrected_image = image_gamma_correction(image, 0.5)

def show_image(img, title='Image'):
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

# Use this function to show all your images
show_image(image, 'Original Image')
show_image(negated_image, 'Negated Image')
show_image(thresholded_image, 'Thresholded Image')
show_image(gamma_corrected_image, 'Gamma Corrected Image')


# Wait for a key press and then close the windows
cv2.waitKey(0)
cv2.destroyAllWindows()
