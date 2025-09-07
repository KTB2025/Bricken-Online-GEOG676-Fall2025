Lab06 Tasks: 
• Create a script that can generate either a unique value or graduated color map 
• Turn said script into a toolbox that can be accessed from the Geoprocessing pane in ArcGIS Pro 
• Utilize a progressor inside the tool to inform the user how far along the script is in generating the map 

For this homework assignment, you will need to create a toolbox whose job is to create either a GraduatedColorsRenderer or UniqueValueRenderer based map. Once you have a working toolbox, you will need to add in a progressor who's label tracks what portion of the code is executing. This means the progressor should increment every so often and the label text should change with each progression. 
STEP 1: Generate a map 
1. Create a new ArcGIS Pro project. 
2. Add Campus.gdb and load one feature (GarageParking layer) 
3. Save the project. You’ll notice a toolbox (tbx) file within the project folder and in the Catalog tab. 
 
4. To make an editable toolbox, right click Toolboxes and select New Python Toolbox. Name it after the tool you choose (GraduatedColorsRenderer or UniqueValueRenderer) and you should see it added to your project with a generic tool inside the dropdown. We’re going to change the toolbox to make this tool serve a unique purpose! 
  

STEP 2: Edit your toolbox 
1. At this point I recommend making a copy of your toolbox and saving it as a .py so that you can edit it more easily (with colors). Don’t forget to change it back to a .pyt when you’re done. 
2. Do not edit anything besides the tool name in the first part, otherwise the toolbox will not work. 
 




Your tool’s name
3. Now add your parameters. At minimum you’ll need: a. Input project 
b. Layer to classify (which layer you want to use to generate a color map) 
c. Output location 
d. Output project name 
The first one should look something like this: 
 
Check the link at the bottom of the instructions for your data types. 

4. Next is the progressor within the execute section. a. First, you’ll define progressor variables 
 
b. Set up your progressor with a message of your choice and read in your project file for your input project parameter. 
 
c. Now that the progressor is initialized, set up new labels as it increments through the tool. You’ll need to do this again after your for loop classification. 
 

5. For loop 
a. To classify your layer, you’ll need to set up the following filters: 
 
b. Make sure to add your own labels and decide what field you’ll use for classification. 
c. You can also adjust the break count and color to your personal preference! 

6. Increment your progressor again to end the process. Save a copy of your classification using your last parameters. 
 
STEP 4: Submission 
• Screenshot of your .py code with Terminal window illustrating that it can be run without any errors. 
• Screenshot of your Toolbox in ArcGIS Pro with no error messages popping up after running. 
• Link to your Github page that contains the Python codes (Python script and toolbox) 

Notes: 
• If you’re having difficulty with one (GraduatedColorsRenderer or UniqueValueRenderer) try the other one before giving up. 
• Make sure you’re checking if your toolbox is saved as a .py or a .pyt 
• Keep your workspace clean. If you make copies of the toolbox to try different code, make sure you stay organized and remember where you save everything. 
• Triple check that your data type is correctly listed in your parameters! **** 
• https://pro.arcgis.com/en/pro-app/arcpy/geoprocessing_and_python/defining-parameter-data-types-in-a-python-toolbox.htm 

