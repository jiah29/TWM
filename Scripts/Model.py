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
.\propy.bat {LocationToModel.py} {LocationOfRouteFeature.shp} 100 Meters True

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

        startTime = time.time()

        print("==============================================================")
        print("Step 2: Counting Points of Interest (POI) within the buffer...")

        # Count number of POI feature that intersects with RouteBuffer 
        # using the Select Layer By Location tool
        POIFeature = dataFolder + "Places_of_Interests\\Places of Interest and Attractions - 4326.shp"
        POIIntersectionRes = arcpy.SelectLayerByLocation_management(POIFeature, "INTERSECT", RouteBuffer, "", "NEW_SELECTION")

        POIResult = int(arcpy.GetCount_management(POIIntersectionRes).getOutput(0))
        result["Number of Places of Interests"] = POIResult

        print("Finished Counting Points of Interest (POI) within the buffer: " + str(POIResult))
        print("Step 2: Completed in " + str(round((time.time() - startTime), 2)) + " s.")

        startTime = time.time()

        print("==============================================================")
        print("Step 3: Counting Subway Stations within the buffer...")

        # Count number of Subway Stations feature that intersects with RouteBuffer
        # using the Select Layer By Location tool
        SubwayFeature = dataFolder + "SubwayStops\\TorontoSubwayStations_Ridership.shp"
        SubwayIntersectionRes = arcpy.SelectLayerByLocation_management(SubwayFeature, "INTERSECT", RouteBuffer, "", "NEW_SELECTION")

        SubwayResult = int(arcpy.GetCount_management(SubwayIntersectionRes).getOutput(0))
        result["Number of Subway Stations"] = SubwayResult

        print("Finished Counting Subway Stations within the buffer: " + str(SubwayResult))
        print("Step 3: Completed in " + str(round((time.time() - startTime), 2)) + " s.")

        startTime = time.time()

        print("==============================================================")
        print("Step 4: Counting High Traffic Intersections within the buffer...")

        # Count number of High Traffic Intersections feature that intersects with RouteBuffer
        # using the Select Layer By Location tool
        HighTrafficFeature = dataFolder + "above_avg_car_intersections\\above_avg_car_intersections.shp"
        HighTrafficIntersectionRes = arcpy.SelectLayerByLocation_management(HighTrafficFeature, "INTERSECT", RouteBuffer, "", "NEW_SELECTION")

        HighTrafficResult = int(arcpy.GetCount_management(HighTrafficIntersectionRes).getOutput(0))
        result["Number of High Traffic Intersections"] = HighTrafficResult

        print("Finished Counting High Traffic Intersections within the buffer: " + str(HighTrafficResult))
        print("Step 4: Completed in " + str(round((time.time() - startTime), 2)) + " s.")

        startTime = time.time()

        print("==============================================================")
        print("Step 5: Counting Number of Commercial Zones within the buffer...")

        # Filter out commercial zones from the zoning data using
        # filter by attributes GEN_ZON2 = 201
        ZoningFeature = dataFolder + "Zoning_Area_-_4326\\Zoning Area - 4326.shp"
        CommercialZones = arcpy.SelectLayerByAttribute_management(ZoningFeature, "NEW_SELECTION", "GEN_ZON2 = 201")

        # Count number of Commercial Zones feature that intersects with RouteBuffer
        # using the Select Layer By Location tool
        CommercialIntersectionRes = arcpy.SelectLayerByLocation_management(CommercialZones, "INTERSECT", RouteBuffer, "", "SUBSET_SELECTION")

        CommercialResult = int(arcpy.GetCount_management(CommercialIntersectionRes).getOutput(0))
        result["Number of Commercial Zones"] = CommercialResult

        print("Finished Counting Number of Commercial Zones within the buffer: " + str(CommercialResult))
        print("Step 5: Completed in " + str(round((time.time() - startTime), 2)) + " s.")

        startTime = time.time()

        print("==============================================================")
        print("Step 6: Counting Number of Residential Zones within the buffer...")

        # Filter out residential zones from the zoning data using
        # filter by attributes GEN_ZON2 = 0 OR 101
        ResidentialZones = arcpy.SelectLayerByAttribute_management(ZoningFeature, "NEW_SELECTION", "GEN_ZON2 = 0 OR GEN_ZON2 = 101")

        # Count number of Residential Zones feature that intersects with RouteBuffer
        # using the Select Layer By Location tool
        ResidentialIntersectionRes = arcpy.SelectLayerByLocation_management(ResidentialZones, "INTERSECT", RouteBuffer, "", "SUBSET_SELECTION")

        ResidentialResult = int(arcpy.GetCount_management(ResidentialIntersectionRes).getOutput(0))
        result["Number of Residential Zones"] = ResidentialResult

        print("Finished Counting Number of Residential Zones within the buffer: " + str(ResidentialResult))
        print("Step 6: Completed in " + str(round((time.time() - startTime), 2)) + " s.")

        startTime = time.time()

        print("==============================================================")
        print("Step 7: Counting Number of Mixed Use Zones (Commercial & Residential) within the buffer...")

        # Filter out mixed use zones from the zoning data using
        # filter by attributes GEN_ZON2 = 6 OR 202
        MixedUseZones = arcpy.SelectLayerByAttribute_management(ZoningFeature, "NEW_SELECTION", "GEN_ZON2 = 6 OR GEN_ZON2 = 202")

        # Count number of Mixed Use Zones feature that intersects with RouteBuffer
        # using the Select Layer By Location tool
        MixedUseIntersectionRes = arcpy.SelectLayerByLocation_management(MixedUseZones, "INTERSECT", RouteBuffer, "", "SUBSET_SELECTION")

        MixedUseResult = int(arcpy.GetCount_management(MixedUseIntersectionRes).getOutput(0))
        result["Number of Mixed Use (Commercial & Residential) Zones"] = MixedUseResult

        print("Finished Counting Number of Mixed Use Zones (Commercial & Residential) within the buffer: " + str(MixedUseResult))
        print("Step 7: Completed in " + str(round((time.time() - startTime), 2)) + " s.")

        startTime = time.time()

        print("==============================================================")
        print("Step 8: Calculating Areas of Business Improvement Areas within the buffer...")

        # Find overlap using the Count Overlapping features tool
        BIAFeature = dataFolder + "Business Improvement Areas Data - 4326\\Business Improvement Areas Data - 4326.shp"
        BIAOverlapRes = arcpy.CountOverlappingFeatures_analysis([BIAFeature, RouteBuffer], "BIAOverlapRes", 1)

        # Calculate area of overlap using the Calculate Geometry tool
        BIAOverlapAreaRes = arcpy.CalculateGeometryAttributes_management(
            in_features=BIAOverlapRes, 
            geometry_property=[["Area_m2", "AREA_GEODESIC"]], 
            length_unit="",
            area_unit="SQUARE_METERS")
        
        # Select record with attribute COUNT = 2
        ValidBIAOverlapAreaRes = arcpy.SelectLayerByAttribute_management(BIAOverlapAreaRes, "NEW_SELECTION", "COUNT_ = 2")

        # sum the area of the selected records using the Summary Statistics tool
        SummarySumTable = arcpy.analysis.Statistics(ValidBIAOverlapAreaRes, "SummarySumTable", [["Area_m2", "SUM"]])
        result["Areas of Business Improvement Areas"] = int(arcpy.da.SearchCursor(SummarySumTable, "SUM_Area_m2").next()[0])

        print("Finished Calculating Areas of Business Improvement Areas within the buffer: " + str(result["Areas of Business Improvement Areas"]) + " m2")
        print("Step 8: Completed in " + str(round((time.time() - startTime), 2)) + " s.")

        print("==============================================================")
        print("Analysis completed. Cleaning up...")

        # remove the created buffer and intermediate files
        arcpy.Delete_management(RouteBuffer)
        arcpy.Delete_management(POIIntersectionRes)
        arcpy.Delete_management(SubwayIntersectionRes)
        arcpy.Delete_management(HighTrafficIntersectionRes)
        arcpy.Delete_management(CommercialIntersectionRes)
        arcpy.Delete_management(CommercialZones)
        arcpy.Delete_management(ResidentialIntersectionRes)
        arcpy.Delete_management(ResidentialZones)
        arcpy.Delete_management(MixedUseZones)
        arcpy.Delete_management(MixedUseIntersectionRes)
        arcpy.Delete_management(BIAOverlapRes)
        arcpy.Delete_management(BIAOverlapAreaRes)
        arcpy.Delete_management(ValidBIAOverlapAreaRes)
        arcpy.Delete_management(SummarySumTable)

        print("Clean up completed in " + str(round((time.time() - startTime), 2)) + " s.")

    except Exception as e:
        result["Error"] = str(e)
    finally:
        return result


