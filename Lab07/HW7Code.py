# =============================================
# TAMU GIS Programming: Homework 07 - Raster Analysis
# Author: Kate Bricken
# Date: 09/08/2025
# =============================================

import arcpy
import os

# =============================================
# Landsat & Composite Bands
# =============================================

# Load four Landsat spectral bands (blue, green, red, NIR) as raster objects -> combine into a single multi spectral composite.
source = r"C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025-Lab07-Images\LT05_L1TP_025039_20111031_20200820_02_T1"
band1 = arcpy.sa.Raster(source + r"\LT05_L1TP_025039_20111031_20200820_02_T1_B1.TIF")  # Blue band
band2 = arcpy.sa.Raster(source + r"\LT05_L1TP_025039_20111031_20200820_02_T1_B2.TIF")  # Green band
band3 = arcpy.sa.Raster(source + r"\LT05_L1TP_025039_20111031_20200820_02_T1_B3.TIF")  # Red band
band4 = arcpy.sa.Raster(source + r"\LT05_L1TP_025039_20111031_20200820_02_T1_B4.TIF")  # Near-infrared band 


# Allow output to overwrite existing files to assist with code testing
arcpy.env.overwriteOutput = True

# If a composite raster already exists, delete it.
out_composite = os.path.join(source, "combined.tif")
if arcpy.Exists(out_composite):
    arcpy.management.Delete(out_composite)

# Create the composite raster by stacking the four input bands.
arcpy.management.CompositeBands([band1, band2, band3, band4], source + "\combined.tif")

# =============================================
# Hillshade 
# =============================================

# Generate a hillshade raster from the DEM to highlight terrain morphology.
source = r"C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025-Lab07-Images\DEM"
azimuth = 315        # Sun azimuth angle (from north -> clockwise)
altitude = 45        # Sun elevation angle above horizon
shadows = "NO_SHADOWS"
z_factor = 1         # Vertical exaggeration -> kept at 1 for metric consistency
arcpy.ddd.HillShade(source + r"\n29_w096_1arc_v3.tif",source + r"\n29_w096_1arc_v3_hillshade.tif", azimuth, altitude, shadows, z_factor)


# =============================================
# Slope 
# =============================================

# Calculate slope in degrees from the DEM. This provides quantitative information about surface gradient, relevant to hydrology, geomorphology, and land use planning.
source = r"C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025-Lab07-Images\DEM"
output_measurement = "DEGREE"
z_factor = 1
# method = "PLANAR"   # Defaults to planar
# z_unit = "METERS"   # Units inferred from DEM
arcpy.ddd.Slope(source + r"\n29_w096_1arc_v3.tif", source + r"\n29_w096_1arc_v3_slope.tif", output_measurement, z_factor)
