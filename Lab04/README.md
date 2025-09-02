# TAMU GIS Programming: Homework 04 — Fun with ArcPy

**Author:** Kate Bricken  
**Course:** GEOG 676 — GIS Programming  
**Assignment Due Date:** September 22, 2025  


---

## Overview

This script uses **ArcPy** to find which campus buildings fall within a user-defined buffer distance of each TAMU parking garage. It:
1) builds a point feature class from a CSV of garage coordinates,  
2) projects those points to match the **Structures** layer,  
3) creates buffers,  
4) intersects the buffers with **Structures**, and  
5) exports a tidy CSV of results.

---

## How it Works

1. **CSV → Points (WGS 84)**  
   Reads `garages.csv` (required columns: `X`, `Y`, `Name`) and creates a `Garages` point feature class in `HW04.gdb` (SRID 4326).

2. **Copy Structures**  
   Copies `Campus.gdb/Structures` into `HW04.gdb` to ensure all processing occurs in the working geodatabase.

3. **Project Garages**  
   Projects `Garages` to the **exact spatial reference** of `Structures` → `Garages_proj`. This ensures buffers in meters are correct.

4. **Buffer**  
   Buffers `Garages_proj` to `GarageBuffers` using the user-provided distance (e.g., `"100 Meters"`). Planar buffer is used.

5. **Intersect**  
   Intersects `GarageBuffers` with `Structures` → `GarageBuilding_Intersect`.

6. **Export CSV**  
   Exports a results table to `garage_building_intersections.csv`. It will include whichever of these fields are present:
   - `Name` (garage name from CSV)  
   - `BldgAbbr`, `BldgName`, `Address` (from Structures)  
   - plus a stable identifier (e.g., `OBJECTID`) for traceability.  
   The script also prints **all available fields** in the intersect output to the console.

---


## How to Run



## Expected Output 



---

## Notes

- **CRS & Units:** CSV coordinates are assumed **WGS 84 (lon/lat)**. The script **projects** garages to match **Structures** before buffering to keep **meter** buffers correct.
- **Field Flexibility:** The script does **not** assume shapefile-style fields like `FID_Structures`. It exports whichever of `Name`, `BldgAbbr`, `BldgName`, `Address` exist, plus a stable ID.
- **Overwrites:** `arcpy.env.overwriteOutput = True`. Existing outputs in `HW04.gdb` (e.g., `Garages`, `Garages_proj`, `GarageBuffers`, `GarageBuilding_Intersect`) are safely deleted/recreated.
- **Validation:** You’ll get clear errors if `garages.csv` is missing, `Structures` can’t be found, or the buffer distance isn’t numeric.

---

## Troubleshooting

- **“Missing CSV/FC” errors:** Check `workspace`, `csv_file`, and `structures_path` at the top of the script.
- **Empty output:** Verify your buffer isn’t too small, and that garage points and buildings overlap spatially after projection.
- **Field not found in CSV:** Ensure your CSV has exact headers `X`, `Y`, `Name`.
- **No `BldgAbbr/BldgName` in CSV output:** Your Structures layer may use different field names. The script prints all intersect fields—adjust the preferred list if needed.

---

## Screenshot of Script Execution

> *(Insert your console or ArcGIS Pro messages screenshot here.)*

---

## Submission Checklist

- Python script (`.py`)
- Geodatabase with outputs (`.gdb`)
- Exported CSV (`.csv`)
- Screenshots of executed script
- Updated `README.md`
