# TAMU GIS Programming: Homework 05 — Creating a Toolbox

**Author:** Kate Bricken  
**Course:** GEOG 676 – GIS Programming  
**Assignment Due Date:** September 29, 2025  

---

## Assignment Overview

This assignment builds on the work completed in **Homework 04**. The original Python script that buffered garage points and intersected them with campus buildings has now been transformed into a **custom ArcGIS Python Toolbox (.pyt)**.  

The tool is parameterized, integrated into a toolbox, and can be run directly inside **ArcGIS Pro** with user inputs.  

---

## Tasks

- Convert the HW04 buffer + intersect script into a reusable ArcGIS tool  
- Define user parameters for inputs, outputs, and buffer distance  
- Add the tool into a custom ArcGIS Python Toolbox (.pyt)  
- Run and test the tool directly inside ArcGIS Pro  

---

## Tool Description

**Toolbox:** `HW05Toolbox.pyt`  
**Tool:** `Building Proximity (Buffer + Intersect)`  

This tool performs the following operations:  
1. Buffers input **garage point features** by a user-defined distance (meters).  
2. Intersects the resulting buffer with **building/structure features**.  
3. Writes the buffer and intersect outputs to a specified geodatabase.  

---

## Parameters

| Parameter Name     | Type            | Description                                              |
|--------------------|-----------------|----------------------------------------------------------|
| `GaragePoints`     | Feature Class   | Garage point features to buffer                          |
| `Buildings`        | Feature Class   | Campus buildings/structures to intersect with the buffer |
| `BufferMeters`     | Double          | Distance in meters to buffer garage points               |
| `OutputWorkspace`  | Workspace (GDB) | Geodatabase where results will be saved                  |
| `OutBufferName`    | String          | Name for the buffer feature class                        |
| `OutIntersectName` | String          | Name for the intersect feature class                     |

---

## How to Run the Tool

1. Open **ArcGIS Pro**.  
2. In the **Catalog** pane, right-click **Toolboxes → Add Toolbox…** and select `HW05Toolbox.pyt`.  
3. Double-click the tool: **Building Proximity (Buffer + Intersect)**.  
4. Fill out the tool dialog:  
   - Select **Garage** points feature class (from HW04 results).  
   - Select **Structures** feature class (from HW04 results).  
   - Enter buffer distance (e.g., `100`).  
   - Choose an output geodatabase (e.g., `HW05.gdb`).  
   - Enter names for the buffer and intersect outputs.  
5. Click **Run**.  

The outputs will include:  
- A new **buffer feature class** (e.g., `Garage_Buffers`).  
- A new **intersect feature class** (e.g., `Garage_Buildings_Intersect`).  
- A new **points feature class** (e.g, `Garage_Points_Reprojected`). 
---

## Example Run

**Parameters used:**  
- Garage Points: `HW04.gdb/Garages`  
- Buildings: `Campus.gdb/Structures`  
- Buffer Distance: `100`  
- Output Workspace: `HW05.gdb`  
- OutBufferName: `Garage_Buffers`  
- OutIntersectName: `Garage_Buildings_Intersect`  

**Expected Outputs:**  
- `HW05.gdb/Garage_Buffers`  
- `HW05.gdb/Garage_Buildings_Intersect`  
- `HW05.gdb/Garage_Points_Reprojected`

---

## Screenshot of the Tool Operating in ArcGIS Pro

![HW05 Screenshot #1](https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/blob/4be347d15da83d5021507abcde6e67d4ef824516/Lab05/Bricken_GEOG676_HW5.png)
![HW05 Screenshot #2](https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/blob/4be347d15da83d5021507abcde6e67d4ef824516/Lab05/Bricken_GEOG676_HW5_2.png)


---

## Submission Items

- Python toolbox file (`HW05Toolbox.pyt`)  
- Python file used for testing (`HW05PracticeToolboxCodex.py`)
- Python file used for progressor testing based off of the module notes (`ToolboxPracticeWithProgressorsAndExecute.py`)
- Screenshots of tool running in ArcGIS Pro 
- Output feature classes saved in `HW05.gdb`
- ArcGIS Pro Project File - `GEOG-676_HW05.aprx`
- This `README.md`  

---
