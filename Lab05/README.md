# TAMU GIS Programming: Homework 05 — Creating a Toolbox

**Author:** Kate Bricken  
**Course:** GEOG 676 - GIS Programming  
**Assignment Date:** September 29, 2025

---

## Assignment Overview

This assignment builds on the work completed in **Homework 04**. The original Python script that buffered garage points and intersected them with campus buildings has now been transformed into a **custom ArcGIS tool**. The tool has been packaged inside a user-defined **ArcGIS Toolbox (.tbx)** and can be reused within **ArcGIS Pro**.

---

## Tasks

- Convert a standalone ArcPy script into a parameterized geoprocessing tool
- Integrate the tool into a custom ArcGIS toolbox
- Test and run the tool directly within ArcGIS Pro
- Learn how to use script tools and parameter inputs
- Prepare the tool for future analysis and potential reuse

---

## Tool Description

**Name:** `GarageBufferIntersectTool`  
**Toolbox:** `!!! Insert New Name Here!!!.tbx`  
**Script:** `garage_buffer_intersect_tool.py`

This tool performs the following operations:

1. Buffers input **garage point features** by a user-defined distance (in meters)
2. Intersects the resulting buffer with a **building features layer**
3. Exports the intersection results as a `.csv` to the user-specified output location

---

## Parameters

| Parameter Name       | Type            | Description                                         |
|----------------------|------------------|-----------------------------------------------------|
| `Input_Garages`      | Feature Layer     | Garage point features to buffer                    |
| `Input_Structures`   | Feature Layer     | Building polygons to intersect                     |
| `Buffer_Distance`    | Linear Unit       | Buffer distance (e.g., "100 Meters")               |
| `Output_GDB`         | Workspace         | Geodatabase where outputs will be saved            |
| `Output_CSV`         | File              | Full path for final CSV output                     |

---

## Project Structure
Lab05/
├── garage_buffer_intersect_tool.py # Python script with tool logic
├── !!!Insert New Name Here!!!.tbx # Custom ArcGIS toolbox containing the tool
├── garages.csv # Input garage data (from HW04)
├── Campus.gdb/ # Provided geodatabase with Structures layer
├── HW04.gdb/ # Output GDB from HW04 (used as input)
├── garage_building_results.csv # Output CSV from the tool
└── README.md # This documentation file


---

## How to Run the Tool

1. Open **ArcGIS Pro**.
2. Open the `Catalog` pane and right-click to **add toolbox** (`!!!Insert New Name Here!!!.tbx`).
3. Double-click the tool: `GarageBufferIntersectTool`.
4. Fill out the tool dialog:
   - Select garage feature layer
   - Select structures layer
   - Enter buffer distance (e.g., `100 Meters`)
   - Choose an output geodatabase
   - Define a path to the output CSV
5. Click **Run**.

The output will include:
- A new buffer feature class
- An intersect result layer
- A final `.csv` listing intersected structures for each garage buffer

---

## Screenshot of the Tool in ArcGIS Pro

> *(Insert screenshot here of the toolbox and tool running in ArcGIS Pro)*

---

## Submission Items

- Python tool script (`garage_buffer_intersect_tool.py`)
- Custom toolbox (`!!!Create New Name here!!!.tbx`)
- Screenshot of tool running in ArcGIS Pro
- Output CSV
- This `README.md`

---

## Related Work

This tool builds directly on:

🔗 [Homework 04: Fun with arcpy](../Lab04/README.md)  
See HW04 for original CSV data input, geodatabase creation, and standalone script logic.


