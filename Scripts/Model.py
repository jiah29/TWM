"""
ArcGIS Model Script for Toronto Waterfront Marathon Route Analysis to be used in 
ArcGIS Pro environment.

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
from typing import Optional, List, Dict
import arcpy
import time
import json
from sys import argv

# Root folder may need to be changed based on the location of the project
rootFolder = "C:\\Users\\14168\\Documents\\ArcGIS\\Projects\\TWM\\"

# This should not be changed if no folder structure is changed
workspaceGDB = rootFolder + "TWM.gdb"
dataFolder = rootFolder + "Data\\"

def Model(Route: str, BufferSize: int, BufferSizeUnit: str) -> Dict[str, Optional[int]]:
    # keep track of result
    result = {}
    # to keep track of features which might need to be cleaned up
    intermediateFiles = []
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

        intermediateFiles.append(RouteBuffer)

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

        intermediateFiles.append(POIIntersectionRes)
        
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

        intermediateFiles.append(SubwayIntersectionRes)

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

        intermediateFiles.append(HighTrafficIntersectionRes)

        print("Finished Counting High Traffic Intersections within the buffer: " + str(HighTrafficResult))
        print("Step 4: Completed in " + str(round((time.time() - startTime), 2)) + " s.")

        startTime = time.time()

        # print("==============================================================")
        # print("Step 5: Counting Number of Commercial Zones within the buffer...")

        # CommercialZones = arcpy.SelectLayerByAttribute_management(ZoningFeature, "NEW_SELECTION", "GEN_ZON2 = 201")

        # # Count number of Commercial Zones feature that intersects with RouteBuffer
        # # using the Select Layer By Location tool
        # CommercialIntersectionRes = arcpy.SelectLayerByLocation_management(CommercialZones, "INTERSECT", RouteBuffer, "", "SUBSET_SELECTION")

        # CommercialResult = int(arcpy.GetCount_management(CommercialIntersectionRes).getOutput(0))
        # result["Number of Commercial Zones"] = CommercialResult

        # intermediateFiles.append(CommercialIntersectionRes)
        # intermediateFiles.append(CommercialZones)

        # print("Finished Counting Number of Commercial Zones within the buffer: " + str(CommercialResult))
        # print("Step 5: Completed in " + str(round((time.time() - startTime), 2)) + " s.")

        # startTime = time.time()

        print("==============================================================")
        print("Step 6: Counting Number of Residential Zones within the buffer...")

        ZoningFeature = dataFolder + "Zoning_Area_-_4326\\Zoning Area - 4326.shp"

        # Filter out residential zones from the zoning data using
        # filter by attributes GEN_ZON2 = 0 OR 101
        ResidentialZones = arcpy.SelectLayerByAttribute_management(ZoningFeature, "NEW_SELECTION", "GEN_ZON2 = 0 OR GEN_ZON2 = 101")

        # Count number of Residential Zones feature that intersects with RouteBuffer
        # using the Select Layer By Location tool
        ResidentialIntersectionRes = arcpy.SelectLayerByLocation_management(ResidentialZones, "INTERSECT", RouteBuffer, "", "SUBSET_SELECTION")

        ResidentialResult = int(arcpy.GetCount_management(ResidentialIntersectionRes).getOutput(0))
        result["Number of Residential Zones"] = ResidentialResult

        intermediateFiles.append(ResidentialIntersectionRes)
        intermediateFiles.append(ResidentialZones)

        print("Finished Counting Number of Residential Zones within the buffer: " + str(ResidentialResult))
        print("Step 6: Completed in " + str(round((time.time() - startTime), 2)) + " s.")

        startTime = time.time()

        # print("==============================================================")
        # print("Step 7: Counting Number of Mixed Use Zones (Commercial & Residential) within the buffer...")

        # # Filter out mixed use zones from the zoning data using
        # # filter by attributes GEN_ZON2 = 6 OR 202
        # MixedUseZones = arcpy.SelectLayerByAttribute_management(ZoningFeature, "NEW_SELECTION", "GEN_ZON2 = 6 OR GEN_ZON2 = 202")

        # # Count number of Mixed Use Zones feature that intersects with RouteBuffer
        # # using the Select Layer By Location tool
        # MixedUseIntersectionRes = arcpy.SelectLayerByLocation_management(MixedUseZones, "INTERSECT", RouteBuffer, "", "SUBSET_SELECTION")

        # MixedUseResult = int(arcpy.GetCount_management(MixedUseIntersectionRes).getOutput(0))
        # result["Number of Mixed Use (Commercial & Residential) Zones"] = MixedUseResult

        # intermediateFiles.append(MixedUseIntersectionRes)
        # intermediateFiles.append(MixedUseZones)

        # print("Finished Counting Number of Mixed Use Zones (Commercial & Residential) within the buffer: " + str(MixedUseResult))
        # print("Step 7: Completed in " + str(round((time.time() - startTime), 2)) + " s.")

        # startTime = time.time()

        print("==============================================================")
        print("Step 8: Calculating Areas of Business Improvement Areas within the buffer...")

        # Find overlap using the Count Overlapping features tool
        BIAFeature = dataFolder + "Business Improvement Areas Data - 4326\\Business Improvement Areas Data - 4326.shp"
        BIAOverlapRes = arcpy.CountOverlappingFeatures_analysis([BIAFeature, RouteBuffer], None, 1)

        # Calculate area of overlap using the Calculate Geometry tool
        BIAOverlapAreaRes = arcpy.CalculateGeometryAttributes_management(
            in_features=BIAOverlapRes, 
            geometry_property=[["Area", "AREA_GEODESIC"]], 
            length_unit="",
            area_unit="SQUARE_METERS")
        
        # Select record with attribute COUNT = 2
        ValidBIAOverlapAreaRes = arcpy.SelectLayerByAttribute_management(BIAOverlapAreaRes, "NEW_SELECTION", "COUNT_ = 2")

        # sum the area of the selected records using the Summary Statistics tool
        SummarySumTable = arcpy.analysis.Statistics(ValidBIAOverlapAreaRes, None, [["Area", "SUM"]])
        result["Areas of Business Improvement Areas"] = int(arcpy.da.SearchCursor(SummarySumTable, "SUM_Area").next()[0])

        intermediateFiles.append(BIAOverlapRes)
        intermediateFiles.append(BIAOverlapAreaRes)
        intermediateFiles.append(ValidBIAOverlapAreaRes)
        intermediateFiles.append(SummarySumTable)

        print("Finished Calculating Areas of Business Improvement Areas within the buffer: " + str(result["Areas of Business Improvement Areas"]) + " m2")
        print("Step 8: Completed in " + str(round((time.time() - startTime), 2)) + " s.")

        startTime = time.time()

        print("==============================================================")
        print("Step 9: Counting Number of Condomininiums within the Closed Route")

        # get connected route feature path from json mapping file
        connectedRouteFilePath = GetConnectedRouteVersionFilePath(Route)
        if connectedRouteFilePath == None:
            print("Skipping step 9 as no connected closed route found for current route")
            result["Number of Condomininiums within the Route Coverage Area"] = None
        else:
            ConnectedRouteFile = dataFolder + connectedRouteFilePath

            # convert line feature to polygon
            ConnectedRoutePolygon = rootFolder + "ConnectedRoutePolygon"
            arcpy.FeatureToPolygon_management(ConnectedRouteFile, ConnectedRoutePolygon)

            # Select all the condominiums from property data
            PropertyFeature = dataFolder + "Property Boundaries\\PROPERTY_BOUNDARIES_WGS84.shp"
            Condominiums = arcpy.SelectLayerByAttribute_management(PropertyFeature, "NEW_SELECTION", "F_TYPE = 'CONDO'")

            # Count how many condominiums are inside the connected route polygon
            CondominiumsIntersectionRes = arcpy.SelectLayerByLocation_management(Condominiums, "WITHIN", ConnectedRoutePolygon, "", "SUBSET_SELECTION")
            result["Number of Condomininiums within the Route Coverage Area"] = int(arcpy.GetCount_management(CondominiumsIntersectionRes).getOutput(0))

            intermediateFiles.append(CondominiumsIntersectionRes)
            intermediateFiles.append(Condominiums)
            intermediateFiles.append(ConnectedRoutePolygon)

            print("Finished Counting Number of Condomininiums within the Route Coverage Area: " + str(result["Number of Condomininiums within the Route Coverage Area"]))

        print("Step 9: Completed in " + str(round((time.time() - startTime), 2)) + " s.")
    except Exception as e:
        result["Error"] = str(e)
    finally:
        startTime = time.time()

        print("==============================================================")
        print("Analysis completed. Cleaning up...")

        # remove the created buffer and intermediate files
        for file in intermediateFiles:
            arcpy.Delete_management(file)

        print("Clean up completed in " + str(round((time.time() - startTime), 2)) + " s.")

        return result

def GetConnectedRouteVersionFilePath(Route) -> Optional[str] :
    file = open(rootFolder + 'RouteToConnectedRouteMapping.json')
    mappings = json.load(file)
    routeStrip = Route.split("\\")[-1].strip()
    file.close()
    return mappings.get(routeStrip, None)
    
def GetMetrics() -> List[str]:
    return ["Number of Places of Interests", 
            "Number of Subway Stations", 
            "Number of High Traffic Intersections", 
            # "Number of Commercial Zones", 
            "Number of Residential Zones", 
            # "Number of Mixed Use (Commercial & Residential) Zones", 
            "Areas of Business Improvement Areas",
            "Number of Condomininiums within the Route Coverage Area"
            ]


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

    if not argv[1].endswith(".shp"):
        print("Error: Invalid Route: " + argv[1])
        print("Usage: Route must be a valid .shp file path")
        exit(1)
    
    if (argv[2].isdigit() == False) or (int(argv[2]) <= 0) or (float(argv[2]).is_integer() == False):
        print("Error: Invalid Buffer Size: " + argv[2])
        print("Usage: Buffer Size must be a whole positive number")
        exit(1) 

    if argv[3] != "Meters" and argv[3] != "Kilometers":
        print("Error: Invalid Buffer Size Unit: " + argv[3])
        print("Usage: Buffer Size Unit must be either Meters or Kilometers")
        exit(1)
    
    if argv[4] != "True" and argv[4] != "False":
        print("Error: Invalid show_chart_bool: " + argv[4])
        print("Usage: show_chart_bool must be either True or False")
        exit(1)
    

    # Global Environment settings
    with arcpy.EnvManager(scratchWorkspace=workspaceGDB, workspace=workspaceGDB):
        startTime = time.time()
        # run models twice with both baseline route and custom route
        
        # use baseline model from data and the last 2 arguments 
        print("Doing baseline evaluation...")
        baselineResult = Model(dataFolder + "2023_TWM_Marathon_Route\\2023_TWM_Marathon_Route.shp", *argv[2:4])
        print("Baseline evaluation completed in " + str(round((time.time() - startTime), 2)) + " s.\n")

        # if no error in baseline result, run model with the given arguments
        if "Error" not in baselineResult:
            startTime = time.time()

            # use the model with the given arguments
            print("Doing evaluation with test route...")
            result = Model(*argv[1:4])
            print("Evaluation with test route completed in " + str(round((time.time() - startTime), 2)) + " s.\n")
        else:
            result = baselineResult
            print("Test route evaluation skipped due to error in baseline evaluation.")

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
            if key in baselineResult and value:
                # rename key to make each line shorter and easier to read
                newKey = key.replace("Number of ", "")
                newKey = "\n".join([newKey[i:i+30] for i in range(0, len(newKey), 30)])

                # calculate percentage difference
                baselineResultValue = baselineResult.get(key, None)
                if baselineResultValue:
                    if baselineResultValue == 0:
                        # if baseline is 0, use 0.0001 to avoid division by zero
                        diffResult[newKey] = ((value - baselineResultValue) / 0.0001) * 100
                    else:
                        diffResult[newKey] = ((value - baselineResultValue) / baselineResultValue) * 100
        
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
