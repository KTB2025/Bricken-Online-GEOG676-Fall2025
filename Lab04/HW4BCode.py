# =============================================
# TAMU GIS Programming: Homework 04 - Fun with arcpy
# Author: Kate Bricken
# Date: 08/31/2025
# =============================================

import arcpy
import os

# ----------------------------
# Paths / environment
# ----------------------------
workspace = r"C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025\Lab04"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

csv_file        = os.path.join(workspace, "garages.csv")                      # expects: X, Y, Name
structures_src  = os.path.join(workspace, "Campus.gdb", "Structures")         # given
out_gdb         = os.path.join(workspace, "HW04.gdb")                         # new / reused
out_csv         = os.path.join(workspace, "garage_building_intersections.csv")

# ----------------------------
# 1) Get buffer distance (meters)
# ----------------------------
while True:
    raw = input("Enter buffer distance in meters (e.g., 100): ").strip()
    try:
        buf_m = abs(float(raw))
        break
    except ValueError:
        print(f"Please enter a number (you typed: {raw!r}).")
buf_str = f"{buf_m} Meters"

# ----------------------------
# 2) Create GDB (if missing)
# ----------------------------
if not arcpy.Exists(out_gdb):
    arcpy.management.CreateFileGDB(workspace, "HW04.gdb")

# ----------------------------
# 3) CSV -> points (WGS84)
# ----------------------------
sr_wgs84 = arcpy.SpatialReference(4326)  # lon/lat
garages = os.path.join(out_gdb, "Garages")
if arcpy.Exists(garages):
    arcpy.management.Delete(garages)

# XYTableToPoint brings over the Name field automatically if present
arcpy.management.XYTableToPoint(
    in_table=csv_file,
    out_feature_class=garages,
    x_field="X",
    y_field="Y",
    coordinate_system=sr_wgs84
)
structures = os.path.join(out_gdb, "Structures")
arcpy.management.CopyFeatures(structures_src, structures); structures_src = structures

# ----------------------------
# 4) Project to match Structures
# ----------------------------
sr_struct = arcpy.Describe(structures_src).spatialReference
garages_proj = os.path.join(out_gdb, "Garages_proj")
if arcpy.Exists(garages_proj):
    arcpy.management.Delete(garages_proj)
arcpy.management.Project(garages, garages_proj, sr_struct)

# ----------------------------
# 5) Buffer (planar; meters)
# ----------------------------
buffers = os.path.join(out_gdb, "GarageBuffers")
if arcpy.Exists(buffers):
    arcpy.management.Delete(buffers)
arcpy.analysis.Buffer(garages_proj, buffers, buf_str, dissolve_option="NONE")

# ----------------------------
# 6) Intersect with Structures
# ----------------------------
intersect_fc = os.path.join(out_gdb, "GarageBuilding_Intersect")
if arcpy.Exists(intersect_fc):
    arcpy.management.Delete(intersect_fc)
arcpy.analysis.Intersect([buffers, structures_src], intersect_fc)

# ----------------------------
# 7) Export table to CSV
# ----------------------------
# Export *all* fields from the intersect result as a simple CSV (meets prompt)
if arcpy.Exists(out_csv):
    arcpy.management.Delete(out_csv)
arcpy.conversion.ExportTable(intersect_fc, out_csv)

print("Done!")
print(f" - GDB: {out_gdb}")
print(f" - Intersect table: {intersect_fc}")
print(f" - CSV: {out_csv}")
