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
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        
        p2 = arcpy.Parameter(
            displayName="Break Count",
            name="BreakCount",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
        
        p3 = arcpy.Parameter(
            displayName="Color Ramp Name",
            name="ColorRampName",
            datatype="GPString",
            parameterType="Optional",
            direction="Input")
        p3.value = "Blue to Red"  #Update with a different default color ramp name 

        p4 = arcpy.Parameter(
            displayName="Output Folder",
            name="OutputFolder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        p5 = arcpy.Parameter(
            displayName="Output Project Name (no .aprx)",
            name="OutputName",
            datatype="GPString",
            parameterType="Required",
            direction="Input")

        params = [p0, p1, p2, p3, p4, p5]
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
        time.sleep(readTime)

        arcpy.AddMessage("Validating project file...")

        project = arcpy.mp.ArcGISProProject(parameters[0].valueAsText)

        #Grabs the first instance of a map from the .aprx
        campus = project.listMaps('map')[0] #user navigates to this specified folder

        #Increment Progressor
        arcpy.SetProgressorPosition(start + step)
        arcpy. SetProgressorLabel('Finding your map layer...')
        time.sleep(readTime)
        arcpy.AddMessage("Finding your map layer...")
        
        #loop through the layers of the map
        for layer in campus.listLayers():
            #check if the layer is a feature layer
            if layer.isFeatureLayer:
                #check the layer's symbology type
                symbology = layer.symbology
                #make sure symbology has a renderer attribute
                if hasattr(symbology, 'renderer'):
                    #check layer name
                    if layer.name == parameters[1].valueAsText: # user will have to input this as an exact string
                        
                        #Increment Progressor
                        arcpy.SetProgressorPosition(start + 2*step)
                        arcpy.SetProgressorLabel('Calculating & Clasifying...')
                        time.sleep(readTime)
                        arcpy.AddMessage("Calculating & Classifying...")

                        #Update the copy's renderer to Graduated Colors Renderer
                        symbology.updateRenderer('GraduatedColorsRenderer')
                        #Tell arcpy which field to base the cholorpleth map off of
                        symbology.renderer.classificationField = "Shape_Area"
                        #Set the number of classes
                        symbology.renderer.breakCount = 5
                        #Set the color ramp
                        symbology.colorRamp = project.listColorRamps("Greens (5 Classes)")[0]
                        #Set the layer's actual symbology equal to the copy's
                        layer.symbology = symbology
                    else:
                        print("NOT STRUCTURES")

        project.saveACopy(os.path.join(parameters[4].valueAsText, parameters[5].valueAsText + ".aprx"))
        arcpy.AddMessage(f"Saved new project to {os.path.join(parameters[4].valueAsText, parameters[5].valueAsText + '.aprx')}")
        return
                    
    def postExecute(self, parameters):
                """This method takes place after outputs are processed and
                added to the display."""
                return
