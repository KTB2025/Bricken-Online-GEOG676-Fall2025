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
        self.description = "Create a Graduated Colors map for an existing ArcGIS Pro project" \
                            " with a progressor and a saved output copy."
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
            displayName="Layer to Classify",
            name="Class_field",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input")
        
        p2 = arcpy.Parameter(
            displayName="Break Count",
            name="Break_Count",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
        p2.filter.type = "Range"
        p2.filter.list = [3,9]  #Set min and max values for break count
        p2.value = 5  #Set default value for break count
        
        p3 = arcpy.Parameter(
            displayName="Color Ramp Name",
            name="ColorRampName",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p3.value = "Green (5 Classes)"  #Update with a different default color ramp name 

        p4 = arcpy.Parameter(
            displayName="Output Folder",
            name="Out_Folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        p5 = arcpy.Parameter(
            displayName="Output Project Name (no .aprx)",
            name="Out_ Name",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        return [p0, p1, p2, p3, p4, p5]
      

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
        aprx_path = parameters[0].valueAsText
        in_layer = parameters[1].value  # GPFeatureLayer reference
        break_count = int(parameters[2].value)
        ramp_name = parameters[3].valueAsText or f"Oranges ({break_count} Classes)"
        out_folder = parameters[4].valueAsText
        out_name = parameters[5].valueAsText.strip()
        out_aprx = os.path.join(out_folder, f"{out_name}.aprx")

        # ----------------------------
        # Progressor
        # ----------------------------

        # Progressor setup
        readTime = 1.0
        start = 0
        maximum = 100
        step = 25
        arcpy.SetProgressor("step", "Opening project…", start, maximum, step)
        time.sleep(readTime)

        arcpy.AddMessage("Opening project…")
        project = arcpy.mp.ArcGISProject(aprx_path)

        # Try to resolve the map that contains the chosen layer
        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Locating layer in map…")
        time.sleep(readTime)
        arcpy.AddMessage("Locating layer in map…")

        # The GPFeatureLayer parameter already points to the live layer in the map, but we still need its symbology via the layer object.
        layer = in_layer

        if not getattr(layer, "isFeatureLayer", False):
            raise arcpy.ExecuteError("Selected input is not a feature layer.")

        sym = layer.symbology
        if not hasattr(sym, "renderer"):
            raise arcpy.ExecuteError("Selected layer does not support a renderer.")

        # Apply Graduated Colors renderer
        arcpy.SetProgressorPosition(start + step*2)
        arcpy.SetProgressorLabel("Applying Graduated Colors…")
        time.sleep(readTime)
        arcpy.AddMessage("Applying Graduated Colors…")

        sym.updateRenderer("GraduatedColorsRenderer")

        # Classification field — lab uses GarageParking.Shape_Area
        # (Adjust if your layer uses a different numeric field.)
        sym.renderer.classificationField = "Shape_Area"

        sym.renderer.breakCount = break_count

        # Try to find a ramp by name; fall back to first available multi-class ramp
        ramps = project.listColorRamps(ramp_name)
        if not ramps:
            ramps = project.listColorRamps()  # any
        if not ramps:
            raise arcpy.ExecuteError("No color ramps available in this project.")
        sym.renderer.colorRamp = ramps[0]

        # Commit symbology back to the layer
        layer.symbology = sym

        # Save a copy of the project
        arcpy.SetProgressorPosition(start + step*3)
        arcpy.SetProgressorLabel("Saving a copy of the project…")
        time.sleep(readTime)
        arcpy.AddMessage("Saving a copy of the project…")

        project.saveACopy(out_aprx)

        arcpy.SetProgressorPosition(maximum)
        arcpy.SetProgressorLabel("Done.")
        time.sleep(readTime)
        arcpy.AddMessage(f"Saved new project to: {out_aprx}")
        return