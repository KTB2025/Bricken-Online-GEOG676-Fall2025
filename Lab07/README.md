# TAMU GIS Programming: Homework 07 — Raster Analysis

**Author:** Kate Bricken  
**Course:** GEOG 676 – GIS Programming  
**Assignment Due Date:** October 17, 2025  

---

## Assignment Overview
This assignment focuses on **raster analysis** using satellite imagery and digital elevation data.  
The goal is to practice working with **raster datasets in ArcPy**, including combining multiple spectral bands, generating derived terrain rasters, and visualizing topography through shaded relief and slope.  

---

## Tasks
- Download multispectral satellite imagery (e.g., **Landsat**) separated by bands.  
- Create a **composite raster** image by stacking several spectral bands.  
- Download a **Digital Elevation Model (DEM)** of an area of interest. For this project this was centerted on the Houston-Galveston area.   
- Use the DEM to create two analytical outputs:
  1. **Hillshade raster** to visualize topographic relief.  
  2. **Slope raster** to quantify terrain gradients.  
---

## Script Description

**Script:** `HW07_RasterAnalysis.py`  

This Python script automates raster analysis steps within ArcGIS Pro using the **arcpy.sa** and **arcpy.ddd** modules. It creates a composite raster from Landsat imagery, then generates both **hillshade** and **slope** rasters from a DEM to analyze surface form and topographic variation.

### Operations Performed
1. **Load Spectral Bands**  
   - Imports the blue, green, red, and near-infrared (NIR) Landsat bands as raster objects.  

2. **Create Composite Raster**  
   - Combines the four bands into a single multispectral raster (`combined.tif`) using `arcpy.management.CompositeBands`.  

3. **Generate Hillshade Raster**  
   - Applies `arcpy.ddd.HillShade` to the DEM to produce a shaded relief raster simulating illumination from the northwest (azimuth 315°, altitude 45°).  

4. **Calculate Slope Raster**  
   - Uses `arcpy.ddd.Slope` to compute slope in degrees from the DEM, useful for geomorphological or hydrological analysis.  

---

## Parameters
| # | Name | Type | Description |
|---|------|------|-------------|
| 1 | `source` | `String (Path)` | Directory path to Landsat or DEM datasets |
| 2 | `band1–band4` | `Raster` | Input spectral bands: Blue, Green, Red, NIR |
| 3 | `out_composite` | `Raster Output` | Combined multiband raster (`combined.tif`) |
| 4 | `azimuth` | `Long` | Sun azimuth angle (default: 315°) |
| 5 | `altitude` | `Long` | Sun elevation angle (default: 45°) |
| 6 | `shadows` | `String` | Shadow model option (set to `"NO_SHADOWS"`) |
| 7 | `z_factor` | `Float` | Vertical exaggeration (default: 1) |
| 8 | `output_measurement` | `String` | Unit of slope output (`"DEGREE"`) |

---

## How to Run
1. **Prepare Input Data**  
   - Download Landsat spectral bands (B1–B4) and place them in a single folder.  
   - Download a DEM (e.g., SRTM) for the same region.  

2. **Set Environment**  
   - Open the script in **ArcGIS Pro** or **Visual Studio Code** using the ArcGIS Pro Python environment.  
   - Confirm that the **Spatial Analyst** and **3D Analyst** extensions are enabled.  

3. **Run the Script**  
   - Update the `source` directory paths in the script to match the local workspace.  
   - Run the script.  
   - The following output rasters will be generated:  
     - `combined.tif` (composite raster)  
     - `n29_w096_1arc_v3_hillshade.tif` (hillshade raster)  
     - `n29_w096_1arc_v3_slope.tif` (slope raster)  

---

## Expected Output
- A **composite raster** showing combined Landsat RGB+NIR bands.  
- A **hillshade raster** representing shaded terrain relief.  
- A **slope raster** in degrees, visualizing terrain gradient intensity.  

---

## Output Images
**Composite Raster**  
![HW07 Screenshot #1](https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/blob/dd3a763ac17320b6306333b3288bad17386a435e/Lab07/Images/HoustonAreaLandsatComposite.png)

**Hillshade Raster**  
![HW07 Screenshot #2](https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/blob/dd3a763ac17320b6306333b3288bad17386a435e/Lab07/Images/HoustonAreaDEMHillshade.png)

**Slope Analysis Raster**  
![HW07 Screenshot #3](https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/blob/dd3a763ac17320b6306333b3288bad17386a435e/Lab07/Images/HoustonAreaDEMSlope.png)

---

## Submission Items
- Screenshot of **composite raster** output in ArcGIS Pro.  
- Screenshot of **hillshade raster** output in ArcGIS Pro.  
- Screenshot of **slope raster** output in ArcGIS Pro.  
- Link to **GitHub repository** containing `HW07_RasterAnalysis.py` and imagery data.  
- This very helpful and descriptive `README.md`.  
