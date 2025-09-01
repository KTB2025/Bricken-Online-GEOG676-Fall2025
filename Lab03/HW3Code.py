# TAMU GIS Programming: Homework 03 - Fun with object oriented programming
# Author: Kate Bricken
# Date: 09/01/2025

import math # Access Python's built in math module for more precise/accurate calculations

# -------------------------------
# Define Shape Classes
# -------------------------------

class Shape(): # Base class for all shapes
    def get_area(self): #Placeholder for area calculation
        pass

    def __str__(self):  # Returns a human readable string showing the shape type and area
        return f"{type(self).__name__} with area {self.get_area():.2f}"

    def __len__(self):  #  Enables use of len(shape) to get the shape's area as an integer
        return int(self.get_area())

class Rectangle(Shape): #  Rectangle shape, defined by length and width
    def __init__(self,l,w):
        self.length = l
        self.width = w
    def get_area(self):
        return self.length * self.width

class Circle(Shape): # Circle shape, defined by radius
    def __init__(self,r):
        self.radius = r
    def get_area(self):
        return math.pi * self.radius * self.radius # Use the exact value of pi
    
class Triangle(Shape): # Triangle shape, defined by base and height
    def __init__(self,b,h):
        self.base = b
        self.height = h
    def get_area(self):
        return 0.5 * self.base * self.height 
    
# -------------------------------
# Read Shape.Txt File
# -------------------------------
from pathlib import Path

file_path = Path(__file__).resolve().parent / 'shape.txt' # Build a path to 'shape.txt' in the same directory as this code


with open(file_path, 'r') as file:
    lines = file.readlines() # Read each line of the file into a list of strings


# -------------------------------
# For each line, create a new object determined by the shape & add to a list
# -------------------------------

shapes = []  # Create list to hold all shape objects

for line in lines:
    components = line.strip().split(',')  # split line by commas
    shape_type = components[0] # First element is the shape type

    # Based on shape type, initialize appropriate object and add to list
    if shape_type == 'Rectangle':
        shapes.append(Rectangle(float(components[1]), float(components[2])))
    elif shape_type == 'Circle':
        shapes.append(Circle(float(components[1])))
    elif shape_type == 'Triangle':
        shapes.append(Triangle(float(components[1]), float(components[2])))

# -------------------------------
# Iterate through your list and print out the area for each shape
# -------------------------------

for shape in shapes:
    print(shape)  # Calls __str__ method, prints shape type and area
    print(f"Area as integer (using __len__): {len(shape)}")  # Calls __len__, converts area to int