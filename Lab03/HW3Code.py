#TAMU GIS Programming: Homework 03 - Fun with object oriented programming
##Read data in from the provided text file found here (20pt)
##Create a class for each shape found in the text file (20pt)
##For each line, create a new object determined by the shape (e.g. Triangle object for line Triangle,8,1 base and height) (30pt)
##Iterate through your list and print out the area for each shape (30pt)
import math
#Define Shape Classes
class Shape():
    def get_area(self):
        pass

class Rectangle(Shape):
    def __init__(self,l,w):
        self.length = l
        self.width = w
    def get_area(self):
        return self.length * self.width 
    
class Circle(Shape):
    def __init__(self,r):
        self.radius = r
    def get_area(self):
        return math.pi * self.radius * self.radius
    
class Triangle(Shape):
    def __init__(self,b,h):
        self.base = b
        self.height = h
    def get_area(self):
        return 0.5 * self.base * self.height 
    
#Read Txt File
file = open(r'C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025\Lab03\shape.txt','r')
lines = file.readlines()
file.close()

#For each line, create a new object determined by the shape & print out the area for each shape
for line in lines:
    components = line.split(',')
    Shape_Type = components[0].strip()

    if Shape_Type == 'Rectangle':
        rect = Rectangle(float(components[1]),float(components[2]))
        print('Area of Rectangle is:',rect.get_area())
    elif Shape_Type == 'Circle':
        circl = Circle(float(components[1]))
        print('Area of Circle is:',circl.get_area())
    elif Shape_Type == 'Triangle':
        tri = Triangle(float(components[1]),float(components[2]))
        print('Area of triangle is:',tri.get_area())
    else:
        pass