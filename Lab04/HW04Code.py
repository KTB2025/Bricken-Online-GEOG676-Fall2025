import arcpy
import os

# ----------------------------
# Workspace & paths
# ----------------------------
# Define the folder where input files and outputs will live
folder_path = r"C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025\Lab04"

# Name and path for the project geodatabase
gdb_name = "HW04.gdb"
gdb_path = os.path.join(folder_path, gdb_name)

# Set ArcPy environment
arcpy.env.workspace = folder_path           # workspace can stay as the folder
arcpy.env.overwriteOutput = True            # automatically overwrite old outputs

# Create the geodatabase if it doesn’t already exist
if not arcpy.Exists(gdb_path):
    arcpy.management.CreateFileGDB(folder_path, gdb_name)
    print(f"Geodatabase created at: {gdb_path}")
else:
    print(f"Geodatabase already exists at: {gdb_path}")


# ----------------------------
# Inputs
# ----------------------------
# Path to the CSV of garage coordinates (must contain X and Y columns)
csv_path = os.path.join(folder_path, "garages.csv")
x_field = "X"   # column in CSV for longitude/easting
y_field = "Y"   # column in CSV for latitude/northing

# Path to Structures feature class (should exist inside your geodatabase)
structures_path = os.path.join(gdb_path, "Structures")
if not arcpy.Exists(structures_path):
    raise FileNotFoundError(f"Structures feature class not found: {structures_path}")


# ----------------------------
# Create point feature class from CSV
# ----------------------------
# Define WGS84 coordinate system (EPSG:4326) for the input XY coordinates
sr_wgs84 = arcpy.SpatialReference(4326)

# Path for output point feature class
garages_fc = os.path.join(gdb_path, "Garages")

# Clean up old version if it exists
if arcpy.Exists(garages_fc):
    arcpy.management.Delete(garages_fc)

# Convert CSV table to a point feature class using the XY fields
arcpy.management.XYTableToPoint(
    in_table=csv_path,
    out_feature_class=garages_fc,
    x_field=x_field,
    y_field=y_field,
    coordinate_system=sr_wgs84
)
print(f"Point feature class created: {garages_fc}")


# ----------------------------
# Project garages to match Structures spatial reference
# ----------------------------
# Get the spatial reference of the Structures feature class
struct_sr = arcpy.Describe(structures_path).spatialReference

# Define new path for projected garages
garages_proj = os.path.join(gdb_path, "Garages_proj")

# Delete old projected layer if it exists
if arcpy.Exists(garages_proj):
    arcpy.management.Delete(garages_proj)

# Project garages into the same coordinate system as Structures
arcpy.management.Project(garages_fc, garages_proj, struct_sr)
print(f"Projected garages to: {garages_proj} (SR: {struct_sr.name})")


# ----------------------------
# Buffer garages
# ----------------------------
buffer_output = os.path.join(gdb_path, "Garage_Buffer")

# Delete old buffer if it exists
if arcpy.Exists(buffer_output):
    arcpy.management.Delete(buffer_output)

# Prompt user for buffer distance in meters
raw = input("Enter the buffer distance in meters (e.g., 100): ").strip()
try:
    buffer_m = abs(float(raw))  # ensure positive float
except Exception as e:
    raise ValueError(f"Buffer distance must be a number (meters). Got '{raw}'.") from e

# Run buffer tool (ArcGIS will handle meters → dataset units if needed)
arcpy.analysis.Buffer(garages_proj, buffer_output, f"{buffer_m} Meters")
print(f"Buffer created: {buffer_output}")


# ----------------------------
# Intersect garage buffers with Structures
# ----------------------------
intersection_output = os.path.join(gdb_path, "Garage_Structures_Intersection")

# Delete old intersection if it exists
if arcpy.Exists(intersection_output):
    arcpy.management.Delete(intersection_output)

# Perform intersection between buffers and Structures
arcpy.analysis.Intersect([buffer_output, structures_path], intersection_output)
print(f"Intersection created: {intersection_output}")


# ----------------------------
# Export results to CSV
# ----------------------------
# Define CSV path in the working folder
intersection_csv = os.path.join(folder_path, "Garage_Structures_Intersection.csv")

# Delete old CSV if it exists (ArcPy fails if file already exists)
if arcpy.Exists(intersection_csv):
    os.remove(intersection_csv)

# Export intersection attribute table to CSV
arcpy.conversion.TableToTable(intersection_output, folder_path, "Garage_Structures_Intersection.csv")
print(f"Intersection table exported to: {intersection_csv}")