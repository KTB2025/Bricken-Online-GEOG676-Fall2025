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
 
