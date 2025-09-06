# =============================================
# TAMU GIS Programming: Homework 05 - Creating a Custom ArcGIS Toolbox Tool
# Author: Kate Bricken
# Date: 09/06/2025
# =============================================


# -*- coding: utf-8 -*-

import arcpy

class Toolbox(object):
    def __init__(self):
        self.label = "HW05 Tools"
        self.alias = "hw05"
        self.tools = [BuildingProximity]

class BuildingProximity(object):
    #Define the tool to be run in ArcGIS Pro
    def __init__(self):
        self.label = "Building Proximity (Buffer + Intersect)"
        self.description = "Buffers garage points and finds buildings intersecting those buffers."
        self.canRunInBackground = False
        self.category = "Building Tools"

    # ----------------------------
    # Parameters
    # ----------------------------

    def getParameterInfo(self):
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
        ); p2.value = 100.0
        p3 = arcpy.Parameter(
            displayName="Output Workspace (e.g., File GDB)",
            name="OutputWorkspace",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input"
        )
        p4 = arcpy.Parameter(
            displayName="Output Buffer Name",
            name="OutBufferName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        ); p4.value = "Garage_Buffers"
        p5 = arcpy.Parameter(
            displayName="Output Intersect Name",
            name="OutIntersectName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        ); p5.value = "Garage_Buildings_Intersect"
        return [p0, p1, p2, p3, p4, p5]

    def isLicensed(self):
        return True
    # Clean up names and remove spaces
    def updateParameters(self, parameters):
        for idx in (4, 5):
            if parameters[idx].value:
                parameters[idx].value = str(parameters[idx].value).strip().replace(" ", "_")
        return

    # ----------------------------
    # Execute
    # ----------------------------

    def execute(self, parameters, messages):
        """Buffer garage points (meters) and intersect with Buildings."""
        import os, time
        arcpy.env.overwriteOutput = True

         # All User Inputs
        garage_fc   = parameters[0].valueAsText
        bldg_fc     = parameters[1].valueAsText
        buffer_m    = float(parameters[2].value)
        out_ws      = parameters[3].valueAsText
        out_buf     = os.path.join(out_ws, parameters[4].valueAsText)
        out_int     = os.path.join(out_ws, parameters[5].valueAsText)

        if not arcpy.Exists(out_ws):
            raise arcpy.ExecuteError(f"Output workspace does not exist: {out_ws}")
        
        # ----------------------------
        # Progressor
        # ----------------------------

        arcpy.SetProgressor("step", "Preparing inputs…", 0, 100, 50)
        time.sleep(0.1)
        arcpy.AddMessage("Preparing inputs…")

 # Check if garage and building layers use the same spatial reference
        # If not, reproject garages so they match
        gar_sr = arcpy.Describe(garage_fc).spatialReference
        bld_sr = arcpy.Describe(bldg_fc).spatialReference
        garages_for_buffer = garage_fc
        proj_garages = os.path.join(out_ws, "Garage_Points_Reprojected")

        try:
            if gar_sr.name != bld_sr.name and bld_sr.name not in (None, "", "Unknown"):
                extent = arcpy.Describe(bldg_fc).extent
                transforms = arcpy.ListTransformations(gar_sr, bld_sr, extent)
                transform = transforms[0] if transforms else None
                arcpy.AddMessage(f"Using transformation: {transform}" if transform else "No geographic transformation required/available.")

                if arcpy.Exists(proj_garages):
                    arcpy.Delete_management(proj_garages)

                arcpy.management.Project(
                    in_dataset=garage_fc,
                    out_dataset=proj_garages,
                    out_coor_system=bld_sr,
                    transform_method=transform  # may be None
                )

                if not arcpy.Exists(proj_garages):
                    raise arcpy.ExecuteError("Projection completed but output FC not found. Check workspace permissions/paths.")

                arcpy.AddMessage(f"Reprojected garage points to {bld_sr.name} -> {proj_garages}")
                garages_for_buffer = proj_garages
            else:
                arcpy.AddMessage("Spatial references match or target SR unknown; skipping projection.")
        except Exception as e:
            arcpy.AddError(f"Projection failed: {e}")
            raise

        # Buffer garage points
        arcpy.SetProgressorPosition(50)
        arcpy.SetProgressorLabel("Buffering garage points…")
        time.sleep(0.1)

        if arcpy.Exists(out_buf):
            arcpy.Delete_management(out_buf)

        dist_str = f"{buffer_m} Meters"
        arcpy.Buffer_analysis(
            in_features=garages_for_buffer,
            out_feature_class=out_buf,
            buffer_distance_or_field=dist_str,
            line_side="FULL",
            line_end_type="ROUND",
            dissolve_option="NONE",
            method="PLANAR"
        )
        if not arcpy.Exists(out_buf):
            raise arcpy.ExecuteError("Buffer finished but output FC not found.")
        arcpy.AddMessage(f"Garage buffers -> {out_buf}")

        # Intersect buffers with buildings
        arcpy.SetProgressorPosition(100)
        arcpy.SetProgressorLabel("Intersecting buffers with Buildings…")
        time.sleep(0.1)

        if arcpy.Exists(out_int):
            arcpy.Delete_management(out_int)

        arcpy.Intersect_analysis(
            in_features=[out_buf, bldg_fc],
            out_feature_class=out_int,
            join_attributes="ALL"
        )
        if not arcpy.Exists(out_int):
            raise arcpy.ExecuteError("Intersect finished but output FC not found.")
        arcpy.AddMessage(f"Intersect result -> {out_int}")

        arcpy.AddMessage("Tool completed successfully.")
        return None
