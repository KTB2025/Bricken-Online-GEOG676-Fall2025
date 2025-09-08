# -*- coding: utf-8 -*-

import arcpy


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
        self.label = "Graduated Colors Renderer"
        self.description = "Applies a graduated colors renderer to a layer."

    def getParameterInfo(self):
        """Define the tool parameters."""
        param(0) = arcpy.Parameter(
            displayName="Input ArcGIS Pro Prooject Name",
            name="aepxinputname",
            datatype="DEFile",
            parameterType="Required",
            direction="Input")
        
        param(1) = arcpy.Parameter(
            displayName="Layer to Classsify",
            name="ClassificationLayer",
            datatype="DEFeatureLayer",
            parameterType="Required",
            direction="Input")
        
        param(2) = arcpy.Parameter(
            displayName="Output Location",
            name="OutputLocation",   
            datatype="DEWorkspace",        
            parameterType="Required",
            direction="Input")
        
         param(3) = arcpy.Parameter(
            displayName="Output Project Name",
            name="OutProjectName",   
            datatype="GPString",        
            parameterType="Required",
            direction="Input")
            

        param(4) = arcpy.Parameter(
            displayName="Field Name",
            name="fieldname",   
            datatype="GPString",        
            parameterType="Required",
            direction="Input")

        params = [param0, param1, param2, param3, param4]
        return params

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

    def execute(self, parameters, messages):
        """The source code of the tool."""
        
        #Define Progressor Variables
        readTime = 2.5
        start = 0
        max = 100
        step = 33

        #Setup Progressor 
        arcpy.SetProgressor("step", "Starting Process...", start, max, step)
        tme.sleep(readTime)

        arcpy.AddMessage("Validating project file...")

        project = arcpy.mp.ArcGISProProject(parameters[0].valueAsText)

        #Grabs the first instance of a map from the .aprx
        campus = project.listMaps('map')[0] #user navigates to this specified folder

        #Increment Progressor
        arcpy.SetProgressorPosition(start + step)
        arcpy. SetProgressorLabel('Finding your map layer...'))
        time.sleep(readTime)
        arcpy.AddMessage("Finding your map layer...")
        return

    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
