import pandas as pd
import os
import time

CLEAN_FILE = r"E:\Android\measurements\CARE_dataset\safecast_radiation_clean.csv"

print("=" * 70)
print("CARE++ — CLEAN SAFECAST DATASET INSPECTION")
print("=" * 70)

print(f"File exists: {os.path.exists(CLEAN_FILE)}")

if os.path.exists(CLEAN_FILE):
    size_gb = os.path.getsize(CLEAN_FILE) / (1024 ** 3)
    print(f"File size: {size_gb:.2f} GB")

    df = pd.read_csv(
        CLEAN_FILE,
        nrows=10
    )

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 10 rows:")
    print(df)

print("=" * 70)
