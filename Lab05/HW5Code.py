# =============================================
# TAMU GIS Programming: Homework 05 - Creating a Custom ArcGIS Toolbox Tool
# Author: Kate Bricken
# Date: 09/02/2025
# =============================================

# -*- coding: utf-8 -*-
import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the .pyt file)."""
        self.label = "Toolbox"
        self.alias = ""

        # List of tool classes associated with this toolbox
        self.tools = [tool]

class tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Building Proximity"
        self.description = "Determines which buildings on TAMU's campus are near a targeted building"
        self.canRunInBackground = False
        self.category = "Building Tools"

    # ----------------------------
    # Parameters
    # ----------------------------
    def getParameterInfo(self):
        """Define parameter definitions"""
        param0 = arcpy.Parameter(
            displayName="GDB Folder",
            name="GDBFolder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input"
        )
        param1 = arcpy.Parameter(
            displayName="GDB Name",
            name="GDBName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param2 = arcpy.Parameter(
            displayName="Garage CSV File",
            name="GarageCSVFile",
            datatype="DEFile",
            parameterType="Required",
            direction="Input"
        )
        param3 = arcpy.Parameter(
            displayName="Garage Layer Name",
            name="GarageLayerName",
            datatype="GPString",
            parameterType="Required",
            direction="Input"
        )
        param4 = arcpy.Parameter(
            displayName="CampusGDB",
            name="CampusGDB",
            datatype="DEWorkspace",
            parameterType="Required",
            direction="Input"
        )
        param5 = arcpy.Parameter(
            displayName="Buffer Distance (meters)",
            name="BufferDistance",
            datatype="GPDouble",
            parameterType="Required",
            direction="Input"
        )

        params = [param0, param1, param2, param3, param4, param5]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed. This method is called whenever a parameter
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


        #Create output geodatabase
        arcpy.CreateFileGDB_management(folder_path, gdb_name)

        #Inputs from parameters
        folder_path = parameters[0].valueAsText
        gdb_name = parameters[1].valueAsText
        gdb_path = folder_path + '\\' + gdb_name

        csv_path = parameters[2].valueAsText
        garage_layer_name = parameters[3].valueAsText
        garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)



        #Save inputs into the geodatabase
        input_layer = garages
        arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
        garage_points = gdb_path + '\\' + garage_layer_name


        # Copy Structures from Campus.gdb into the HW05 output gdb
        campus_gdb = parameters[4].valueAsText
        campus_buildings = campus_gdb + '\\Structures'
        buildings = gdb_path + '\\' + 'Buildings'
        arcpy.Copy_management(campus_buildings, buildings)


        #Project garage points to match the Structures file
        spatial_ref = arcpy.Describe(buildings).spatialReference
        arcpy.Project_management(garage_points, gdb_path + '\\Garage_Points_Reprojected', spatial_ref)


        # Buffer garages (use parameter distance, meters)
        buffer_distance = int(parameters[5].value)
        arcpy.Buffer_analysis(gdb_path + '\\Garage_Points_Reprojected', gdb_path + '\\Garage_Points_Buffered', buffer_distance)

        # Intersect buffers with buildings
        arcpy.Intersect_analysis([gdb_path + '\\Garage_Points_Buffered', buildings], gdb_path + '\\Garage_Buildings_Intersection', 'ALL')
        
        # Export table to CSV (drop in the chosen folder)
        arcpy.TableToTable_conversion(gdb_path + '\\Garage_Buildings_Intersection', 'dbf', r'C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025\Lab05', 'nearbyBuildings')

        return None

