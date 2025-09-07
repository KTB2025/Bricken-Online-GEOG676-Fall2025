# TAMU GIS Programming: Homework 04 — Fun with ArcPy
 
**Author:** Kate Bricken  
**Course:** GEOG 676 — GIS Programming  
**Assignment Due Date:** September 22, 2025  
 
---
 
## Overview
This script uses **ArcPy** to determine which TAMU campus buildings intersect with user defined buffer zones around parking garages. It runs reproducibly by resetting a clean results/ folder each time.

Script Pipeline:
1. Builds a point feature class from a CSV of garage coordinates 
2. Copy **Structures** into a working GDB 
3. Projects garages to match the **Structures** layer  
4. Creates buffers from a user input in meters  
5. Intersects those buffers with **Structures**  
6. Exports a clean results table as a CSV  
 
---
 

---

## How it Works

1. **CSV → Points (WGS84)**  
   Reads `data/garages.csv` (expects columns `X`, `Y`, `Name`) and creates `Garages` in `results/HW04.gdb` with `SpatialReference(4326)`.

2. **Copy Structures**  
   Copies `data/Campus.gdb/Structures` into `results/HW04.gdb` so all processing occurs in one geodatabase.

3. **Project Garages**  
   Projects `Garages` to the **same coordinate system as `Structures`** → `Garages_proj` (so buffer units are correct).

4. **Buffer**  
   Buffers `Garages_proj` → `GarageBuffers` using a user-provided distance like `100 Meters`.

5. **Intersect**  
   Intersects `GarageBuffers` with `Structures` → `GarageBuilding_Intersect`.

6. **Export CSV**  
   Exports the `GarageBuilding_Intersect` attribute table to `results/garage_building_intersections.csv`.

*(The script deletes and recreates `results/` and `HW04.gdb` on each run.)*

---

## How to Run

1. Ensure inputs are in `Lab04/data/`:
   - `garages.csv` with columns **X, Y, Name**
   - `Campus.gdb` containing **Structures**

2. Run with ArcGIS Pro’s Python:
   OR
   Open the script in an IDE, such as Visual Studio Code:
   "C:/Program Files/ArcGIS/Pro/bin/Python/envs/arcgispro-py3/python.exe" HW04Code.py
 
3. When prompted, enter a buffer distance in meters (e.g., 100).
 
## Expected Output
**Lab04 folder** containing:
1. **HW04.gdb** containing:
   - **Garages** (points from CSV)  
   - **Structures** (copied from Campus.gdb)  
   - **Garages_proj** (projected garages)  
   - **GarageBuffers** (buffer polygons)  
   - **GarageBuilding_Intersect** (intersected features)  
2. **garage_building_intersections.csv** in the Lab04 folder with fields such as:
   - **Name** (garage name from CSV)  
   - **BldgAbbr, BldgName, Address** (if present in Structures)  
   - A unique ID (e.g., **OBJECTID**)  
3. **Campus.gdb**  & **garages.csv** - These were provided instead of created by the script.
 
---
 
## Notes
- **Coordinate systems**: The CSV is assumed to be WGS84 (lon/lat). The script projects garages to match *Structures* before buffering.  
- **Overwrite behavior**: Outputs are deleted/recreated automatically (`arcpy.env.overwriteOutput = True`).  
- **Validation**: Script checks that `garages.csv` exists, has `X` and `Y` fields, and that `Campus.gdb/Structures` exists. It also validates the buffer distance input.  
- **Outcome demo**: After export, the script uses a *SearchCursor* (iterator) and a *set* (container) to report the count of unique intersected buildings.
---
 
## Troubleshooting
- **“Missing CSV/FC” errors** → Check the paths at the top of the script.  
- **Empty outputs** → Buffer distance may be too small; confirm garages overlap with buildings.  
- **CSV header errors** → Ensure `garages.csv` has `X, Y, Name` columns.  
- **Unexpected field names** → *Structures* may use different attributes; adjust the exported fields if necessary.  
 
---
 
## Screenshot of Script Execution
![HW04 Screenshot #1](https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/blob/68bc56fe6076a0af214719b0f2cf5d4aafbb4cf9/Lab04/Images/Bricken_GEOG676_HW4.png)
![HW04 Screenshot #2](https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/blob/68bc56fe6076a0af214719b0f2cf5d4aafbb4cf9/Lab04/Images/Bricken_GEOG676_HW4_2.png)
![HW04 Screenshot #3](https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/blob/68bc56fe6076a0af214719b0f2cf5d4aafbb4cf9/Lab04/Images/Bricken_GEOG676_HW4_3.png)
![HW04 Screenshot #4](https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/blob/68bc56fe6076a0af214719b0f2cf5d4aafbb4cf9/Lab04/Images/Bricken_GEOG676_HW4_4.png)
![HW04 Screenshot #5](https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/blob/68bc56fe6076a0af214719b0f2cf5d4aafbb4cf9/Lab04/Images/Bricken_GEOG676_HW4_5.png)
![HW04 Screenshot #6](https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/blob/68bc56fe6076a0af214719b0f2cf5d4aafbb4cf9/Lab04/Images/Bricken_GEOG676_HW4_6.png)





 
---
 
## Submission Checklist
- Python script (**HW04Code.py**)  
- **README.md** with operations descriptions  
- Screenshots of script execution  
**Found in the Data Folder** **
- Geodatabase (**Campus.gdb**) - Provided by course instructor
- **Garages.csv** - CSV provided by course instructor
**Found in the Results Folder**
- Geodatabase (**HW04.gdb**) with outputs  
- Exported CSV (**GarageBuilding_Intersections.csv**)  
 
 
