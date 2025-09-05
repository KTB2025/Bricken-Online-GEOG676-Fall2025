# =============================================
# TAMU GIS Programming: Homework 04 - Fun With Arcpy
# Author: Kate Bricken
# Date: 09/04/2025
# =============================================

import arcpy
 
# ----------------------------
# Input and output workspaces
# ----------------------------

folder_path = r"C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025\Lab04"  # parent folder for input and output data
input_workspace  = r"C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025\Lab04\data"   # raw data
output_workspace = r"C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025\Lab04\results" # outputs
 
arcpy.env.overwriteOutput = True  # auto overwrite outputs
 
# ----------------------------
# Reset the results folder for a clean workspace 
# ----------------------------

if arcpy.Exists(output_workspace):  # If results folder exists from the last script run then delete it
    print(f"Deleting old results folder: {output_workspace}")
    arcpy.management.Delete(output_workspace)

if not arcpy.Exists(output_workspace):  # If results folder does not exist then recreate it
    arcpy.management.CreateFolder(folder_path, "results")


if not arcpy.Exists(output_workspace): # if the folder creation failed, then raise an error 
    raise RuntimeError(f"Failed to create results folder: {output_workspace}")

print(f"Created clean results folder: {output_workspace}")


# ----------------------------
# Input files to the data workspace
# ----------------------------

csv_file       = fr"{input_workspace}\garages.csv"  # expects fields: X, Y, Name
structures_src = fr"{input_workspace}\Campus.gdb\Structures"   # buildings feature class

if not arcpy.Exists(csv_file):
    raise FileNotFoundError(f"Missing CSV: {csv_file}")
if not arcpy.Exists(structures_src):
    raise FileNotFoundError(f"Missing Structures: {structures_src}")

# ----------------------------
# Create output geodatabase and make sure it is clear
# ----------------------------

out_gdb = fr"{output_workspace}\HW04.gdb"
out_csv = fr"{output_workspace}\garage_building_intersections.csv"

# if a previous GDB is still there, remove just the GDB
if arcpy.Exists(out_gdb):
    arcpy.management.Delete(out_gdb)

arcpy.management.CreateFileGDB(output_workspace, "HW04.gdb")
print(f"Created clean & clear geodatabase: {out_gdb}")

# ----------------------------
# Get buffer distance (meters) from user input
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
# Convert garages CSV -> point feature class in WGS 84
# ----------------------------

sr_wgs84 = arcpy.SpatialReference(4326)  # WGS 84 (lon/lat), matches CSV assumption
garages = fr"{out_gdb}\Garages"
 
arcpy.management.XYTableToPoint(         
 
    in_table=csv_file,
 
    out_feature_class=garages,
 
    x_field="X",
 
    y_field="Y",
 
    coordinate_system=sr_wgs84
 
)
 
print(f"Created garage points in WGS84: {garages}")
 
# ----------------------------
# Copy Structures file into the output geodatabase, if it is not already present
# ----------------------------

structures = fr"{out_gdb}\Structures"
if not arcpy.Exists(structures):
 
    arcpy.management.CopyFeatures(structures_src, structures)
 
    print(f"Copied Structures file into HW04.gdb: {structures}")
 
else:
 
    print("Structures already present in HW04.gdb")
 
# ----------------------------
# Project garages to match Structures CRS
# ----------------------------

sr_struct = arcpy.Describe(structures).spatialReference   # target CRS = Structures layer CRS
garages_proj = fr"{out_gdb}\Garages_proj"
 
arcpy.management.Project(garages, garages_proj, sr_struct)
 
print(f"Projected garages to: {sr_struct.name}")
 
# ----------------------------
# Buffer garages to the distance in meters input from user
# ----------------------------

buffers = fr"{out_gdb}\GarageBuffers"
 
arcpy.analysis.Buffer(garages_proj, buffers, buffer_str, dissolve_option="NONE")
 
print(f"Buffered garages at {buffer_str}")
 
# ----------------------------
# Intersect buffers with Structures > buildings within buffer
# ----------------------------

intersect_fc = fr"{out_gdb}\GarageBuilding_Intersect"
 
arcpy.analysis.Intersect([buffers, structures], intersect_fc)
 
print(f"Intersected buffers with Structures -> {intersect_fc}")

# ----------------------------
# Export the intersect attribute table to the results geodatabase
# ----------------------------

arcpy.conversion.ExportTable(intersect_fc, out_csv)

# ----------------------------
#demonstrate an iterator and container as per the procedure task list using HW04 data to find unique building names
# ----------------------------

unique_buildings = set()  # container
with arcpy.da.SearchCursor(intersect_fc, ["Name", "BldgName"]) as rows:  # iterator
    for _, bname in rows:
        if bname:
            unique_buildings.add(bname)

print(f"Unique buildings intersected: {len(unique_buildings)}")

# ----------------------------
# Final locations summary
# ----------------------------

print("Exported the intersect feature class attribute table to a CSV")
 
print(f" - GDB: {out_gdb}")
 
print(f" - Intersect table: {intersect_fc}")
 
print(f" - CSV: {out_csv}")
 