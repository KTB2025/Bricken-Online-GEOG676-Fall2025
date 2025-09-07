TAMU GIS Programming: Homework 04
Topic: Fun with arcpy

Outcomes
Learn how to build an iterator.
Learn several of the general purpose container data types.
Learn how to use Arcpy to 1) setup a workspace; 2) create a geodatabase; and 3) find example arcpy code.
Learn how to manipulate feature layers and perform some basic spatial analysis (e.g. buffering, intersection) using arcpy.
Task:
Read in garage location X/Y coords from the provided .csv
Create a geodatabase and add in the input layers
Buffer the garage points
Intersect the buildings layer with the buffered garage points
Output the resulting table to a .csv
To Hand In:
Link to your Github page that contains the Python code, GDB, and CSV resulting table.
Screenshot of the executed code.
Fun with arcpy
In this homework assignment, you will be creating a Python script that will determine which buildings on TAMU's main campus intersect with it's various garages.

1. Read x/y coords
Using the text file here, read in these data points. These are the locations of various parking garages around the TAMU campus.

2. Create a geodatabase
With your text file parsed and your garage points available, create a new geodatabase and add in the garage data. Once you have garages added in, use the Structures layer in the Campus.gdb found here for the intersection. You'll probably want to copy the Structures feature class into your geodatabase.

3. Buffer the garages
Use the buffer tool covered in the "Basic operations" lecture to create a buffer around the garages. You should get the buffer distance value from the user using the input() method covered previously. The distance for the buffer should be in meters.

4. Intersect the two files
With both the garage layer and the building layers present, perform an intersection on these two layers and add the resulting layer to your geodatabase.

5. Output the intersection table
With your intersection complete, output the resulting layer's attribute table as a .csv.

