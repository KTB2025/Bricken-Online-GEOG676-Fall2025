# =============================================
# TAMU GIS Programming: Homework 04 - Fun with arcpy
# Author: Kate Bricken
# Date: 08/31/2025
# =============================================

import arcpy
import csv
import os
import sys

# ----------------------------
# 0) Inputs & environment
# ----------------------------
workspace = r"C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025\Lab04"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

csv_file = os.path.join(workspace, "garages.csv")                      # X,Y,Name
structures_path = os.path.join(workspace, "Campus.gdb", "Structures")  # Buildings FC
output_gdb = os.path.join(workspace, "HW04.gdb")

# ----------------------------
# 1) Buffer distance (meters)
# ----------------------------
if len(sys.argv) >= 2:
    raw = sys.argv[1]
else:
    raw = input("Enter buffer distance in meters (e.g., 100): ").strip()

try:
    buffer_meters_val = abs(float(raw))
except Exception:
    raise ValueError(f"Buffer distance must be numeric (got: {raw})")

buffer_distance_str = f"{buffer_meters_val} Meters"

# ----------------------------
# 2) Preconditions
# ----------------------------
if not os.path.exists(csv_file):
    raise FileNotFoundError(f"Missing CSV: {csv_file}")
if not arcpy.Exists(structures_path):
    raise FileNotFoundError(f"Missing Structures FC: {structures_path}")

if not arcpy.Exists(output_gdb):
    arcpy.management.CreateFileGDB(workspace, "HW04.gdb")

# ----------------------------
# 3) CSV -> point FC (WGS84)
# ----------------------------
garage_fc = os.path.join(output_gdb, "Garages")
if arcpy.Exists(garage_fc):
    arcpy.management.Delete(garage_fc)

sr_wgs84 = arcpy.SpatialReference(4326)  # CSV is assumed lon/lat WGS84

# Create empty point FC and add name
arcpy.management.CreateFeatureclass(output_gdb, "Garages", "POINT", spatial_reference=sr_wgs84)
arcpy.management.AddField(garage_fc, "Name", "TEXT", field_length=100)

# Insert points from CSV
with open(csv_file, "r", newline="") as f:
    reader = csv.DictReader(f)
    required = {"X", "Y", "Name"}
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
# 4) Copy Structures to GDB
# ----------------------------
structures_copy = os.path.join(output_gdb, "Structures")
if not arcpy.Exists(structures_copy):
    arcpy.management.CopyFeatures(structures_path, structures_copy)
    print("✓ Copied Structures into HW04.gdb")
else:
    print("• Structures already present in HW04.gdb")

# ----------------------------
# 5) Project garages to match Structures
# ----------------------------
sr_struct = arcpy.Describe(structures_copy).spatialReference
garages_proj = os.path.join(output_gdb, "Garages_proj")
if arcpy.Exists(garages_proj):
    arcpy.management.Delete(garages_proj)

arcpy.management.Project(garage_fc, garages_proj, sr_struct)
print(f"✓ Projected garages to {sr_struct.name}")

# ----------------------------
# 6) Buffer (planar, in meters string OK)
# ----------------------------
buffer_fc = os.path.join(output_gdb, "GarageBuffers")
if arcpy.Exists(buffer_fc):
    arcpy.management.Delete(buffer_fc)

# Note: Providing "XX Meters" converts units as needed even if dataset units differ
arcpy.analysis.Buffer(garages_proj, buffer_fc, buffer_distance_str, dissolve_option="NONE")
print(f"✓ Buffered garages at {buffer_distance_str}")

# ----------------------------
# 7) Intersect buffers with Structures
# ----------------------------
intersect_fc = os.path.join(output_gdb, "GarageBuilding_Intersect")
if arcpy.Exists(intersect_fc):
    arcpy.management.Delete(intersect_fc)

arcpy.analysis.Intersect([buffer_fc, structures_copy], intersect_fc, output_type="INPUT")
print("✓ Intersected buffers with Structures")

# ----------------------------
# 8) Inspect fields & export CSV
# ----------------------------
all_fields = {f.name for f in arcpy.ListFields(intersect_fc)}
print("Available fields in intersect output:")
for nm in sorted(all_fields):
    print(" -", nm)

# Prefer these if available:
preferred = ["Name", "BldgAbbr", "BldgName", "Address"]

# Build an export list from available fields (keep order from preferred, then add a stable id)
fields_to_export = [f for f in preferred if f in all_fields]

# Add a stable ID last for traceability
for candidate in ("OBJECTID", "FID", "OID@", "OID"):
    if candidate in all_fields:
        fields_to_export.append(candidate)
        break

if not fields_to_export:
    # Fallback: at least give OBJECTID
    fields_to_export = ["OBJECTID"]

output_csv = os.path.join(workspace, "garage_building_intersections.csv")
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(fields_to_export)
    with arcpy.da.SearchCursor(intersect_fc, fields_to_export) as cur:
        for row in cur:
            writer.writerow(row)

print(f"Done! CSV exported to: {output_csv}")
