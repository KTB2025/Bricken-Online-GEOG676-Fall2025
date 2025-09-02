# =============================================
# TAMU GIS Programming: Homework 04 - Fun with arcpy
# Author: Kate Bricken
# Date: 09/02/2025
# =============================================

import arcpy
import os
import csv

# ----------------------------
# Setup: paths & environment
# ----------------------------
workspace = r"C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025\Lab04"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True  # overwrite old outputs safely

csv_file        = os.path.join(workspace, "garages.csv")             # garage coords (X, Y, Name)
structures_src  = os.path.join(workspace, "Campus.gdb", "Structures")# provided buildings layer
out_gdb         = os.path.join(workspace, "HW04.gdb")                # output GDB for this HW
out_csv         = os.path.join(workspace, "garage_building_intersections.csv")

# ----------------------------
# Preconditions / validation
# ----------------------------
# Ensure required input files exist
if not os.path.exists(csv_file):
    raise FileNotFoundError(f"Missing CSV: {csv_file}")
if not arcpy.Exists(structures_src):
    raise FileNotFoundError(f"Missing Structures feature class: {structures_src}")

# Validate CSV headers contain X and Y fields
with open(csv_file, "r", newline="") as f:
    reader = csv.reader(f)
    headers = next(reader, None)
    if headers is None:
        raise ValueError("CSV file is empty.")
    if not {"X", "Y"}.issubset(set(headers)):
        raise ValueError(f"CSV must contain 'X' and 'Y'. Found: {headers}")

# ----------------------------
# 1) Get buffer distance (meters)
# ----------------------------
# Prompt user and validate numeric input
while True:
    raw = input("Enter buffer distance in meters (e.g., 100): ").strip()
    try:
        buf_m = abs(float(raw))
        break
    except ValueError:
        print(f"Please enter a number (you typed: {raw!r}).")
buf_str = f"{buf_m} Meters"
print(f"✓ Buffer distance set to: {buf_str}")

# ----------------------------
# 2) Create output GDB
# ----------------------------
# Store all results in HW04.gdb for consistency
if not arcpy.Exists(out_gdb):
    arcpy.management.CreateFileGDB(workspace, "HW04.gdb")
    print(f"✓ Created geodatabase: {out_gdb}")
else:
    print(f"• Using existing geodatabase: {out_gdb}")

# ----------------------------
# 3) CSV -> point feature class
# ----------------------------
sr_wgs84 = arcpy.SpatialReference(4326)  # WGS84 (matches lon/lat input)
garages = os.path.join(out_gdb, "Garages")
if arcpy.Exists(garages):
    arcpy.management.Delete(garages)

# Create point features directly from CSV
arcpy.management.XYTableToPoint(
    in_table=csv_file,
    out_feature_class=garages,
    x_field="X",
    y_field="Y",
    coordinate_system=sr_wgs84
)
print(f"✓ Created garage points (WGS84): {garages}")

# Copy Structures into HW04.gdb for local use
structures = os.path.join(out_gdb, "Structures")
if not arcpy.Exists(structures):
    arcpy.management.CopyFeatures(structures_src, structures)
    print(f"✓ Copied Structures into HW04.gdb: {structures}")
else:
    print("• Structures already present in HW04.gdb")

# ----------------------------
# 4) Project garages
# ----------------------------
# Reproject garages to match Structures (so buffer units = meters)
sr_struct = arcpy.Describe(structures).spatialReference
print(f"• Structures spatial reference: {sr_struct.name}")

garages_proj = os.path.join(out_gdb, "Garages_proj")
if arcpy.Exists(garages_proj):
    arcpy.management.Delete(garages_proj)
arcpy.management.Project(garages, garages_proj, sr_struct)
print(f"✓ Projected garages to: {sr_struct.name}")

# ----------------------------
# 5) Buffer garages
# ----------------------------
buffers = os.path.join(out_gdb, "GarageBuffers")
if arcpy.Exists(buffers):
    arcpy.management.Delete(buffers)
arcpy.analysis.Buffer(garages_proj, buffers, buf_str, dissolve_option="NONE")
print(f"✓ Buffered garages at {buf_str}")

# ----------------------------
# 6) Intersect buffers + Structures
# ----------------------------
intersect_fc = os.path.join(out_gdb, "GarageBuilding_Intersect")
if arcpy.Exists(intersect_fc):
    arcpy.management.Delete(intersect_fc)
arcpy.analysis.Intersect([buffers, structures], intersect_fc)
print(f"✓ Intersected buffers with Structures → {intersect_fc}")

# ----------------------------
# 7) Export intersection table
# ----------------------------
if arcpy.Exists(out_csv):
    os.remove(out_csv)
arcpy.conversion.ExportTable(intersect_fc, out_csv)
print("✓ Exported intersect attribute table to CSV")
print("Done!")
print(f" - GDB: {out_gdb}")
print(f" - Intersect table: {intersect_fc}")
print(f" - CSV: {out_csv}")
