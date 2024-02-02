"""
GIS Script for Toronto Waterfront Marathon Route Analysis to be used in ArcGIS
Pro environment.

This script is created by The Toronto Waterfront Marathon (TWM) team to analyse
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
        RouteBuffer = "C:\\Users\\14168\\Documents\\ArcGIS\\Projects\\TWM\\TWM.gdb\\RouteBuffer"
        # if the buffer already exists, delete it
        if arcpy.Exists(RouteBuffer):
            print("File with conflicting name found, deleting existing RouteBuffer file.")
            arcpy.Delete_management(RouteBuffer)

        arcpy.Buffer_analysis(Route, RouteBuffer, str(BufferSize) + " " + BufferSizeUnit, "FULL", "ROUND", "NONE", "", "PLANAR")

        print("Finished Buffering Route: " + RouteBuffer)
        print("Step 1: Completed in " + str(round((time.time() - startTime), 2)) + " seconds.")

        print("==============================================================")
        print("Step 2: Counting Points of Interest (POI) within the buffer...")

        # Count number of POI feature that intersects with RouteBuffer 
        # using the Select Layer By Location tool
        POIFeature = "C:\\Users\\14168\\Documents\\ArcGIS\\Projects\\TWM\\Data\\Places_of_Interests\\Places of Interest and Attractions - 4326.shp"
        arcpy.SelectLayerByLocation_management(POIFeature, "INTERSECT", RouteBuffer, "", "NEW_SELECTION")
        POIResult = int(arcpy.GetCount_management(POIFeature).getOutput(0))

        print("Finished Counting Points of Interest (POI) within the buffer: " + str(POIResult))
        print("Step 2: Completed in " + str(round((time.time() - startTime), 2)) + " seconds.")

        result["Number of Places of Interests"] = POIResult
    except Exception as e:
        result["Error"] = str(e)
    finally:
        return result


if __name__ == '__main__':
    # script: print out prompts
    print("Model.py running...")

    # keep track of time of execution
    startTime = time.time()
    
    # if no arguments, print usage
    if len(argv) < 2:
        print("Error: Missing arguments")
        print("Usage: Model.py <Route> <BufferSize> <BufferSizeUnit>")
        exit(1)


    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace="C:\\Users\\14168\\Documents\\ArcGIS\\Projects\\TWM\\TWM.gdb", workspace="C:\\Users\\14168\\Documents\\ArcGIS\\Projects\\TWM\\TWM.gdb"):
        result = Model(*argv[1:])

    print("==============================================================")
    print("Finished running Model.py in " + str(round((time.time() - startTime), 2)) + " seconds.")

    if "Error" in result:
        print("\nScript ended with error: " + str(result["Error"]))
        exit(1)
    else:
        print("\nResult:")
        
        # print result
        for key, value in result.items():
            print(f"{key}: {value}")
