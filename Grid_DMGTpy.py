from PIL import Image
import numpy as np

image = Image.open("C:/Users/Acer/Downloads/Map_1.png")

g_image = image.convert("L")

image_matrix = np.array(g_image)
threshold = 128

b_matrix = (image_matrix > threshold).astype(int)

import matplotlib.pyplot as plt

plt.imshow(b_matrix, cmap='gray')
plt.show()


#print(b_matrix)