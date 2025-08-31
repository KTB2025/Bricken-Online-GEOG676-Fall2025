# TAMU GIS Programming: Homework 04 — Fun with arcpy

**Author:** Kate Bricken  
**Course:** GEOG 676 - GIS Programming  
**Assignment Date:** September 22, 2025

---

## Assignment Overview

This Python script uses **ArcPy** to analyze the spatial relationship between parking garages and buildings on the Texas A&M University campus. The goal is to determine which buildings fall within a user-defined buffer distance from each garage.

---

## Tasks

1. Read garage X/Y coordinates and names from a CSV file.
2. Create a file geodatabase to store output data.
3. Convert CSV data to a point feature class.
4. Buffer the garage points using user input.
5. Intersect the buffered points with the building layer.
6. Output the intersected attribute table as a `.csv`.

---

## Project Structure
Lab04/
│
├── garages.csv # Input data containing X/Y locations of garages
├── Campus.gdb/ # Provided geodatabase with Structures layer
├── HW04.gdb/ # Created geodatabase with all outputs
│ ├── Garages
│ ├── Structures
│ ├── GarageBuffers
│ └── GarageBuilding_Intersect
├── garage_building_intersections.csv # Final result table
├── HW4Code.py # Python script using ArcPy
└── This README.md file


---

## How to Run

1. Open **ArcGIS Pro** or a Python script environment with ArcPy access.
2. Update file paths in `HW4Code.py` if necessary.
3. Run the script.
4. When prompted, enter a **buffer distance in meters** (e.g., `100`).
5. Check the folder for the exported CSV file with intersection results.

---

## Expected Output

The output CSV includes the names and IDs of garages and any buildings that fall within the buffer zone.

| FAC_CODE | Name | StructureID | StructureName |
|----------|------|-------------|----------------|
| CCG      | CCG  | 1021        | Academic Building |
| NSG      | NSG  | 1044        | Engineering Lab  |

---

## Notes

- Make sure your `Campus.gdb` and `garages.csv` are located in the project folder.
- Field names in your input CSV must include `X`, `Y`, `FAC_CODE`, and `Name`.

---

## Screenshot of Script Execution

> *(Insert screenshot here once completed!!!!)

---

## Submission Items

- Python script (.py)
- Geodatabase with output layers (.gdb)
- Output CSV (.csv)
- Screenshots of executed script (.png or .jpg)
- This README.md