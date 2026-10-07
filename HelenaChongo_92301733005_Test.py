#Q1
import numpy as np

def find_primes(n):#function to find is the number is prime or not
    if n<= 1:
        return False
    for i in range(2, int(n**0.5) +1):
        if n % i ==0:
            return False
    return True

def find_prime_array(arr):#function to extract and check each element of array 
    prime_numbers = []#new array to store thr prime numbers
    
    for row in arr:
        for i in row:
            if find_primes(i):#After extract the number, we call the function to check whether the number is prime or not
                prime_numbers.append(i)
    return prime_numbers
     
arr=np.array([[1,3,5,7],
              [12,14,27,11],
             [21,34,56,98],
             [71,12,51,9]])

print(find_prime_array(arr))


#Q2

class Car:
    number_of_wheels=4
    # Constructor to initialize the object
    def __init__(self, brand, model, year):
        self.brand = brand  # Attribute
        self.model = model  # Attribute
        self.year = year    # Atribute

    # Method to describe the car
    def car_info(self):
        return f"Car: {self.brand}, Model: {self.model}, Year: {self.year} with {Car.number_of_wheels} wheels"

# Creating an object of the Car class
m_car = Car("Toyota", "Corolla", 1997)
m_car1 = Car("Toyota", "Mercedes", 1995)
print(m_car.car_info())
print(m_car1.car_info())

#Q3
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

#to open the images 
img = Image.open(r"C:/Users/Acer/OneDrive/Pictures/Saved Pictures/page1.jpg")
img_1 = Image.open(r"C:/Users/Acer/OneDrive/Pictures/Saved Pictures/page2.jpg")
img_array = np.array(img)
img_arr = np.array(img_1)

arr_mul = img_array * img_arr #multiply the matrices of the two images 

img = arr_mul.sum(2) / (255*3) # As a form to normalize the result
img = np.clip(img, 0, 1) # Clip the values to prevent display issues
plt.imshow(img)
#plt.axis('off') # Optional
plt.show()

