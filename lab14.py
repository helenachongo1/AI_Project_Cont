'''class Car:
    # Constructor to initialize the object
    def __init__(self, brand, model):
        self.brand = brand  # Attribute
        self.model = model  # Attribute

    # Method to describe the car
    def car_details(self):
        return f"Car: {self.brand}, Model: {self.model}"

# Creating an object of the Car class
my_car = Car("Toyota", "Corolla")
print(my_car.car_details())'''

'''class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    # Method to calculate area
    def area(self):
        return self.width * self.height

    # Method to calculate perimeter
    def perimeter(self):
        return 2 * (self.width + self.height)

# Create an object
rect = Rectangle(10, 5)

# Accessing methods
print(f"Area: {rect.area()}")  # Output: Area: 50
print(f"Perimeter: {rect.perimeter()}") '''

#Q1
'''import numpy as np
class Circle:
    def __init__(self,radius):
        self.radius=radius
        
    def area(self):
        return np.pi*self.radius*self.radius
    
    def perimeter(self):
        return 2*np.pi*self.radius
 
x=int(input("Enter a value of radius: "))
circ=Circle(x)
print(f"Area of circle: {circ.area()}")
print(f"Perimeter of circle: {circ.perimeter()}")'''

#Q2
'''class Book:
    def __init__(self,title,author,price):
        self.title=title
        self.author=author
        self.price=price
        
    def display(self):
        return {self.title,self.author,self.price}
    
    def discount(self):
        return self.price-(0.1*self.price)
    
title_book=input("Enter the title of book:")
author_name=input("Enter the name of author:")
n_price=int(input("Enter the price of the book:"))

title_book1=input("Enter the title of book:")
author_name1=input("Enter the name of author:")
n_price1=int(input("Enter the price of the book:"))

print("\n")
book=Book(title_book,author_name,n_price)
n_book=Book(title_book1,author_name1,n_price1)

print(f"Details: {book.display()}")
print(f"Details: {n_book.display()}")

print(f"Discount of the book1: {book.discount()}")
print(f"Discount of the book2: {n_book.discount()}")'''


'''class BankAccount:
    def __init__(self, account_holder, balance):
        self.account_holder = account_holder
        self.__balance = balance  # Private attribute

    def deposit(self, amount):
        self.__balance += amount

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
        else:
            print("Insufficient funds")

    def get_balance(self):
        return self.__balance

# Create an account
account = BankAccount("John", 1000)
account.deposit(500)
print(account.get_balance())  # 
account.withdraw(700)
print(account.get_balance())  # '''

'''class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "I am an animal."

# Dog class inherits from Animal class
class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

# Cat class inherits from Animal class
class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

dog = Dog("Buddy")
cat = Cat("Whiskers")
print(dog.speak())  # 
print(cat.speak()) '''

'''class Polygon:
    # method to render a shape
    def render(self):
        print("Rendering Polygon...")

class Square(Polygon):
    # renders Square
    def render(self):
        print("Rendering Square...")

class Circle(Polygon):
    # renders circle
    def render(self):
        print("Rendering Circle...")
    
# create an object of Square
s1 = Square()
s1.render()

# create an object of Circle
c1 = Circle()
c1.render()'''

'''from abc import ABC, abstractmethod

# Abstract class
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius * self.radius

circle = Circle(5)
print(f"Area of the circle: {circle.area()}")'''

 

 
 

