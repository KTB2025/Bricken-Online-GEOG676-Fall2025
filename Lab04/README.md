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

The workflow is designed to be **reproducible** and **robust** (safe overwrites, input validation, and flexible field export).

---

## What the Script Does (Step-by-Step)

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

## Project Structure

Lab04/
├─ garages.csv # Input CSV with X, Y, Name
├─ Campus.gdb/ # Provided geodatabase (source Structures)
├─ HW04.gdb/ # Created by script (outputs)
│ ├─ Garages # Points from CSV (WGS84)
│ ├─ Structures # Copy of Campus.gdb/Structures
│ ├─ Garages_proj # Garages reprojected to match Structures
│ ├─ GarageBuffers # Buffers around garage points
│ └─ GarageBuilding_Intersect # Intersect of buffers with Structures
├─ garage_building_intersections.csv # Final exported table
├─ HW4Code.py # This homework’s Python script
└─ README.md


---

## Requirements

- **ArcGIS Pro** (ArcPy environment)  
- Access to the provided **Campus.gdb** (with the `Structures` feature class)  
- A CSV named **`garages.csv`** with columns: `X`, `Y`, `Name` (lon/lat assumed in WGS 84)

---

## How to Run

**Option A — Prompted run (no args):**
1. Open the **ArcGIS Pro Python** environment (or run inside Pro).
2. Update the `workspace` path at the top of `HW4Code.py` if needed.
3. Run `HW4Code.py`.  
4. When prompted, enter a **buffer distance in meters** (e.g., `100`).

**Option B — Command line with argument:**
```bash
python HW4Code.py 150

This skips the prompt and uses 150 Meters.

## Expected Output (example)

Final CSV columns depend on what exists in your data, but typically include:

| Name | BldgAbbr | BldgName            | Address                       | OBJECTID |
|------|----------|---------------------|-------------------------------|----------|
| CCG  | ACAD     | Academic Building   | 389 Houston St, College…      | 1021     |
| NSG  | ENGLAB   | Engineering Lab     | 188 Bizzell St, College…      | 1044     |

> The script prints the full list of fields found in the intersect so you can confirm what’s available.

---

## Notes & Best Practices

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
