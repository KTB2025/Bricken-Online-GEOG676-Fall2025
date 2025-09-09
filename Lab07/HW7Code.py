# =============================================
# TAMU GIS Programming: Homework 07 - Raster Analysis
# Author: Kate Bricken
# Date: 09/08/2025
# =============================================

import arcpy
import os

# R5 Composite Bands 

source = r"C:\Mac\Home\Documents\GEOG 676\Lab07\LT05_L1TP_026039_20110819_20200820_02_T1"
band1 = arcpy.sa.Raster(source + r"\LT05_L1TP_026039_20110819_20200820_02_T1_B1.TIF") # blue 
band2 = arcpy.sa.Raster(source + r"\LT05_L1TP_026039_20110819_20200820_02_T1_B2.TIF") # gree
band3 = arcpy.sa.Raster(source + r"\LT05_L1TP_026039_20110819_20200820_02_T1_B3.TIF") # red
band4 = arcpy.sa.Raster(source + r"\LT05_L1TP_026039_20110819_20200820_02_T1_B4.TIF") # NIR

#Delete existing composite output
arcpy.env.overwriteOutput = True

out_composite = os.path.join(source, "combined.tif")
if arcpy.Exists(out_composite):
    arcpy.management.Delete(out_composite)

arcpy.management.CompositeBands([band1, band2, band3, band4], out_composite)

composite = arcpy.CompositeBands_management([band1, band2, band3, band4], source + "\combined.tif")


# Hillshade
source = r"C:\Mac\Home\Documents\GEOG 676\Lab07\DEM"
azimuth = 315
altitude = 45
shadows = "NO_SHADOWS"
z_factor = 1
arcpy.ddd.HillShade(source + r"\n30_w097_1arc_v3.tif", source + r"\n30_w097_1arc_v3_hillshade.tif", azimuth, altitude, shadows, z_factor)



# Slope
source = r"C:\Mac\Home\Documents\GEOG 676\Lab07\DEM"
output_measurement = "DEGREE"
z_factor = 1
# method = "PLANAR"
# z_unit = "METERS"
arcpy.ddd.Slope(source + r"\n30_w097_1arc_v3.tif", source + r"\n30_w097_1arc_v3_slope.tif", output_measurement, z_factor)