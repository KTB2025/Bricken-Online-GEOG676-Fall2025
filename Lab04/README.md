# TAMU GIS Programming: Homework 04 — Fun with ArcPy

**Author:** Kate Bricken  
**Course:** GEOG 676 — GIS Programming  
**Assignment Due Date:** September 22, 2025  

---

## Overview

This script uses **ArcPy** to determine which TAMU campus buildings intersect with user-defined buffer zones around parking garages. It:

1. Builds a point feature class from a CSV of garage coordinates  
2. Projects garages to match the **Structures** layer  
3. Creates buffers in meters  
4. Intersects those buffers with **Structures**  
5. Exports a clean results table as a CSV  

---

## How it Works

1. **CSV → Points (WGS 84)**  
   Reads `garages.csv` (required columns: `X`, `Y`, `Name`) and creates a `Garages` feature class in `HW04.gdb` (WGS84, EPSG:4326).

2. **Copy Structures**  
   Copies `Campus.gdb/Structures` into `HW04.gdb` so all processing happens in one geodatabase.

3. **Project Garages**  
   Projects `Garages` into the same coordinate system as `Structures` → `Garages_proj` (ensures buffer units are correct).

4. **Buffer**  
   Buffers `Garages_proj` → `GarageBuffers` using the user-provided distance in meters.

5. **Intersect**  
   Intersects `GarageBuffers` with `Structures` → `GarageBuilding_Intersect`.

6. **Export CSV**  
   Exports the attribute table from `GarageBuilding_Intersect` to `garage_building_intersections.csv`.

---

## How to Run

1. Place the script in your `Lab04` folder alongside:
   - `garages.csv` (with columns `X`, `Y`, `Name`)
   - `Campus.gdb` (with the `Structures` feature class)

2. Open the script in an IDE, such as Visual Code Studio:
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

---

## Troubleshooting
- **“Missing CSV/FC” errors** → Check the paths at the top of the script.  
- **Empty outputs** → Buffer distance may be too small; confirm garages overlap with buildings.  
- **CSV header errors** → Ensure `garages.csv` has `X, Y, Name` columns.  
- **Unexpected field names** → *Structures* may use different attributes; adjust the exported fields if necessary.  

---

## Screenshot of Script Execution
*(Insert screenshot of console showing successful run.)*

---

## Submission Checklist
- Python script (**HW04Code.py**)  
- Geodatabase (**HW04.gdb**) with outputs  
- Geodatabase (**Campus.gdb**) - Provided by course instructor
- **Garages.csv** - CSV provided by course instructor
- Exported CSV (**garage_building_intersections.csv**)  
- Screenshots of script execution  
- **README.md** with operations descriptions  
