# =============================================
# TAMU GIS Programming: Homework 05 - Creating a Custom ArcGIS Toolbox Tool
# Author: Kate Bricken
# Date: 09/02/2025
# =============================================
import arcpy
import os

class Toolbox(object):
    def __init__(self):
        self.label = "Campus Proximity Tools"
        self.alias = "campus"
        self.tools = [BuildingProximity]


class BuildingProximity(object):
    def __init__(self):
        self.label = "Garage Buffers ∩ Structures"
        self.description = ("Buffers garage points and intersects with campus buildings. "
                            "Provide existing garages (points) and structures (polygons).")
        self.canRunInBackground = True
        self.category = "Building Tools"

    def getParameterInfo(self):
        p0 = arcpy.Parameter(
            displayName="Garages (Point Feature Class/Layer)",
            name="garages_fc",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )
        p1 = arcpy.Parameter(
            displayName="Structures (Polygon Feature Class/Layer)",
            name="structures_fc",
            datatype="GPFeatureLayer",
            parameterType="Required",
            direction="Input"
        )
        p2 = arcpy.Parameter(
            displayName="Buffer Distance",
            name="buffer_distance",
            datatype="GPLinearUnit",
            parameterType="Required",
            direction="Input"
        )
        p2.value = "100 Meters"  # sensible default

        p3 = arcpy.Parameter(
            displayName="Output Geodatabase (optional; defaults to scratch GDB)",
            name="out_gdb",
            datatype="DEWorkspace",
            parameterType="Optional",
            direction="Input"
        )

        p4 = arcpy.Parameter(
            displayName="Output Feature Class Name",
            name="out_fc_name",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        p4.value = "Garage_Buildings_Intersection"

        p5 = arcpy.Parameter(
            displayName="(Optional) Export Intersections to CSV",
            name="out_csv_path",
            datatype="DEFile",
            parameterType="Optional",
            direction="Input"
        )

        # Derived output so ArcGIS Pro shows it in the UI
        p6 = arcpy.Parameter(
            displayName="Intersections (Output)",
            name="out_intersections",
            datatype="DEFeatureClass",
            parameterType="Derived",
            direction="Output"
        )

        return [p0, p1, p2, p3, p4, p5, p6]

    def isLicensed(self):
        return True

    def updateParameters(self, params):
        # If user picked a feature layer, hint its name for output
        if params[0].altered and not params[4].altered:
            base = arcpy.Describe(params[0].value).baseName
            params[4].value = f"{base}_Buildings_Intersection"
        return

    def updateMessages(self, params):
        # Warn if geometries aren't the expected types
        if params[0].value:
            if arcpy.Describe(params[0].value).shapeType.lower() != "point":
                params[0].setErrorMessage("Garages must be a point feature class/layer.")
        if params[1].value:
            if arcpy.Describe(params[1].value).shapeType.lower() not in ("polygon", "multipatch"):
                params[1].setErrorMessage("Structures must be a polygon feature class/layer.")
        return

    def execute(self, parameters, messages):
        arcpy.env.overwriteOutput = True

        garages = parameters[0].valueAsText
        structures = parameters[1].valueAsText
        buf_dist = parameters[2].valueAsText  # e.g., "100 Meters"
        out_gdb = parameters[3].valueAsText or arcpy.env.scratchGDB
        out_name = parameters[4].valueAsText
        out_csv = parameters[5].valueAsText  # may be None

        arcpy.AddMessage(f"Using output workspace: {out_gdb}")

        # Resolve output paths
        out_fc = os.path.join(out_gdb, out_name)
        tmp_garages = garages  # may be replaced if we project
        scratch = arcpy.env.scratchGDB

        # Ensure SR match so buffer units behave as expected
        sr_struct = arcpy.Describe(structures).spatialReference
        sr_gar = arcpy.Describe(garages).spatialReference

        if not sr_gar or not sr_struct or sr_gar.factoryCode != sr_struct.factoryCode:
            arcpy.AddMessage("Projecting garages to match structures' spatial reference...")
            tmp_garages = os.path.join(scratch, "Garages_Proj")
            if arcpy.Exists(tmp_garages):
                arcpy.management.Delete(tmp_garages)
            arcpy.management.Project(garages, tmp_garages, sr_struct)

        # Buffer
        buffers = os.path.join(scratch, "Garage_Buffers")
        if arcpy.Exists(buffers):
            arcpy.management.Delete(buffers)
        arcpy.AddMessage(f"Buffering garages by {buf_dist} ...")
        arcpy.analysis.Buffer(tmp_garages, buffers, buf_dist, dissolve_option="NONE")

        # Intersect
        if arcpy.Exists(out_fc):
            arcpy.management.Delete(out_fc)
        arcpy.AddMessage("Intersecting buffers with structures...")
        arcpy.analysis.Intersect([buffers, structures], out_fc, "ALL")

        # Set derived output so it shows in the UI
        parameters[6].value = out_fc
        arcpy.AddMessage(f"✓ Created intersections: {out_fc}")

        # Optional CSV export
        if out_csv:
            # Ensure folder exists & write as CSV (not DBF)
            out_folder = os.path.dirname(out_csv)
            if not out_csv.lower().endswith(".csv"):
                out_csv = out_csv + ".csv"
            arcpy.AddMessage(f"Exporting attribute table to CSV: {out_csv}")
            # Make a temp table view then export
            view = "intersect_view"
            if arcpy.Exists(view):
                arcpy.management.Delete(view)
            arcpy.management.MakeTableView(out_fc, view)
            arcpy.conversion.TableToTable(view, out_folder, os.path.basename(out_csv))
            arcpy.AddMessage("✓ CSV export complete.")

        arcpy.AddMessage("Done.")
        return
