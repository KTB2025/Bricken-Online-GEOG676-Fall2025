# TAMU GIS Programming: Homework 06 — Map Generation Toolbox

**Author:** Kate Bricken  
**Course:** GEOG 676 – GIS Programming  
**Assignment Due Date:** October 13, 2025

---

## Assignment Overview
Build a Python Toolbox tool that applies a **Graduated Colors** renderer to a layer in an ArcGIS Pro project, shows progress with a **step progressor**, and saves an updated **.aprx** copy.

---

## Tasks
- Create a script that generates a **GraduatedColorsRenderer** (choropleth) map.  
- Package the script as a **Python Toolbox (.pyt)** accessible in the ArcGIS Pro Catelog under Toolboxes.  
- Use a **step progressor** whose label updates at key stages (open project -> locate layer -> apply renderer -> save copy).

---

## Tool: Create a Graduated Colors or Chloropleth Map
**Class:** `GraduatedColorsRenderer` (inside `HW06MapTool.pyt`)  
**Category:** Map Creation Tools

### Parameters
| # | Name (Display) | Type | Notes |
|---|---|---|---|
| 1 | Input ArcGIS Pro Project (.aprx) | `DEFile` | Path to the source .aprx (will be opened and copied). |
| 2 | Classification Layer (feature layer) | `GPFeatureLayer` | Pick a layer from the current session. |
| 3 | Classification Field (numeric field) | `Field` | Filtered to numeric: Short, Long, Float, Double. |
| 4 | Break Count | `GPLong` (Range 3–9) | Number of classes in the choropleth. |
| 5 | Color Ramp Name | `GPString` (Optional) | Tries exact name; falls back to first available ramp. |
| 6 | Output Folder | `DEFolder` | Where the new .aprx copy will be written. |
| 7 | Output Project Name (no .aprx) | `GPString` | Name Exported Project/Map with .aprx extension added automatically. |

---

## How to Run
1. **Prep the .aprx**  
   - Create a new Pro project, add `Campus.gdb`, and add **GarageParking** (or another polygon layer). Save.
2. **Add the toolbox**  
   - In **Catalog** -> **Toolboxes** → right-click → **Add Toolbox…** -> select `HW06MapTool.pyt`.
3. **Open the tool**  
   - Toolbox drop down - ArcGIS Pro Catelog -> **Make a Graduated Colors Map**.
4. **Fill parameters**  
   - Input .aprx = your saved project  
   - Classification Layer = the layer you want symbolized  
   - Classification Field = a numeric field (e.g., `Shape_Area`)  
   - Break Count = 3–9 (default 5)  
   - Color Ramp = e.g., `Greens (5 Classes)` (optional)  
   - Output Folder
   - Output Project Name
5. **Run**  
   - Watch the **step progressor** messages update through each stage. A new **.aprx** copy is created in your output folder.

---

## Expected Output
- A **new .aprx** saved to your output folder, in which the target layer has a **Graduated Colors** renderer using the chosen field, break count, and color ramp.  
- The current map view (live layer) is also updated when possible so you can see changes immediately.

---

## Screenshot of the Tool
**.Py Script Run in Visual Studio Code**
![HW06 Screenshot #1](https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/blob/e0a825c4b0ac950cd5a8afb23aecefdfa0d5ede3/Lab06/Images/PyCodeRunVCS.png)
**.Pyt Run in ArcGIS Pro - Successful**
![HW06 Screenshot #1](https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/blob/e0a825c4b0ac950cd5a8afb23aecefdfa0d5ede3/Lab06/Images/CodeRunInArcGISPro_1.png
)
**The .Aprx file Created By The Tool With Chloropleth Map**
![HW06 Screenshot #1](https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/blob/e0a825c4b0ac950cd5a8afb23aecefdfa0d5ede3/Lab06/Images/OutputAprxAndMap.png)


---

## Submission Items
- Screenshot of `.py` code run in Visual Studio Code showing **no errors** in the terminal.  
- Screenshot of **ArcGIS Pro** toolbox run (no error popups) and resulting symbology visible.  
- Link to GitHub repo containing `HW06MapTool.pyt` and this `README.md`.  

---

## Troubleshooting
- **Output .aprx looks “empty.”**  
  Ensure the input .aprx actually contains a map with a layer that **matches the selected layer’s name**. If not found, the tool warns and only updates the live layer.
- **No color ramp found.**  
  Try a known ramp label like `Greens (5 Classes)` or leave blank to auto-fallback.
- **Field not in layer / not numeric.**  
  Choose a numeric field (e.g., `Shape_Area`)—the parameter is filtered to numeric types.  
- **Progressor shows but no changes.**  
  Verify the correct **input .aprx** is selected, and the **Output Name** isn’t adding “.aprx” twice.

