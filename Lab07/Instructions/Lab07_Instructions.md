# TAMU GIS Programming: Homework 07
>
>**Topic:** Raster analysis 

# **Task:**
> - Find and download satellite imagery that is split up by band. [Landsat](https://landsat.usgs.gov/landsat-data-access) is a great choice.  Add the imagery to your Github.
> - Using the satellite imagery you downloaded, create a composite raster image
> - Find a digital elevation model of your area of interest and create the following: [Shace-Shuttle Radar Topography Mission](https://www2.jpl.nasa.gov/srtm/) is a great choice.  Add the DEM to your Github.
>   - A hillshade analysis raster
>   - A slope analysis raster
>
# **To Hand In:**
1. Link to your Github page that contains the Python code 60pts
2. Provide screenshot of your composit raster image 20pts
3. Provide screenshot of your hillshade raster image 10pts
4. Provide screenshot of you slope analysis raster image 10pts
>
# Raster analysis
For this homework assignment, you will be finding and downloading your own satellite imagery and combining the different bands into a single composite image. Once you have your composite image, you'll be tasked with finding a digital elevation model raster for your area of interest. With your DEM in hand, create a hillshade analysis raster and a slope analysis raster.

# Homework 07B
# **Task:**
> - Find and download satellite imagery that is split up by band
> - Create a composite image using the rasters you downloaded
> - Make a clipping mask polygon of the darkest area you can find
> - Create an atmospherically corrected multiband raster

# **To Hand In:**
1. Link to your Github page that contains the Python code
# Atmospherically corrected mutliband raster
For this homework assignment, you will be creating whats known as an atmospherically corrected multiband raster. What this entails is finding the darkest / blackest region of a raster and creating a polygon feature that covers the entire area. Once you have both a composite image and a feature layer that contains the polygon (also called the clipping mask), you 
# Download satellite imagery
A great place to get satellite imagery is from USGS and their **EarthExplorer** platform. The area you select does not matter for this exercise, just make sure that for the **Data Sets** option you select **Landsat**. 
# Composite image
Using the information from the second rasters lecture, create a composite image from your downloaded raster imagery.
# Clipping mask