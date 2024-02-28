"""
GIS Runner Script to run the model and generate the output for multiple routes.

This script is created by the Toronto Waterfront Marathon (TWM) team to analyse
and evaluate marathon routes against various criteria. It is a project conducted
in  collaboration with Tata Consultancy Services & Canada Running Series as 
part of the Multidisciplinary Urban Capstone Project (MUCP) at the University
of Toronto.

It is required to run this script under the active conda environment
of ArcGIS Pro. Use C:\Program Files\ArcGIS\Pro\bin\Python\scripts\propy.bat
to activate the conda environment and run the script.

Example Usage (assuming you are in the same directory as propy.bat):
.\propy.bat {LocationToRunner.py}. Then, follow the instructions in the console 
to run the script.

Copyright 2024 Toronto Waterfront Marathon Team (MUCP 2023/24)
"""
from Model import Model, GetMetrics
import pandas as pd
import time

# Root folder may need to be changed based on the location of the project
rootFolder = "C:\\Users\\14168\\Documents\\ArcGIS\\Projects\\TWM\\"

def RunModelOnRoutesFromFile() -> pd.DataFrame:
    routes = []

    # read test routes from TestRoutesPaths.txt, skipping the first line
    with open(rootFolder + "RoutesPaths.txt", "r") as file:
        for line in file.readlines()[1:]:
            # only add if file ends with .shp
            if line.strip().endswith(".shp"):
                routeName = line.split(",")[0]
                routePath = rootFolder + "Data\\" + line.split(",")[1]
                routes.append((routeName, routePath))
    print(len(routes), "routes registered succesfully from file.")

    # REMOVE ABILITY TO ADD ROUTES MANUALLY DURING SCRIPT EXECUTION
    # more_routes = input("Do you want to add more routes? (y/n): ")
    # while more_routes.lower() == "y":
    #     route_file = input("Enter the shp route file path: ")
    #     # only add if file ends with .shp
    #     if route_file.strip().endswith(".shp"):
    #         routes.append(route_file)
    #     else:
    #         print("Invalid file path. Please enter a valid .shp file path.")
    #     more_routes = input("Do you want to add more routes? (y/n): ")

    # print("Total routes to be processed: ", len(routes))

    if len(routes) == 0:
        print("No routes to process. Exiting...")
        exit(0)
    
    # ask the user for buffer size
    buffer_size_unit = input("Enter the buffer size units (m or km): ")
    while buffer_size_unit.lower() not in ["m", "km"]:
        print("Invalid buffer size units. Please enter either m or km.")
        buffer_size_unit = input("Enter the buffer size units (m or km): ")
    
    # ask the user for the buffer distance positive whole number
    buffer_size = input("Enter the buffer distance (whole positive number): ")
    while (not buffer_size.isdigit()) or (int(buffer_size) <= 0) or (not float(buffer_size).is_integer()):
        print("Invalid buffer distance. Please enter a valid positive whole number.")
        buffer_size = input("Enter the buffer distance (whole positive number): ")

    # convert buffer size to appropriate units
    if buffer_size_unit.lower() == "m":
        buffer_size_unit = "Meters"
    else:
        buffer_size_unit = "Kilometers"

    list_of_metrics = GetMetrics()
    results = {}
    for metric in list_of_metrics:
        results[metric] = []
    
    # run Model.py for each route
    for route_name, route in routes:
        print(f"\nRunning Model.py for {route_name}...")
        result = Model(route, int(buffer_size), buffer_size_unit)
        if "Error" in result:
            print("Error running Model.py for", route)
            print(result["Error"])
            exit(1)
        else:
            for metric in list_of_metrics:
                res = result.get(metric, None)
                results[metric].append(res)

    print("\nFinished running Model.py for all routes.")  

    # return a 2d dataframe representation of the results
    df = pd.DataFrame(results, index=[route[0] for route in routes])
    df.index.name = "Route"

    return df


if __name__ == "__main__":
    print("Starting script...")
    startTime = time.time()

    result_df = RunModelOnRoutesFromFile()

    # save the results to a csv file
    print("Saving results to Results.csv...")
    result_df.to_csv(rootFolder + "Results.csv")
    print("Results saved to Results.csv")

    endTime = time.time()
    print("Script ended in", round(endTime - startTime, 2), "s")