if __name__ == '__main__':
    # script: print out prompts
    print("Starting script...\n")

    scriptStartTime = time.time()
    
    # if not enough arguments, print usage
    if len(argv) < 5:
        print("Error: Missing arguments")
        print("Usage: Model.py <Route> <BufferSize> <BufferSizeUnit> <show_chart_bool>")
        print("Example 1: Model.py C:\\Users\\14168\\Documents\\ArcGIS\\Projects\\TWM\\Data\\2023_TWM_Marathon_Route\\2023_TWM_Marathon_Route.shp 100 Meters True")
        print("Example 2: Model.py C:\\Users\\14168\\Documents\\ArcGIS\\Projects\\TWM\\Data\\2023_TWM_Marathon_Route\\2023_TWM_Marathon_Route.shp 1 Kilometers False")
        exit(1)


    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=workspaceGDB, workspace=workspaceGDB):
        startTime = time.time()
        # run models twice with both baseline route and custom route
        
        # use baseline model from data and the last 2 arguments 
        print("Doing baseline analysis...")
        baselineResult = Model(dataFolder + "2023_TWM_Marathon_Route\\2023_TWM_Marathon_Route.shp", *argv[2:4])
        print("Baseline analysis completed in " + str(round((time.time() - startTime), 2)) + " s.\n")

        # if no error in baseline result, run model with the given arguments
        if "Error" not in baselineResult:
            startTime = time.time()

            # use the model with the given arguments
            print("Doing analysis with test route...")
            result = Model(*argv[1:4])
            print("Analysis with test route completed in " + str(round((time.time() - startTime), 2)) + " s.\n")

    if "Error" in result:
        print("Script ended in " + str(round((time.time() - scriptStartTime), 2)) + " s. with error:")
        print(result["Error"])
        exit(1)
    else:
        print("Script ended successfully in " + str(round((time.time() - scriptStartTime), 2)) + " s.")

        # print result
        print("\nResult:")
        for key, value in result.items():
            print(f"{key}: {value}")

        # print baseline result
        print("\nBaseline Result:")
        for key, value in baselineResult.items():
            print(f"{key}: {value}")

        # calculate the percentage difference of custom route from baseline
        diffResult = {}
        for key, value in result.items():
            if key in baselineResult:
                newKey = key.replace("Number of ", "")
                newKey = "\n".join([newKey[i:i+30] for i in range(0, len(newKey), 30)])
                if baselineResult[key] == 0:
                    # if baseline is 0, use 0.0001 to avoid division by zero
                    diffResult[newKey] = ((value - baselineResult[key]) / 0.0001) * 100
                else:
                    diffResult[newKey] = ((value - baselineResult[key]) / baselineResult[key]) * 100
        
        if argv[4] == "False":
            exit(0)
        else:
            # plot the difference in a horizontal bar chart
            import matplotlib.pyplot as plt

            plt.barh(range(len(diffResult)), list(diffResult.values()), align='center')
            plt.yticks(range(len(diffResult)), list(diffResult.keys()))
            plt.yticks(fontsize=8, rotation=45)
            plt.xlabel('Percentage Difference')
            plt.title('Test Route Performance from 2023 Baseline')

            # show bar labels inside bar with name of the feature
            for index, value in enumerate(diffResult.values()):
                plt.text(value, index, str(round(value, 2)) + "%", fontsize=8)

            plt.show()

            exit(0)
