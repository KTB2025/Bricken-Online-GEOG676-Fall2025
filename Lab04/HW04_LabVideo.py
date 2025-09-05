import arcpy

# Create a geodatabase 
arcpy.env.workspace = r'C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025\Lab04\codes_env'
folder_path = r'C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025\Lab04'
gdb_name = 'HW04.gdb'
gdb_path = folder_path + '\\' + gdb_name

#Check to see if gdb already exists - if not then create it
if arcpy.Exists(gdb_path):
    arcpy.management.Delete(gdb_path)
if not arcpy.Exists(gdb_path):
    arcpy.management.CreateFileGDB(folder_path, gdb_name)
    print(f"✓ Created geodatabase: {gdb_path}")


#Create a garage feature class
sr_wgs84 = arcpy.SpatialReference(4326)  # WGS84 (matches lon/lat input)
csv_path = r'C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025\Lab04\garages.csv'
garage_layer_name = 'Garage_Points'
garages = arcpy.MakeXYEventLayer_management(csv_path, 'X', 'Y', garage_layer_name)


input_layer = garages
arcpy.FeatureClassToGeodatabase_conversion(input_layer, gdb_path)
garage_points = gdb_path + '\\' + garage_layer_name

# open campus gdb, copy building feature to our gdb
campus = folder_path + '\\' + 'Campus.gdb'
campus_buildings = campus + '\\Structures'
buildings = gdb_path + '\\' + 'Buildings'

arcpy.Copy_management(campus_buildings, buildings)

# Re-Projection
spatial_ref = arcpy.Describe(buildings).spatialReference
arcpy.Project_management(garage_points, gdb_path + '\\Garage_Points_reprojected', spatial_ref)

# buffer the garages
garageBuffered = arcpy.Buffer_analysis(gdb_path + '\\Garage_Points_reprojected',
                                       gdb_path + '\\Garage_Points_buffered', 150)

# Intersect our buffer with the buildings
arcpy.Intersect_analysis([garageBuffered, buildings],
                         gdb_path + '\\Garage_Building_Intersection', 'ALL')

arcpy.TableToTable_conversion(gdb_path + '\\Garage_Building_Intersection.dbf',
                              r'C:\Mac\Home\Documents\FallWorkSpace\Bricken-Online-GEOG676-Fall2025\Lab04', 'nearbyBuildings.csv')
