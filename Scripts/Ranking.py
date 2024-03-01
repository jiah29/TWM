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

    # Add back the weights 
    ranks = pd.merge(ranks.reset_index(), wt.reset_index(), on = 'index')

    # Weight the ranks
    for col in ranks.columns:
         if col != 'weight':
             ranks[col] = ranks[col] * ranks['weight'].astype(int)

    ranks = ranks.rename(columns = {'index': 'Route'}).set_index('Route').drop(columns = 'weight').T.add_suffix(' Ranks') # untranspose dataframe

    ranks['Score'] = ranks.mean(axis = 1) # calculate average rank as score. performance increasing in score
    
    return ranks

def ConvertToMaximizingMetrics(df: pd.DataFrame) -> pd.DataFrame:
    toConvert = ["Number of High Traffic Intersections"]

    # multiply the metrics that need to be be converted to maximizing metrics by -1
    df[toConvert] = df[toConvert].apply(lambda x: -x)
    
    return df

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: .\Ranking.py {CSVFileContainingResultDF}")
        exit(1)

    print("Ranking routes based on GIS evaluations...")

    df = pd.read_csv(sys.argv[1], index_col=0)
    dfWithAllMaximingMetrics = ConvertToMaximizingMetrics(df)
    finalDf = Rank(dfWithAllMaximingMetrics)

    print("Finished ranking routes. Exporting to CSV...")

    finalDf.to_csv("RankedRoutes.csv")
    
    print("Export completed. Ranking completed successfully!")
