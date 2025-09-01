# =============================================
# TAMU GIS Programming: Homework 04 - Fun with arcpy
# Author: Kate Bricken
# Date: 08/31/2025
# =============================================
"""
Pipeline:
1) Read garage XY + Name from CSV (assumed WGS84 lon/lat)
2) Create a file GDB (if missing)
3) Make a point feature class from the CSV
4) Copy Structures into the same GDB
5) Project garage points to the Structures' CRS (so meter buffers are correct)
6) Buffer the projected garages by a user-specified distance (meters)
7) Intersect buffers with Structures
8) Export a tidy CSV of chosen fields (falling back gracefully)
"""

import arcpy
import csv
import os
import sys

# ----------------------------
# Inputs & environment
# ----------------------------
workspace = r"C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025\Lab04"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True  # allow re-runs without manual cleanup

csv_file = os.path.join(workspace, "garages.csv")                      # expects columns: X, Y, Name
structures_path = os.path.join(workspace, "Campus.gdb", "Structures")  # buildings feature class
output_gdb = os.path.join(workspace, "HW04.gdb")

# ----------------------------
# Buffer distance (meters)
# ----------------------------
# ----------------------------
# Buffer distance (meters)
# ----------------------------
import argparse

parser = argparse.ArgumentParser(description="HW4 buffer distance (meters)")
parser.add_argument("buffer", nargs="?", type=float, help="Buffer distance in meters")
args = parser.parse_args()

if args.buffer is not None:
    buffer_meters_val = abs(float(args.buffer))
else:
    while True:
        raw = input("Enter buffer distance in meters (e.g., 100): ").strip()
        try:
            buffer_meters_val = abs(float(raw))
            break
        except ValueError:
            print(f"Please enter a numeric value (you typed: {raw!r}).")

buffer_distance_str = f"{buffer_meters_val} Meters"


# ----------------------------
# Preconditions
# ----------------------------
# Fast fail with clear messages if required inputs are missing
if not os.path.exists(csv_file):
    raise FileNotFoundError(f"Missing CSV: {csv_file}")
if not arcpy.Exists(structures_path):
    raise FileNotFoundError(f"Missing Structures FC: {structures_path}")

# Create a clean output GDB on first run
if not arcpy.Exists(output_gdb):
    arcpy.management.CreateFileGDB(workspace, "HW04.gdb")

# ----------------------------
# CSV -> point FC (WGS84)
# ----------------------------
garage_fc = os.path.join(output_gdb, "Garages")
if arcpy.Exists(garage_fc):
    arcpy.management.Delete(garage_fc)  # ensure fresh build

sr_wgs84 = arcpy.SpatialReference(4326)  # EPSG:4326; matches CSV lon/lat assumption

# Make an empty point feature class and add a Name field
arcpy.management.CreateFeatureclass(output_gdb, "Garages", "POINT", spatial_reference=sr_wgs84)
arcpy.management.AddField(garage_fc, "Name", "TEXT", field_length=100)

# Load rows from CSV into the point FC
with open(csv_file, "r", newline="") as f:
    reader = csv.DictReader(f)
    required = {"X", "Y", "Name"}
    # Validate header early so failures are obvious to the grader
    if not required.issubset(set(reader.fieldnames or [])):
        raise ValueError(f"CSV must contain columns: {', '.join(required)}")
    with arcpy.da.InsertCursor(garage_fc, ["SHAPE@XY", "Name"]) as icur:
        for row in reader:
            x = float(row["X"])
            y = float(row["Y"])
            nm = row["Name"]
            icur.insertRow(((x, y), nm))

print("✓ Created garage points from CSV")

# ----------------------------
# Copy Structures to GDB
# ----------------------------
# Keep all working data in HW04.gdb for reproducibility/portability
structures_copy = os.path.join(output_gdb, "Structures")
if not arcpy.Exists(structures_copy):
    arcpy.management.CopyFeatures(structures_path, structures_copy)
    print("✓ Copied Structures into HW04.gdb")
else:
    print("• Structures already present in HW04.gdb")

# ----------------------------
# Project garages to match Structures
# ----------------------------
# Critical step: buffering in meters only makes sense in a projected CRS
sr_struct = arcpy.Describe(structures_copy).spatialReference
garages_proj = os.path.join(output_gdb, "Garages_proj")
if arcpy.Exists(garages_proj):
    arcpy.management.Delete(garages_proj)

arcpy.management.Project(garage_fc, garages_proj, sr_struct)
print(f"✓ Projected garages to {sr_struct.name}")

# ----------------------------
# Buffer (planar; meters)
# ----------------------------
buffer_fc = os.path.join(output_gdb, "GarageBuffers")
if arcpy.Exists(buffer_fc):
    arcpy.management.Delete(buffer_fc)

# Planar buffer in target CRS; arcpy will interpret "NNN Meters" correctly
arcpy.analysis.Buffer(garages_proj, buffer_fc, buffer_distance_str, dissolve_option="NONE")
print(f"✓ Buffered garages at {buffer_distance_str}")

# ----------------------------
# Intersect buffers with Structures
# ----------------------------
# Intersect returns segments of Structures that fall within each buffer
intersect_fc = os.path.join(output_gdb, "GarageBuilding_Intersect")
if arcpy.Exists(intersect_fc):
    arcpy.management.Delete(intersect_fc)

arcpy.analysis.Intersect([buffer_fc, structures_copy], intersect_fc, output_type="INPUT")
print("✓ Intersected buffers with Structures")

# ----------------------------
# Inspect fields & export CSV
# ----------------------------
# Show user what came out of the intersect (useful for grading/debugging)
all_fields = {f.name for f in arcpy.ListFields(intersect_fc)}
print("Available fields in intersect output:")
for nm in sorted(all_fields):
    print(" -", nm)

# Prefer consistent, human-friendly attributes when available
preferred = ["Name", "BldgAbbr", "BldgName", "Address"]

# Keep preferred fields that actually exist, then append a stable ID for traceability
fields_to_export = [f for f in preferred if f in all_fields]
for candidate in ("OBJECTID", "FID", "OID@", "OID"):
    if candidate in all_fields:
        fields_to_export.append(candidate)
        break
if not fields_to_export:
    # Last resort—every FC should have some kind of object id
    fields_to_export = ["OBJECTID"]

# Write rows to a simple, portable CSV
output_csv = os.path.join(workspace, "garage_building_intersections.csv")
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(fields_to_export)  # header
    with arcpy.da.SearchCursor(intersect_fc, fields_to_export) as cur:
        for row in cur:
            writer.writerow(row)

print(f"Done! CSV exported to: {output_csv}")
