
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

def updateMessages(self, parameters):
    """Modify the messages created by internal validation for each tool
    parameter.  This method is called after internal validation."""
    return

def updateMessages(self, parameters):
    for param in parameters:
        if param.name == "buildingNumber":
            # We've found the correct parameter
            buildingNum = param.value
    return

def updateMessages(self, parameters):
    for param in parameters:
        if param.name == "buildingNumber":
            buildingNum = param.value
            campus = r"https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/tree/5bd1938fc56f24fa0dd7c422723a3ce33f3228ed/Lab04/data/Campus.gdb"
            where_clause = "Bldg = '%s'" % buildingNum
            cursor = arcpy.SearchCursor(campus + "/Structures", where_clause=where_clause)
    return   


def updateMessages(self, parameters):
    for param in parameters:
        if param.name == "buildingNumber":
            buildingNum = param.value
            campus = r"https://github.com/KTB2025/Bricken-Online-GEOG676-Fall2025/tree/5bd1938fc56f24fa0dd7c422723a3ce33f3228ed/Lab04/data/Campus.gdb"
            where_clause = "Bldg = '%s'" % buildingNum
            cursor = arcpy.SearchCursor(campus + "/Structures", where_clause=where_clause)
            count = 0
            for row in cursor:
                count += 1
            if count == 0:
                param.setErrorMessage("Cannot find building %s in Structures" % buildingNum)
    return

    # ----------------------------
    # Execute
    # ----------------------------
        def execute(self, parameters, messages):
        """The source code of the tool."""
        # Define our progressor variables
        readTime = 2.5
        start = 0
        maximum = 100
        step = 25

        # Setup the progressor
        arcpy.SetProgressor("step", "Checking building proximity...", start, maximum, step)
        time.sleep(readTime)
        # Add message to the results pane
        arcpy.AddMessage("Checking building proximity...")

        campus = r"D:/DevSource/Tamu/GeoInnovation/_GISProgramming/data/modules/17/Campus.gdb"
        
        # Setup our user input variables
        buildingNumber_input = parameters[0].valueAsText
        bufferSize_input = int(parameters[1].value)

        # Generate our where_clause
        where_clause = "Bldg = '%s'" % buildingNumber_input

        # Check if building exists
        structures = campus + "/Structures"
        cursor = arcpy.SearchCursor(structures, where_clause=where_clause)
        shouldProceed = False

        # Increment the progressor and change the label; add message to the results pane
        arcpy.SetProgressorPosition(start + step)
        arcpy.SetProgressorLabel("Validating building number once more...")
        time.sleep(readTime)
        arcpy.AddMessage("Validating building number once more...")

        for row in cursor:
            if row.getValue("Bldg") == buildingNumber_input:
                shouldProceed = True


        # If we shouldProceed do so
        if shouldProceed:
            # Generate the name for our generated buffer layer
            buildingBuff = "/building_%s_buffed_%s" % (buildingNumber_input, bufferSize_input)
            # Get reference to building
            buildingFeature = arcpy.Select_analysis(structures, campus + "/building_%s" % (buildingNumber_input), where_clause)
            # Buffer the selected building
            arcpy.Buffer_analysis(buildingFeature, campus + buildingBuff, bufferSize_input)
            # Increment the progressor, change label, output message to results pane too
            arcpy.SetProgressorPosition(start + step)
            arcpy.SetProgressorLabel("Buffering....")
            time.sleep(readTime)
            arcpy.AddMessage("Buffering...")
            # Clip the structures to our buffered feature
            arcpy.Clip_analysis(structures, campus + buildingBuff, campus + "/clip_%s" % (buildingNumber_input))
            # Increment the progressor, change label, output message to results pane too
            arcpy.SetProgressorPosition(start + step)
            arcpy.SetProgressorLabel("Clipping....")
            time.sleep(readTime)
            arcpy.AddMessage("Clipping...")
            # Remove the feature class we just created
            arcpy.Delete_management(campus + "/building_%s" % (buildingNumber_input))
            # Increment the progressor, change label, output message to results pane too
            arcpy.SetProgressorPosition(maximum)
            arcpy.SetProgressorLabel("Cleaning up files....")
            time.sleep(readTime)
            arcpy.AddMessage("Cleaning up files...")
        else:
            print("Seems we couldn't find the building you entered")
        return None
