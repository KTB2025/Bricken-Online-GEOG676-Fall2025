# =============================================
# TAMU GIS Programming: Homework 06 - Map Generation Toolbox
# Author: Kate Bricken
# Date: 09/08/2025
# =============================================

# -*- coding: utf-8 -*-
import arcpy
import os
import time


class Toolbox:
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Toolbox"
        self.alias = "toolbox"

        # List of tool classes associated with this toolbox
        self.tools = [GraduatedColorsRenderer]


class GraduatedColorsRenderer:
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Make a Graduated Colors Map"
        self.description = ("Create a Graduated Colors map for an existing ArcGIS Pro project with a progressor and a saved output copy.")
        self.canRunInBackground = False
        self.category = "Map Creation Tools"

    # ----------------------------
    # Parameters
    # ----------------------------

    def getParameterInfo(self):
        """Define the tool parameters."""
        p0 = arcpy.Parameter(
            displayName="Input ArcGIS Pro Project (.aprx)", 
            name="aprx_input",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")
        p0.filter.list = ['aprx']

        p1 = arcpy.Parameter(
            displayName="Classification Layer (feature layer)",
            name="in_layer",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        p1.filter.list = ['Polygon']

        p2 = arcpy.Parameter(
            displayName="Classification Field (numeric field)",
            name="Class_field",
            datatype="Field",
            parameterType="Required",
            direction="Input")
        p2.parameterDependencies = [p1.name] 
        # limit to numeric types
        p2.filter.list = ["Short", "Long", "Float", "Double"]
                
        p3 = arcpy.Parameter(
            displayName="Break Count",
            name="Break_Count",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
        p3.filter.type = "Range"
        p3.filter.list = [3,9]  #Set min and max values for break count
        p3.value = 5  #Set default value for break count
        
        p4 = arcpy.Parameter(
            displayName="Color Ramp Name",
            name="ColorRampName",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p4.value = "Greens (5 Classes)"  #Update with a different default color ramp name

        p5 = arcpy.Parameter(
            displayName="Output Folder",
            name="Out_Folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        p6 = arcpy.Parameter(
            displayName="Output Project Name (no .aprx)",
            name="Out_Name",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        return [p0, p1, p2, p3, p4, p5, p6]

    def isLicensed(self):
        """Set whether the tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""
        return
    
    # ----------------------------
    # Execute
    # ----------------------------

    def execute(self, parameters, messages):
        """The source code of the tool."""
        """Tool Plan: open APRX -> set renderer -> save a copy."""
        aprx_path  = parameters[0].valueAsText
        layer      = parameters[1].value            # GPFeatureLayer from current project  
        class_fld  = parameters[2].valueAsText        
        break_cnt  = int(parameters[3].value)
        ramp_name  = parameters[4].valueAsText or f"Greens ({break_cnt} Classes)"
        out_folder = parameters[5].valueAsText
        out_name   = (parameters[6].valueAsText or "").strip().removesuffix(".aprx")
        out_aprx   = os.path.join(out_folder, f"{out_name}.aprx")

    # ----------------------------
    # Progressor
    # ----------------------------

        readTime, start, maximum, step = 1.0, 0, 100, 25
        arcpy.SetProgressor("step", "Opening project…", start, maximum, step)
        time.sleep(readTime)
        arcpy.AddMessage("Opening project…")

        project = arcpy.mp.ArcGISProject(aprx_path)        # Open the .aprx file on disk - the copy

        # Find a layer of the same name inside the loaded APRX
        target_name = layer.name

        target_in_aprx = None
        for m in project.listMaps():  
            for lyr in m.listLayers():
                if getattr(lyr, "isFeatureLayer", False) and lyr.name == target_name:
                    target_in_aprx = lyr
                    break
            if target_in_aprx:
                break

        # If not found in the aprx, fall back to the live current project
        if not target_in_aprx:
            arcpy.AddWarning(f"Could not find a layer named '{target_name}' in {aprx_path}. "
                            "Applying changes to the live layer only; saved copy may look empty.")
            target_in_aprx = layer  # fall back so user still sees results in session
    
        # Safety checks on the target layer
        if not getattr(target_in_aprx, "isFeatureLayer", False):
            raise arcpy.ExecuteError("Selected input is not a feature layer.")

        # ----------------------------
        # Symbology
        # ----------------------------

        symbology = target_in_aprx.symbology
        if not hasattr(symbology, "renderer"):
            raise arcpy.ExecuteError("Selected layer does not support a renderer.")

        arcpy.SetProgressorPosition(start + step*2)
        arcpy.SetProgressorLabel("Applying Graduated Colors…")
        time.sleep(readTime)
        arcpy.AddMessage("Applying Graduated Colors…")

        # ----------------------------
        # Apply renderer + parameters
        # ----------------------------

        symbology.updateRenderer("GraduatedColorsRenderer")
        symbology.renderer.classificationField = class_fld
        symbology.renderer.breakCount = max(3, min(9, break_cnt))

        ramps = project.listColorRamps(ramp_name)
        if not ramps:
            arcpy.AddWarning(f"Color ramp '{ramp_name}' not found; using first available.")
            ramps = project.listColorRamps()
        if not ramps:
            raise arcpy.ExecuteError("No color ramps available in this project.")
        symbology.renderer.colorRamp = ramps[0]

        # Commit back to the layer in the copy
        target_in_aprx.symbology = symbology

        # Also update the layer in the live/current project so the live map reflects the change
        try:
            current_aprx = arcpy.mp.ArcGISProject("CURRENT")
            updated_live = False
            for cm in current_aprx.listMaps():
                for clyr in cm.listLayers():
                    if getattr(clyr, "isFeatureLayer", False) and clyr.name == target_name:
                        # Build symbology fresh in live project 
                        c_sym = clyr.symbology
                        if not hasattr(c_sym, "renderer"):
                            continue
                        c_sym.updateRenderer("GraduatedColorsRenderer")
                        c_sym.renderer.classificationField = class_fld
                        c_sym.renderer.breakCount = max(3, min(9, break_cnt))

                        # Resolve a ramp in CURRENT; fall back if name not found
                        c_ramps = current_aprx.listColorRamps(ramp_name) or current_aprx.listColorRamps()
                        if c_ramps:
                            c_sym.renderer.colorRamp = c_ramps[0]

                        clyr.symbology = c_sym
                        updated_live = True
                        break
                if updated_live:
                    break

            if not updated_live:
                arcpy.AddWarning(
                    "Couldn’t find a matching layer by name in the CURRENT project; "
                    "live map symbology may not update."
                )
        except Exception as e:
            arcpy.AddWarning(f"Live project update skipped: {e}")


        arcpy.SetProgressorPosition(start + step*3)
        arcpy.SetProgressorLabel("Saving a copy of the project…")
        time.sleep(readTime)
        arcpy.AddMessage("Saving a copy of the project…")

        project.saveACopy(out_aprx) # Save the modified aprx copy to disk

        arcpy.SetProgressorPosition(maximum)
        arcpy.SetProgressorLabel("Done.")
        time.sleep(readTime)
        arcpy.AddMessage(f"Saved new project to: {out_aprx}")
        return
