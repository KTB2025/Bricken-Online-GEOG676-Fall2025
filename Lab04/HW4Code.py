# =============================================
# TAMU GIS Programming: Homework 04 - Fun with arcpy
# Author: Kate Bricken
# Date: 08/31/2025
# =============================================

import arcpy     # ArcPy module for geoprocessing
import csv       # For reading/writing CSV files
import os        # For path manipulation
import sys       # To accept command-line arguments

# --------------------------------------------------------
# Get Buffer Distance from Command Line Arguments
# --------------------------------------------------------
# Usage example: python HW4Code.py 100
# Accepts 1 argument: buffer distance in meters (e.g., "100")
# This avoids using input() and supports automation via CLI

if len(sys.argv) < 2:
    print("Usage: python HW4Code.py <buffer_distance_in_meters>")
    sys.exit(1)

buffer_meters = sys.argv[1]
buffer_distance = f"{buffer_meters} Meters"

# --------------------------------------------------------
# Set Up Workspace, Paths, and Environment
# --------------------------------------------------------

workspace = r"C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025\Lab04"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True  # Allow overwriting of existing outputs

# Input files
csv_file = os.path.join(workspace, "garages.csv")                     # CSV with X/Y garage locations
structures_path = os.path.join(workspace, "Campus.gdb", "Structures") # Input building layer

# Output geodatabase
output_gdb = os.path.join(workspace, "HW04.gdb")

# --------------------------------------------------------
# Step 1: Create Output Geodatabase (if it doesn't exist)
# --------------------------------------------------------

if not arcpy.Exists(output_gdb):
    arcpy.CreateFileGDB_management(workspace, "HW04.gdb")

# --------------------------------------------------------
# Step 2: Create Point Feature Class from CSV Coordinates
# --------------------------------------------------------

garage_fc = os.path.join(output_gdb, "Garages")
spatial_ref = arcpy.SpatialReference(4326)  # WGS 1984 - matches CSV coordinate system

# Delete old layer if it exists
if arcpy.Exists(garage_fc):
    arcpy.Delete_management(garage_fc)

# Create empty point feature class
arcpy.CreateFeatureclass_management(output_gdb, "Garages", "POINT", spatial_reference=spatial_ref)
arcpy.AddField_management(garage_fc, "Name", "TEXT")  # Add a text field for garage names

# Read CSV and insert points
with open(csv_file, "r") as f:
    reader = csv.DictReader(f)
    with arcpy.da.InsertCursor(garage_fc, ["SHAPE@XY", "Name"]) as cursor:
        for row in reader:
            x = float(row["X"])
            y = float(row["Y"])
            name = row["Name"]
            cursor.insertRow(((x, y), name))

# --------------------------------------------------------
# Step 3: Copy Structures Layer to Output GDB
# --------------------------------------------------------

structures_copy = os.path.join(output_gdb, "Structures")
if not arcpy.Exists(structures_copy):
    arcpy.CopyFeatures_management(structures_path, structures_copy)

# --------------------------------------------------------
# Step 4: Buffer Garage Points
# --------------------------------------------------------

buffer_fc = os.path.join(output_gdb, "GarageBuffers")

# Delete buffer layer if it already exists
if arcpy.Exists(buffer_fc):
    arcpy.Delete_management(buffer_fc)

# Create buffer around each garage point
arcpy.Buffer_analysis(garage_fc, buffer_fc, buffer_distance)

# --------------------------------------------------------
# Step 5: Intersect Buffers with Structures Layer
# --------------------------------------------------------

intersect_fc = os.path.join(output_gdb, "GarageBuilding_Intersect")

# Delete old intersection if it exists
if arcpy.Exists(intersect_fc):
    arcpy.Delete_management(intersect_fc)

# Perform spatial intersection
arcpy.Intersect_analysis([buffer_fc, structures_copy], intersect_fc)

# --------------------------------------------------------
# Step 6: Inspect Field Names in Intersect Output
# --------------------------------------------------------

print("Available fields in intersect output:")
field_names = [f.name for f in arcpy.ListFields(intersect_fc)]
for name in field_names:
    print("-", name)

# --------------------------------------------------------
# Step 7: Export Selected Fields to CSV
# --------------------------------------------------------

output_csv = os.path.join(workspace, "garage_building_intersections.csv")

# Select fields of interest for export
fields_to_export = ["Name", "FID_Structures", "BldgAbbr", "BldgName", "Address"]

# Write CSV
with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(fields_to_export)  # Write header
    with arcpy.da.SearchCursor(intersect_fc, fields_to_export) as cursor:
        for row in cursor:
            writer.writerow(row)

print("✅ Done! CSV exported to:", output_csv)