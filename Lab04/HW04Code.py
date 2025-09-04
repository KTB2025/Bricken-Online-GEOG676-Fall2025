# TAMU GIS Programming: Homework 04 - Fun With Arcpy
# Author: Kate Bricken
# Date: 09/04/2025

import arcpy
 
# ----------------------------
# Input and output workspaces
# ----------------------------
input_workspace  = r"C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025\Lab04\data"   # raw data
output_workspace = r"C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025\Lab04\results" # outputs
 
arcpy.env.overwriteOutput = True  # auto-overwrite outputs
 
# ----------------------------
# Reset the results folder
# ----------------------------
if arcpy.Exists(output_workspace):
    print(f"Deleting old results folder: {output_workspace}")
    arcpy.management.Delete(output_workspace)
 
arcpy.management.CreateFolder(
    out_folder_path=r"C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025",
    out_name="Lab04\\results"
)

print(f"Created clean results folder: {output_workspace}")
 
# ----------------------------
# Inputs in the data workspace
# ----------------------------
csv_file       = fr"{input_workspace}\garages.csv"
structures_src = fr"{input_workspace}\Campus.gdb\Structures"
 
# ----------------------------
# Create output gdb and make sure it is empty 
# ----------------------------
out_gdb = fr"{output_workspace}\HW04.gdb"
out_csv = fr"{output_workspace}\garage_building_intersections.csv"

arcpy.management.CreateFileGDB(output_workspace, "HW04.gdb")
print(f"Created fresh geodatabase: {out_gdb}")

# ----------------------------
# Get buffer distance (meters)
# ----------------------------
 
while True:
 
    raw = input("Enter buffer distance in meters (e.g., 100): ").strip()
 
    try:
 
        buffer_m = abs(float(raw))
 
        break
 
    except ValueError:
 
        print(f"Please enter a number (you typed: {raw!r}).")
 
buffer_str = f"{buffer_m} Meters"
 
print(f"Buffer distance set to: {buffer_str}")
 
 
# ----------------------------
# CSV -> point feature class
# ----------------------------
sr_wgs84 = arcpy.SpatialReference(4326)
garages = fr"{out_gdb}\Garages"
 
if arcpy.Exists(garages):
 
    arcpy.management.Delete(garages)
 
arcpy.management.XYTableToPoint(
 
    in_table=csv_file,
 
    out_feature_class=garages,
 
    x_field="X",
 
    y_field="Y",
 
    coordinate_system=sr_wgs84
 
)
 
print(f"Created garage points (WGS84): {garages}")
 
# ----------------------------
# Copy Structures
# ----------------------------
structures = fr"{out_gdb}\Structures"
if not arcpy.Exists(structures):
 
    arcpy.management.CopyFeatures(structures_src, structures)
 
    print(f"Copied Structures into HW04.gdb: {structures}")
 
else:
 
    print("Structures already present in HW04.gdb")
 
# ----------------------------
# Project garages
# ----------------------------
sr_struct = arcpy.Describe(structures).spatialReference
garages_proj = fr"{out_gdb}\Garages_proj"
 
if arcpy.Exists(garages_proj):
 
    arcpy.management.Delete(garages_proj)
 
arcpy.management.Project(garages, garages_proj, sr_struct)
 
print(f"Projected garages to: {sr_struct.name}")
 
# ----------------------------
# Buffer garages to the input distance
# ----------------------------
buffers = fr"{out_gdb}\GarageBuffers"
 
if arcpy.Exists(buffers):
 
    arcpy.management.Delete(buffers)
 
arcpy.analysis.Buffer(garages_proj, buffers, buffer_str, dissolve_option="NONE")
 
print(f"Buffered garages at {buffer_str}")
 
# ----------------------------
# Intersect buffers + structures to create an intersection feature class
# ----------------------------
intersect_fc = fr"{out_gdb}\GarageBuilding_Intersect"
 
if arcpy.Exists(intersect_fc):
 
    arcpy.management.Delete(intersect_fc)
 
arcpy.analysis.Intersect([buffers, structures], intersect_fc)
 
print(f"Intersected buffers with Structures → {intersect_fc}")
# ----------------------------
# Export the intersect feature class attribute table to the results geodatabase and print the output location and type
# ----------------------------
arcpy.conversion.ExportTable(intersect_fc, out_csv)
 
print("Exported the intersect feature class attribute table to a CSV")
 
print("Done!")
 
print(f" - GDB: {out_gdb}")
 
print(f" - Intersect table: {intersect_fc}")
 
print(f" - CSV: {out_csv}")
 