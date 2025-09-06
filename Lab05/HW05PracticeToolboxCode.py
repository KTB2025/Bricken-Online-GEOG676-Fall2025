# -*- coding: utf-8 -*-
import arcpy, os

class Toolbox(object):
    def __init__(self):
        self.label = "HW05 Tools"
        self.alias = "hw05"
        self.tools = [BuildingProximity]

class BuildingProximity(object):
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

    def updateParameters(self, parameters):
        for idx in (4, 5):
            if parameters[idx].value:
                parameters[idx].value = str(parameters[idx].value).strip().replace(" ", "_")
        return
    # ----------------------------
    # Execute
    # ----------------------------
    def execute(self, parameters, messages):
        arcpy.env.overwriteOutput = True

        # Inputs
        garage_fc   = parameters[0].valueAsText
        bldg_fc     = parameters[1].valueAsText
        buffer_m    = float(parameters[2].value)
        out_ws      = parameters[3].valueAsText
        out_buf     = os.path.join(out_ws, parameters[4].valueAsText)
        out_int     = os.path.join(out_ws, parameters[5].valueAsText)

        if not arcpy.Exists(out_ws):
            raise arcpy.ExecuteError(f"Output workspace does not exist: {out_ws}")

        # --- Ensure SR match: project garages to Buildings SR if needed (to in_memory)
        gar_sr = arcpy.Describe(garage_fc).spatialReference
        bld_sr = arcpy.Describe(bldg_fc).spatialReference
        garages_for_buffer = garage_fc

        if gar_sr.name != bld_sr.name and bld_sr.name not in (None, "", "Unknown"):
            proj_tmp = r"in_memory\garages_reproj"
            # pick first available transformation if any
            transforms = arcpy.ListTransformations(gar_sr, bld_sr, arcpy.Describe(bldg_fc).extent)
            transform = transforms[0] if transforms else None
            arcpy.management.Project(garage_fc, proj_tmp, bld_sr, transform)
            garages_for_buffer = proj_tmp
            arcpy.AddMessage(f"Reprojected garage points to {bld_sr.name}" + (f" using {transform}" if transform else ""))

        # --- Buffer (no dissolve) with explicit meter units
        arcpy.analysis.Buffer(
            in_features=garages_for_buffer,
            out_feature_class=out_buf,
            buffer_distance_or_field=f"{buffer_m} Meters",
            line_side="FULL",
            line_end_type="ROUND",
            dissolve_option="NONE",
            method="PLANAR"
        )
        arcpy.AddMessage(f"Garage buffers → {out_buf}")

        # --- Intersect
        arcpy.analysis.Intersect(
            in_features=[out_buf, bldg_fc],
            out_feature_class=out_int,
            join_attributes="ALL"
        )
        arcpy.AddMessage(f"Intersect result → {out_int}")

        return None
