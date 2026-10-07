'''
from pathlib import Path
import pandas as pd

PROCESSED_DIR = Path(r"E:\Android\ICT_2025\ICT_26_27\CP\dataset_10_samples\processed")

files = sorted(
    PROCESSED_DIR.glob("*.parquet")
)

print("Number of processed files:", len(files))
print()

for file in files:
    df = pd.read_parquet(file)

    print("=" * 70)
    print(file.name)
    print("=" * 70)

    print("Shape:", df.shape)
    print("SquareIDs:", df["SquareID"].nunique())
    print("Start:", df["Timestamp"].min())
    print("End:", df["Timestamp"].max())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nRows per SquareID:")
    print(df.groupby("SquareID").size().describe())


for file in files:

    df = pd.read_parquet(file)

    print(
        file.name,
        "→",
        df["Timestamp"].min(),
        "to",
        df["Timestamp"].max()
    )
    

dfs = []

for file in files:
    print("Loading:", file.name)
    dfs.append(pd.read_parquet(file))

df = pd.concat(
    dfs,
    ignore_index=True
)

df = df.sort_values(
    ["SquareID", "Timestamp"]
).reset_index(drop=True)

print("Final shape:", df.shape)
print("SquareIDs:", df["SquareID"].nunique())

print("\nRows per SquareID:")
print(df.groupby("SquareID").size().describe())

output_file = PROCESSED_DIR / "milan_2013-11-01_to_2013-11-10.parquet"

df.to_parquet(
    output_file,
    index=False
)

print("Saved:", output_file)'''

'''
import pandas as pd
from pathlib import Path

PROCESSED_DIR = Path(r"E:\Android\ICT_2025\ICT_26_27\CP\dataset_10_samples\processed")

files = sorted(PROCESSED_DIR.glob("*.parquet"))

dfs = [
    pd.read_parquet(file)
    for file in files
]

df = pd.concat(dfs, ignore_index=True)

df = df.sort_values(
    ["SquareID", "Timestamp"]
).reset_index(drop=True)


# ---------------------------------------------------------
# Check timestamp differences within each SquareID
# ---------------------------------------------------------

df["time_diff"] = (
    df.groupby("SquareID")["Timestamp"]
      .diff()
)

print("Timestamp interval distribution:")
print(df["time_diff"].value_counts().head(10))


# ---------------------------------------------------------
# Find gaps larger than 10 minutes
# ---------------------------------------------------------

gaps = df[
    df["time_diff"] > pd.Timedelta(minutes=10)
]

print("\nNumber of gaps larger than 10 minutes:")
print(len(gaps))


# ---------------------------------------------------------
# Show largest gaps
# ---------------------------------------------------------

print("\nLargest gaps:")

print(
    gaps[
        [
            "SquareID",
            "Timestamp",
            "time_diff"
        ]
    ]
    .sort_values("time_diff", ascending=False)
    .head(20)
)

# Make absolutely sure the data is sorted
df = df.sort_values(
    ["SquareID", "Timestamp"]
).reset_index(drop=True)

# Calculate time difference within each SquareID
time_diff = (
    df.groupby("SquareID")["Timestamp"]
      .diff()
)

print("Total rows:", len(df))
print("First observation per SquareID:", time_diff.isna().sum())
print("Non-null time differences:", time_diff.notna().sum())

print("\nTime difference distribution:")
print(time_diff.value_counts(dropna=False).head(15))

print("\nDuplicate SquareID + Timestamp:")
print(
    df.duplicated(
        subset=["SquareID", "Timestamp"]
    ).sum()
)

print("\nGaps greater than 10 minutes:")
print(
    (time_diff > pd.Timedelta(minutes=10)).sum()
)
'''

from pathlib import Path
import pandas as pd

PROCESSED_DIR = Path(r"E:\Android\ICT_2025\ICT_26_27\CP\dataset_10_samples\processed")

'''
# Explicitly select ONLY the 10 daily files
files = sorted(
    PROCESSED_DIR.glob("sms-call-internet-mi-2013-11-*.parquet")
)

print("Number of daily files:", len(files))

for file in files:
    print(file.name)'''
    
# Select ONLY the 10 daily files
files = sorted(
    PROCESSED_DIR.glob("sms-call-internet-mi-2013-11-*.parquet")
)

print("Number of daily files:", len(files))

# ---------------------------------------------------------
# Load the 10 daily files
# ---------------------------------------------------------

daily_dfs = []

for file in files:
    print("Loading:", file.name)
    daily_dfs.append(
        pd.read_parquet(file)
    )

# ---------------------------------------------------------
# Combine
# ---------------------------------------------------------

milan_10day = pd.concat(
    daily_dfs,
    ignore_index=True
)

milan_10day = milan_10day.sort_values(
    ["SquareID", "Timestamp"]
).reset_index(drop=True)

print("\nFinal shape:")
print(milan_10day.shape)

# ---------------------------------------------------------
# Duplicate check
# ---------------------------------------------------------

duplicate_count = milan_10day.duplicated(
    subset=["SquareID", "Timestamp"]
).sum()

print("\nDuplicate SquareID + Timestamp rows:")
print(duplicate_count)

# ---------------------------------------------------------
# Time differences
# ---------------------------------------------------------

time_diff = (
    milan_10day
    .groupby("SquareID")["Timestamp"]
    .diff()
)

print("\nTotal rows:")
print(len(milan_10day))

print("\nFirst observation per SquareID:")
print(time_diff.isna().sum())

print("\nNon-null time differences:")
print(time_diff.notna().sum())

print("\nTime difference distribution:")
print(
    time_diff
    .value_counts(dropna=False)
    .head(15)
)

print("\nGaps greater than 10 minutes:")
print(
    (time_diff > pd.Timedelta(minutes=10)).sum()
)

output_file = (
    PROCESSED_DIR /
    "milan_2013-11-01_to_2013-11-10_clean.parquet"
)

milan_10day.to_parquet(
    output_file,
    index=False
)

print("Saved:", output_file)
print("Shape:", milan_10day.shape)