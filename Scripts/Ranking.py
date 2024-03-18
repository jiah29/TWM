"""
Script to rank routes based on GIS evaluations.

This script is created by the Toronto Waterfront Marathon (TWM) team to analyse
and evaluate marathon routes against various criteria. It is a project conducted
in collaboration with Tata Consultancy Services & Canada Running Series as 
part of the Multidisciplinary Urban Capstone Project (MUCP) at the University
of Toronto.

Example Usage:
.\Ranking.py {CSVFileContainingResultDF}.

Copyright 2024 Toronto Waterfront Marathon Team (MUCP 2023/24)
"""
import pandas as pd
import sys

def Rank(df: pd.DataFrame) -> pd.DataFrame:
    df_T = df.T # transpose dataframe to get metrics in rows, routes as columns
    
    if 'weight' not in df_T.columns:
        df_T['weight'] = 1 # if weights are not specified, give equal weights of 1

    # Seperate weight column and remove from metrics column
    wt = pd.DataFrame(df_T['weight'])
    df_T = df_T.drop(columns = ['weight'])
    
    # Rank route performance in each metric (ascending rank in value)
    ranks = df_T.rank(method = 'max', axis = 1)

    # weight the ranks by multiplying with the weights
    ranks = ranks.mul(wt['weight'], axis = 0)

    # untranspose dataframe
    ranks = ranks.T

    # rename columns to include "Ranks" suffix
    ranks = ranks.rename(columns = lambda x: x + " Weighted Ranks")

    # calculate average rank as score. performance increasing in score
    ranks['Overall Weighted Score'] = ranks.mean(axis = 1)

    return ranks

def ConvertToMaximizingMetrics(df: pd.DataFrame) -> pd.DataFrame:
    toConvert = ["Number of High Traffic Intersections", 
                 "Number of Condomininiums within the Route Coverage Area",
                 "Wide Turns",
                 "Sharp Turns",
                 "Elevation Gain"]

    weight_provided = 'weight' in df.T.columns

    # multiply the metrics that need to be be converted to maximizing metrics by -1
    for metric in toConvert:
        if metric in df.columns:
            if weight_provided:
                # drop the weight column and add it back after converting the metric
                weight = df[metric]["weight"]
                df[metric] = df[metric].drop('weight') * -1
                df.loc["weight", metric] = weight
            else:
                df[metric] = df[metric] * -1
    
    return df

if __name__ == "__main__":
    # refactor to get a list of csv files and combine them into one dataframe
    if len(sys.argv) < 2:
        print("Usage: .\Ranking.py {at least one CSV files containing result dataframe}.")
        exit(1)

    print("Ranking routes based on GIS evaluations...")
    
    # loop through all csv files and combine them into one dataframe
    df = None

    for i in range(1, len(sys.argv)):
        if i == 1:
            df = pd.read_csv(sys.argv[i], index_col=0)
        else:
            df = df.combine_first(pd.read_csv(sys.argv[i], index_col=0))
    
    dfWithAllMaximingMetrics = ConvertToMaximizingMetrics(df)

    finalDf = Rank(dfWithAllMaximingMetrics)

    print("Finished ranking routes. Exporting to CSV...")

    finalDf.to_csv("RankedRoutes.csv")
    
    print("Export completed. Ranking completed successfully!")
