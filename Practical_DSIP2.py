
import cv2
import numpy as np
import matplotlib.pyplot as plt

def apply_hit_or_miss(image, foreground, background):
    hit_or_miss_image = cv2.morphologyEx(image, cv2.MORPH_HITMISS, np.array([foreground, background], dtype=np.uint8))
    return hit_or_miss_image

# Load the input image
image_path = "C:/Users/Acer/Downloads/Datasets Practical Exam-1/Datasets Practical Exam/Image processing/2222.png"
input_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  

# Define the foreground and background structuring elements
foreground = np.array([[0, 1, 0], [0, 1, 1], [0, 0, 0]], dtype=np.uint8)
background = np.array([[1, 0, 1], [1, 0, 0], [1, 1, 1]], dtype=np.uint8)

result_image = apply_hit_or_miss(input_image, foreground, background)

fig, axs = plt.subplots(1, 2)
axs[0].imshow(input_image, cmap='gray')
axs[0].set_title('Original Image')

axs[1].imshow(result_image, cmap='gray')
axs[1].set_title('Hit or Miss Transformation')

for ax in axs:
    ax.axis('off')

plt.show()

'''

import cv2
import numpy as np
import matplotlib.pyplot as plt

def extract_boundary(image):
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    kernel = np.ones((3, 3), np.uint8)
    dilated_image = cv2.dilate(grayscale_image, kernel, iterations=1)

    boundary_image = dilated_image - grayscale_image

    return boundary_image

# Load the input image
image_path = 'C:/Users/Acer/Downloads/Datasets Practical Exam-1/Datasets Practical Exam/Image processing/2222.png'
input_image = cv2.imread(image_path)

boundary_image = extract_boundary(input_image)

fig, axs = plt.subplots(1, 2)
axs[0].imshow(cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB))
axs[0].set_title('Original Image')

axs[1].imshow(boundary_image, cmap='gray')
axs[1].set_title('Boundary Image')

for ax in axs:
    ax.axis('off')

plt.show()
boundary_path = 'boundary_image.jpg'
cv2.imwrite(boundary_path, boundary_image)
print(f"Boundary image saved at: {boundary_path}")


# Save the resulting image (optional)
result_path = 'result_image.jpg'
cv2.imwrite(result_path, result_image)
print(f"Resulting image saved at: {result_path}")'''
