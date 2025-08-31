# TAMU GIS Programming: Homework 04 - Fun with arcpy
# Author: Kate Bricken
# Date: 08/31/2025

import arcpy
import os
import csv

# -------------------------------
# Set workspace and input paths
# -------------------------------

workspace = r"C:\Users\Kate\Documents\GIS\Homework04"
arcpy.env.workspace = workspace
arcpy.env.overwriteOutput = True

garage_csv = os.path.join(workspace, "garages.csv")
campus_gdb = os.path.join(workspace, "Campus.gdb")
structures_fc_name = "Structures"
structures_fc = os.path.join(campus_gdb, structures_fc_name)

# Output GDB path
output_gdb = os.path.join(workspace, "Homework04.gdb")
if not arcpy.Exists(output_gdb):
    arcpy.CreateFileGDB_management(workspace, "Homework04.gdb")

# -------------------------------
# Step 1: Convert CSV to Point Feature Class
# -------------------------------

garage_points_fc = os.path.join(output_gdb, "Garages")
spatial_ref = arcpy.SpatialReference(3857)  # Or use 4326 if needed

arcpy.management.XYTableToPoint(
    in_table=garage_csv,
    out_feature_class=garage_points_fc,
    x_field="X",
    y_field="Y",
    coordinate_system=spatial_ref
)

# -------------------------------
# Step 2: Copy Structures layer to your GDB
# -------------------------------

structures_copy = os.path.join(output_gdb, "Structures")
arcpy.CopyFeatures_management(structures_fc, structures_copy)

# -------------------------------
# Step 3: Buffer the garages
# -------------------------------

buffer_distance = input("Enter buffer distance in meters: ")
garage_buffer_fc = os.path.join(output_gdb, "GarageBuffers")

arcpy.analysis.Buffer(
    in_features=garage_points_fc,
    out_feature_class=garage_buffer_fc,
    buffer_distance_or_field=f"{buffer_distance} Meters",
    dissolve_option="ALL"
)

# -------------------------------
# Step 4: Intersect buffered garages with buildings
# -------------------------------

intersect_fc = os.path.join(output_gdb, "GarageBuilding_Intersect")
arcpy.analysis.Intersect(
    in_features=[[garage_buffer_fc, ""], [structures_copy, ""]],
    out_feature_class=intersect_fc,
    join_attributes="ALL"
)

# -------------------------------
# Step 5: Inspect available fields in Structures
# -------------------------------

print("\nAvailable fields in the Structures layer:")
structure_fields = arcpy.ListFields(structures_copy)
for field in structure_fields:
    print(f"- {field.name} ({field.type})")

# -------------------------------
# Step 6: Export selected fields to CSV
# -------------------------------

# Output CSV path
output_csv = os.path.join(workspace, "garage_building_intersections.csv")

# Define fields to export
# These must exist in BOTH garages and structures layers
fields = ["FAC_CODE", "Name", "StructureID", "StructureName"]
available_fields = [f.name for f in arcpy.ListFields(intersect_fc)]
export_fields = [f for f in fields if f in available_fields]

# Write to CSV
with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(export_fields)

    with arcpy.da.SearchCursor(intersect_fc, export_fields) as cursor:
        for row in cursor:
            writer.writerow(row)

print(f"\n✅ Done! CSV exported to: {output_csv}")
