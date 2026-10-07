from pathlib import Path

SAFECAST_DIR = Path(r"E:\Android\measurements")

#print("Exists:", SAFECAST_DIR.exists())
#print("Location:", SAFECAST_DIR)

#for item in SAFECAST_DIR.iterdir():
    ##print(item)
    
import pandas as pd

file_path = r"E:\Android\measurements\measurements-out.csv"

df_sample = pd.read_csv(file_path, nrows=10)

#print(df_sample)
#print(df_sample.columns.tolist())

import pandas as pd

file_path = r"E:\Android\measurements\measurements-out.csv"

columns = [
    "Captured Time",
    "Latitude",
    "Longitude",
    "Value",
    "Unit",
    "Location Name",
    "Device ID",
    "Height",
    "Surface",
    "Radiation"
]

chunk_size = 100_000

for chunk in pd.read_csv(
    file_path,
    usecols=columns,
    chunksize=chunk_size,
    low_memory=True
):
    print("\nFirst chunk:")
    print(chunk.head())

    print("\nShape:")
    print(chunk.shape)

    print("\nUnits:")
    print(chunk["Unit"].value_counts(dropna=False).head(20))

    print("\nRadiation:")
    print(chunk["Radiation"].value_counts(dropna=False).head(20))

    print("\nMissing values:")
    print(chunk.isna().sum())

    break
