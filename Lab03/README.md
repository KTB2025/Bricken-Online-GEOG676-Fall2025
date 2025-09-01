# TAMU GIS Programming: Homework 03 — Fun with Object Oriented Programming

**Author:** Kate Bricken  
**Course:** GEOG 676 - GIS Programming  
**Assignment Due Date:** September 15, 2025  

---

## Assignment Overview

This assignment demonstrates the use of **object-oriented programming (OOP)** in Python to calculate the area of various shapes based on input from a text file. The focus is on class creation, inheritance, file reading, and use of special methods like `__str__` and `__len__`.

---

## Tasks

1. Read data in from the provided text file found here (`shape.txt`)  
2. Create a class for each shape found in the text file `Rectangle`, `Circle`, `Triangle`  
3. For each line, create a new object determined by the shape (e.g. Triangle object for line Triangle,8,1 base and height)
4. Iterate through your list and print out the area for each shape  `get_area()`, `__str__()`, and `__len__()`  

---

## Project Files
Lab03
│ 
├── HW3Code.py # Python script with OOP implementation
├── README.md # This file that you're currently reading
└── shape.txt # Input file with shape data (e.g., "Rectangle,5,6")


---

## How It Works

1. The script reads shape definitions from `shape.txt`.
2. Each line defines a shape and its dimensions (e.g., `Circle,3`).
3. A corresponding shape object is created using a class (`Rectangle`, `Circle`, `Triangle`).
4. Each object calculates its area and prints:
   - A formatted string using the `__str__()` method
   - The integer version of the area using the `__len__()` method

---

## Code Output
- Rectangle with area 5.00
- Area as integer (using __len__): 5
- Circle with area 28.27
- Area as integer (using __len__): 28
- Triangle with area 4.00
- Area as integer (using __len__): 4
- Triangle with area 13.50
- Area as integer (using __len__): 13
- Triangle with area 20.00
- Area as integer (using __len__): 20
- Circle with area 28.27
- Area as integer (using __len__): 28
- Rectangle with area 8.00
- Area as integer (using __len__): 8
- Rectangle with area 30.00
- Area as integer (using __len__): 30
- Triangle with area 10.00
- Area as integer (using __len__): 10
- Circle with area 254.47
- Area as integer (using __len__): 254

---

## Screenshot of Executed Code

![HW03 Screenshot #1](https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/blob/main/Lab03/Bricken_GEOG676_HW3.png?raw=true)
![HW03 Screenshot #2](https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/blob/main/Lab03/Bricken_GEOG676_HW3_2.png?raw=true)
![HW03 Screenshot #3](https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/blob/main/Lab03/Bricken_GEOG676_HW3_3.png?raw=true)
![HW03 Screenshot #4](https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/blob/main/Lab03/Bricken_GEOG676_HW3_4.png?raw=true)

---

## Submission Items

- Python script uploaded to GitHub
- shape.txt file in the same directory
- Screenshots of executed code output
- Link submitted to Canvas
- This incredibly informative README.md file

---

## Additional Resources Used

- [Python OOP Docs](https://docs.python.org/3/tutorial/classes.html)
- [Using `split()` for String Parsing](https://docs.python.org/3/library/stdtypes.html#str.split)
- [Python Magic Methods (`__str__`, `__len__`)](https://rszalski.github.io/magicmethods/)

---
