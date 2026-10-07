
'''print('# of dims: ',img_array.ndim)     
print('Img shape: ',img_array.shape)   
print('Dtype: ',img_array.dtype)
print(img_array[20, 20])                
print(img_array[:, :, 2].min())
w,h=img.size
print("Weigth=",w)
print("Height=",h)      
plt.imshow(img_array)
plt.title('Original Image')'''

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
img = Image.open(r'C:\Users\Acer\Downloads\vecteezy_holi-powder-splash-colorful-colorful-powder-explosion_22906073.png')
img_array = np.array(img)
img_grey = img_array.sum(2) / (255*3)
imgg = img_grey.copy()
plt.imshow(imgg)

'''img_R, img_G, img_B = img_array.copy(), img_array.copy(), img_array.copy()
img_R[:, :, (1, 2)] = 0
img_G[:, :, (0, 2)] = 0
img_B[:, :, (0, 1)] = 0
img_rgb = np.concatenate((img_R,img_G,img_B), axis=1)
plt.figure(figsize=(15, 15))
plt.imshow(img_rgb)'''


'''image1 = (img_array // 64) * 64
image2 = (img_array // 128) * 128
img_all = np.concatenate((img, image1, image2), axis=1)
plt.figure(figsize=(15, 15))
plt.imshow(img_all)'''


