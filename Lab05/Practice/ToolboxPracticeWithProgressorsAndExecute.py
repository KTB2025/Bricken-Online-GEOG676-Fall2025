
# -*- coding: utf-8 -*-

import arcpy
import os
import time

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "HW05 Tools"
        self.alias = "hw05"
        self.tools = [BuildingProximityTool]

class BuildingProximityTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Building Proximity (Buffers + Intersect)"
        self.description = ("Buffers garage points and finds buildings "
                            "intersecting those buffers.")
        self.canRunInBackground = False
        self.category = "Building Tools"

    # ----------------------------
    # Parameters
    # ----------------------------
    def getParameterInfo(self):
        """Define parameter definitions"""

        p0 = arcpy.Parameter(
            displayName="Garage Points (feature class)",
            name="GaragePoints",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input"
        )

        p1 = arcpy.Parameter(
            displayName="Buildings / Structures (feature class)",
            name="Buildings",
            datatype="DEFeatureClass",
            parameterType="Required",
            direction="Input"
        )

        p2 = arcpy.Parameter(
            displayName="Buffer Distance (meters)",
            name="BufferMeters",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )
        p2.value = 100.0

        p3 = arcpy.Parameter(
            displayName="Output Workspace (e.g., File GDB)",
            name="OutputWorkspace",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input"
        )

        p4 = arcpy.Parameter(
            displayName="Output Buffer Feature Class Name",
            name="OutBufferName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        p4.value = "Garage_Buffers"

        p5 = arcpy.Parameter(
            displayName="Output Intersect Feature Class Name",
            name="OutIntersectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        p5.value = "Garage_Buildings_Intersect"

        return [p0, p1, p2, p3, p4, p5]

    def isLicensed(self):
        return True

    def updateParameters(self, parameters):
        # Normalize names (no spaces)
        for idx in (4, 5):
            if parameters[idx].value:
                parameters[idx].value = str(parameters[idx].value).strip().replace(" ", "_")
        return

    def updateMessages(self, parameters):
        # Warn if spatial reference mismatch
        if parameters[0].value and parameters[1].value:
            try:
                sr_gar = arcpy.Describe(parameters[0].value).spatialReference
                sr_bld = arcpy.Describe(parameters[1].value).spatialReference
                if sr_gar.name != sr_bld.name:
                    parameters[0].setWarningMessage(
                        f"Garage SR ({sr_gar.name}) differs from Buildings SR ({sr_bld.name}). "
                        "Outputs will use Buildings SR."
                    )
            except Exception:
                pass
        return

    # ----------------------------
    # Execute
    # ----------------------------
    def execute(self, parameters, messages):
        """Perform buffer + intersect workflow."""

        # Inputs
        garage_fc = parameters[0].valueAsText
        bldg_fc   = parameters[1].valueAsText
        buffer_m  = float(parameters[2].value)
        out_ws    = parameters[3].valueAsText
        out_buff_name = parameters[4].valueAsText
        out_intersect = parameters[5].valueAsText

        # Env
        arcpy.env.overwriteOutput = True

        # Paths
        out_buff_path = os.path.join(out_ws, out_buff_name)
        out_intersect_path = os.path.join(out_ws, out_intersect)

        # Progressor setup
        start = 0
        maximum = 100
        step = 50
        pause = 0.5

        arcpy.SetProgressor("step", "Preparing inputs…", start, maximum, step)
        time.sleep(pause)
        arcpy.AddMessage("Preparing inputs…")

        # Match SR: project garage points if needed
        gar_sr = arcpy.Describe(garage_fc).spatialReference
        bld_sr = arcpy.Describe(bldg_fc).spatialReference
        garage_for_buffer = garage_fc

        if gar_sr.name != bld_sr.name and bld_sr.name not in (None, "", "Unknown"):
            projected_garage = os.path.join(out_ws, "Garage_Points_Reprojected")
            if arcpy.Exists(projected_garage):
                arcpy.Delete_management(projected_garage)
            arcpy.Project_management(garage_fc, projected_garage, bld_sr)
            garage_for_buffer = projected_garage
            arcpy.AddMessage(f"Reprojected garage points to {bld_sr.name}.")

        # Buffer garages
        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Buffering garage points…")
        time.sleep(pause)
        dist_str = f"{buffer_m} Meters"
        if arcpy.Exists(out_buff_path):
            arcpy.Delete_management(out_buff_path)
        arcpy.Buffer_analysis(garage_for_buffer, out_buff_path, dist_str, dissolve_option="NONE")
        arcpy.AddMessage(f"Garage buffers created → {out_buff_path}")

        # Intersect
        arcpy.SetProgressorPosition(start + 2*step)
        arcpy.SetProgressorLabel("Intersecting buffers with Buildings…")
        time.sleep(pause)
        if arcpy.Exists(out_intersect_path):
            arcpy.Delete_management(out_intersect_path)
        arcpy.Intersect_analysis([out_buff_path, bldg_fc], out_intersect_path, join_attributes="ALL")
        arcpy.AddMessage(f"Intersect done → {out_intersect_path}")

        arcpy.SetProgressorPosition(maximum)
        arcpy.SetProgressorLabel("Finished")
        time.sleep(pause)
        arcpy.AddMessage("Tool completed successfully.")

        return None
