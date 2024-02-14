"""
Script to rank routes based on GIS evaluations.

This script is created by the Toronto Waterfront Marathon (TWM) team to analyse
and evaluate marathon routes against various criteria. It is a project conducted
in  collaboration with Tata Consultancy Services & Canada Running Series as 
part of the Multidisciplinary Urban Capstone Project (MUCP) at the University
of Toronto.

Example Usage:
.\Ranking.py {CSVFileContainingResultDF}.

Copyright 2024 Toronto Waterfront Marathon Team (MUCP 2023/24)
"""
import pandas as pd
import sys

def Rank(df: pd.DataFrame) -> pd.DataFrame:
    return df

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: .\Ranking.py {CSVFileContainingResultDF}")
        exit(1)

    print("Ranking routes based on GIS evaluations...")

    df = pd.read_csv(sys.argv[1], index_col=0)
    print(df)
    df = Rank(df)
    
    print("Ranking completed successfully!")