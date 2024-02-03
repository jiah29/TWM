"""
GIS Script for Toronto Waterfront Marathon Route Analysis to be used in ArcGIS
Pro environment.

This script is created by the Toronto Waterfront Marathon (TWM) team to analyse
and evaluate marathon routes against various criteria. It is a project conducted
in  collaboration with Tata Consultancy Services & Canada Running Series as 
part of the Multidisciplinary Urban Capstone Project (MUCP) at the University
of Toronto.

It is required to run this script under the active conda environment
of ArcGIS Pro. Use C:\Program Files\ArcGIS\Pro\bin\Python\scripts\propy.bat
to activate the conda environment and run the script.

Example Usage (assuming you are in the same directory as propy.bat):
.\propy.bat {LocationToModel.py} {LocationOfRouteFeature.shp} 100 Meters

Copyright 2024 Toronto Waterfront Marathon Team (MUCP 2023/24)
"""
import arcpy
import time
from sys import argv

# Root folder may need to be changed based on the location of the project
rootFolder = "C:\\Users\\14168\\Documents\\ArcGIS\\Projects\\TWM\\"

# This should not be changed if no folder structure is changed
workspaceGDB = rootFolder + "TWM.gdb"
dataFolder = rootFolder + "Data\\"

def Model(Route: str, BufferSize: int, BufferSizeUnit: str) -> dict[str, int]:
    # keep track of result
    result = {}
    # To allow overwriting outputs change overwriteOutput option to True.
    arcpy.env.overwriteOutput = True
    # keep track of time of execution
    startTime = time.time()
    
    try:
        print("==============================================================")
        print("Step 1: Buffering Route...")

        # Create a buffer around the route
        RouteBuffer = rootFolder + "RouteBuffer"
        # if the buffer already exists, delete it
        if arcpy.Exists(RouteBuffer):
            print("File with conflicting name found, deleting existing RouteBuffer file.")
            arcpy.Delete_management(RouteBuffer)

        arcpy.Buffer_analysis(Route, RouteBuffer, str(BufferSize) + " " + BufferSizeUnit, "FULL", "ROUND", "NONE", "", "PLANAR")

        print("Finished Buffering Route: " + RouteBuffer)
        print("Step 1: Completed in " + str(round((time.time() - startTime), 2)) + " s.")

        print("==============================================================")
        print("Step 2: Counting Points of Interest (POI) within the buffer...")

        # Count number of POI feature that intersects with RouteBuffer 
        # using the Select Layer By Location tool
        POIFeature = dataFolder + "Places_of_Interests\\Places of Interest and Attractions - 4326.shp"
        arcpy.SelectLayerByLocation_management(POIFeature, "INTERSECT", RouteBuffer, "", "NEW_SELECTION")

        POIResult = int(arcpy.GetCount_management(POIFeature).getOutput(0))
        result["Number of Places of Interests"] = POIResult

        print("Finished Counting Points of Interest (POI) within the buffer: " + str(POIResult))
        print("Step 2: Completed in " + str(round((time.time() - startTime), 2)) + " s.")

        print("==============================================================")
        print("Step 3: Counting Subway Stations within the buffer...")

        # Count number of Subway Stations feature that intersects with RouteBuffer
        # using the Select Layer By Location tool
        SubwayFeature = dataFolder + "SubwayStops\\TorontoSubwayStations_Ridership.shp"
        arcpy.SelectLayerByLocation_management(SubwayFeature, "INTERSECT", RouteBuffer, "", "NEW_SELECTION")

        SubwayResult = int(arcpy.GetCount_management(SubwayFeature).getOutput(0))
        result["Number of Subway Stations"] = SubwayResult

        print("Finished Counting Subway Stations within the buffer: " + str(SubwayResult))
        print("Step 3: Completed in " + str(round((time.time() - startTime), 2)) + " s.")

        print("==============================================================")
        print("Step 4: Counting High Traffic Intersections within the buffer...")

        # Count number of High Traffic Intersections feature that intersects with RouteBuffer
        # using the Select Layer By Location tool
        HighTrafficFeature = dataFolder + "above_avg_car_intersections\\above_avg_car_intersections.shp"
        arcpy.SelectLayerByLocation_management(HighTrafficFeature, "INTERSECT", RouteBuffer, "", "NEW_SELECTION")

        HighTrafficResult = int(arcpy.GetCount_management(HighTrafficFeature).getOutput(0))
        result["Number of High Traffic Intersections"] = HighTrafficResult

        print("Finished Counting High Traffic Intersections within the buffer: " + str(HighTrafficResult))
        print("Step 4: Completed in " + str(round((time.time() - startTime), 2)) + " s.")


    except Exception as e:
        result["Error"] = str(e)
    finally:
        return result


if __name__ == '__main__':
    # script: print out prompts
    print("Starting analysis...")

    # keep track of time of execution
    startTime = time.time()
    
    # if no arguments, print usage
    if len(argv) < 2:
        print("Error: Missing arguments")
        print("Usage: Model.py <Route> <BufferSize> <BufferSizeUnit>")
        exit(1)


    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=workspaceGDB, workspace=workspaceGDB):
        result = Model(*argv[1:])

    print("==============================================================")
    print("Finished analysis in " + str(round((time.time() - startTime), 2)) + " s.")

    if "Error" in result:
        print("\nAnalysis ended with error: " + str(result["Error"]))
        exit(1)
    else:
        print("\nResult:")
        
        # print result
        for key, value in result.items():
            print(f"{key}: {value}")
