# Multidisciplinary Urban Capstone Project - Toronto Waterfront Marathon Team (2023/24)

## Marathon Routes GIS Evaluation

This repository contains the code and data for the GIS route evaluatin for the Toronto Waterfront Marathon. The script and model created are used specifically to analyse, evaluate and rank a test route against the 2023 baseline route based on several metrics, such as coverage of subway stops and places of interests, using GIS methods. The scripts make use of ArcPy, and require an ArcGIS Pro environment to run. The work is done as part of the Multidisciplinary Urban Capstone Project at the University of Toronto, by the Toronto Waterfront Marathon Team (2023/24), in collaboration with Canada Running Series and Tata Consultancy Services.

## Instructions

There are 3 scripts in the Scripts folder, each with its own purposes and functions. Some of the scripts require an active ArcGIS Pro environment to run, so you will need the program installed in your environment. The easiest way to run these scripts is to use the propy.bat script in the Python Scripts folder of the ArcGIS Pro program file, which will activate an active condo environment to execute ArcGIS Python functions. Simply navigate to the Scripts folder in ArcGIS Pro program file (the same directory as propy.bat), then add .\propy.bat in front of the execution commands (i.e. `.\propy.bat <location_to_python_script> <arguments_to_the_python_script>`).

Here are the descriptions and instructions for each script defined:

**Model.py**:

This python file contains the actual GIS model used to evaluate a route, which is defined in the Model function. There are also two other helper functions, namely GetMetrics, which returns all the metrics used in the model and GetConnectedRouteVersionFilePath, which returns the file path, if any, of the connected (closed) route version of a route file. The latter function makes use of `RouteToConnectedRouteMapping.json` file to find the connected (closed) route file for a given shp file route. Therefore, the json file should be manually updated with the correct mapping if anything is updated or when new routes are added.

Run this script if you want to evaluate and compare a route against the 2023 baseline route. The script takes in 4 arguments:
- Route: the file path to the shapefile of the route you want to evaluate against the baseline
- Buffer Size: how big the buffer is for the route for GIS evaluation purpose
- Buffer Size Unit: the unit of the give buffer size above
- Show Chart Boolean: whether you want to produce a chart for the percentage difference in performance against baseline route

This script needs to be run under ArcGIS Pro environment. Read the docstring in the python file for example and detailed usage. Make sure to update the `rootFolder` variable in the script to the directory of this project in your local environment.

**Runner.py**:

This python script contains a function to run the GIS evaluation model as defined in `Model.py` on a list of routes. The list of routes should be provided in the `RoutesPaths.txt`. It returns the raw result from the GIS evaluation for each defined metrics in the model and export it to a csv file. See `Results.csv` for a sample of the return data.

Run this script if you want a simple and easy way to evaluate a list of routes using the GIS model. Since it makes use of `Model.py`, it needs to be run under ArcGIS Pro environment. Read the docstring in the python file for example and detailed usage. Make sure to update the `rootFolder` variable in the script to the directory of this project in your local environment.



Sinc this script makes

## Data Sources

- Places of Interests & Toronto Attractions: https://open.toronto.ca/dataset/places-of-interest-and-toronto-attractions/
- TTC Subway Routes & Stops: https://open.toronto.ca/dataset/ttc-routes-and-schedules/
- Toronto Zoning By-law (Commercial, Residential & Mixed): https://open.toronto.ca/dataset/zoning-by-law/
- Above average car intersections: derived and filtered from https://open.toronto.ca/dataset/traffic-volumes-at-intersections-for-all-modes/
- Business Improvement Areas: https://open.toronto.ca/dataset/business-improvement-areas/
- Property Boundary: https://open.toronto.ca/dataset/property-boundaries/

All marathon route data sources are either created by the team or provided by Canada Running Series/Tata Consultancy Services.
