import pandas as pd
import numpy as np
import os
import time

# ============================================================
# CARE++ — SAFECAST RADIATION CLEAN DATASET
# ============================================================
#
# Purpose:
# Create a cleaned CPM-only Safecast radiation dataset from
# the original 265+ million-row Safecast CSV.
#
# IMPORTANT:
# This dataset is for ML/data-analysis purposes.
# MAX_CPM is a data-quality filter, NOT a medical safety limit.
#
# Input:
#   Original Safecast CSV
#
# Output:
#   safecast_radiation_clean.csv
#
# ============================================================


# ============================================================
# 1. PATHS
# ============================================================

RAW_FILE = r"E:\Android\measurements\measurements-out.csv"

QUALITY_FILE = (
    r"E:\Android\measurements\CARE_dataset"
    r"\device_quality_ranking.csv"
)

OUTPUT_FILE = (
    r"E:\Android\measurements\CARE_dataset"
    r"\safecast_radiation_clean.csv"
)


# ============================================================
# 2. SETTINGS
# ============================================================

# Number of rows processed at a time.
CHUNK_SIZE = 500_000

# We are using CPM measurements for the first CARE++ dataset.
TARGET_UNIT = "cpm"

# ------------------------------------------------------------
# Data-quality filter
# ------------------------------------------------------------
# This is NOT a radiation safety threshold.
#
# Extremely large CPM values in this Safecast file were observed
# during the initial scan and some are clearly corrupted.
#
# We use this conservative upper bound only to remove obviously
# corrupted measurements.
# ------------------------------------------------------------

MAX_CPM = 100_000


# ------------------------------------------------------------
# Timestamp validity range
# ------------------------------------------------------------
#
# Initial scan showed corrupted timestamps extending to 2143.
# We therefore retain measurements within a realistic historical
# range for this project.
#
# These dates are dataset-selection boundaries, NOT radiation
# safety thresholds.
# ------------------------------------------------------------

MIN_DATE = pd.Timestamp("2010-01-01")

MAX_DATE = pd.Timestamp("2026-08-06 23:59:59")


# ============================================================
# 3. START
# ============================================================

print("=" * 70)
print("CARE++ SAFECAST RADIATION CLEANING")
print("=" * 70)

start_time = time.time()


# ============================================================
# 4. LOAD DEVICE QUALITY RANKING
# ============================================================

print()
print("Loading device quality ranking...")

quality = pd.read_csv(
    QUALITY_FILE
)

print(
    f"Devices in quality ranking: "
    f"{len(quality)}"
)


# ============================================================
# 5. NORMALIZE DEVICE IDs
# ============================================================

quality["Device ID"] = pd.to_numeric(
    quality["Device ID"],
    errors="coerce"
)

quality = quality.dropna(
    subset=["Device ID"]
).copy()

quality["Device ID"] = (
    quality["Device ID"]
    .astype("int64")
)


# ============================================================
# 6. CREATE DEVICE ID SET
# ============================================================

device_ids = set(
    quality["Device ID"]
)

print(
    f"Candidate devices: "
    f"{len(device_ids)}"
)


# ============================================================
# 7. CREATE DEVICE QUALITY LOOKUP
# ============================================================

quality_lookup = quality[
    [
        "Device ID",
        "Quality Score",
        "Quality"
    ]
].drop_duplicates(
    subset=["Device ID"]
).copy()


quality_lookup = quality_lookup.rename(
    columns={
        "Device ID": "device_id",
        "Quality Score": "device_quality_score",
        "Quality": "device_quality"
    }
)


# ============================================================
# 8. COLUMNS TO READ
# ============================================================

usecols = [
    "Captured Time",
    "Latitude",
    "Longitude",
    "Value",
    "Unit",
    "Location Name",
    "Device ID",
    "Height"
]


# ============================================================
# 9. DATA TYPES
# ============================================================

dtype = {
    "Latitude": "float64",
    "Longitude": "float64",
    "Value": "float64",
    "Unit": "string",
    "Location Name": "string",
    "Device ID": "float64",
    "Height": "float64"
}


# ============================================================
# 10. REMOVE EXISTING OUTPUT
# ============================================================

if os.path.exists(OUTPUT_FILE):

    os.remove(OUTPUT_FILE)

    print(
        "Existing output removed."
    )


first_write = True


# ============================================================
# 11. COUNTERS
# ============================================================

total_rows = 0

cpm_rows = 0

candidate_rows = 0

clean_rows = 0

removed_invalid = 0

removed_bad_dates = 0

removed_corrupt = 0

removed_duplicates = 0


# ============================================================
# 12. READ ORIGINAL SAFECAST DATA IN CHUNKS
# ============================================================

print()
print("Starting Safecast processing...")
print()


reader = pd.read_csv(
    RAW_FILE,
    usecols=usecols,
    dtype=dtype,
    chunksize=CHUNK_SIZE,
    low_memory=True
)


# ============================================================
# 13. PROCESS EACH CHUNK
# ============================================================

for chunk_no, df in enumerate(
    reader,
    start=1
):

    # --------------------------------------------------------
    # Count original rows
    # --------------------------------------------------------

    total_rows += len(df)


    # ========================================================
    # NORMALIZE UNIT
    # ========================================================

    df["Unit"] = (
        df["Unit"]
        .astype("string")
        .str.strip()
        .str.lower()
    )


    # ========================================================
    # KEEP CPM ONLY
    # ========================================================

    df = df[
        df["Unit"] == TARGET_UNIT
    ].copy()

    cpm_rows += len(df)


    # ========================================================
    # CONVERT TIMESTAMP
    # ========================================================

    df["timestamp"] = pd.to_datetime(
        df["Captured Time"],
        errors="coerce"
    )


    # ========================================================
    # CONVERT DEVICE ID
    # ========================================================

    df["device_id"] = pd.to_numeric(
        df["Device ID"],
        errors="coerce"
    )


    # ========================================================
    # CONVERT RADIATION VALUE
    # ========================================================

    df["cpm"] = pd.to_numeric(
        df["Value"],
        errors="coerce"
    )


    # ========================================================
    # KEEP ONLY QUALITY-RANKED DEVICES
    # ========================================================

    df = df[
        df["device_id"].isin(device_ids)
    ].copy()

    candidate_rows += len(df)


    # ========================================================
    # REMOVE MISSING CORE VALUES
    # ========================================================

    before = len(df)

    df = df.dropna(
        subset=[
            "timestamp",
            "device_id",
            "cpm"
        ]
    ).copy()

    removed_invalid += (
        before - len(df)
    )


    # ========================================================
    # REMOVE INVALID TIMESTAMPS
    # ========================================================

    before = len(df)

    df = df[
        (df["timestamp"] >= MIN_DATE) &
        (df["timestamp"] <= MAX_DATE)
    ].copy()

    removed_bad_dates += (
        before - len(df)
    )


    # ========================================================
    # REMOVE INVALID / CORRUPTED CPM VALUES
    # ========================================================

    before = len(df)

    df = df[
        (df["cpm"] >= 0) &
        (df["cpm"] <= MAX_CPM)
    ].copy()

    removed_corrupt += (
        before - len(df)
    )


    # ========================================================
    # VALIDATE LATITUDE
    # ========================================================

    invalid_latitude = ~df[
        "Latitude"
    ].between(
        -90,
        90
    )

    df.loc[
        invalid_latitude,
        "Latitude"
    ] = np.nan


    # ========================================================
    # VALIDATE LONGITUDE
    # ========================================================

    invalid_longitude = ~df[
        "Longitude"
    ].between(
        -180,
        180
    )

    df.loc[
        invalid_longitude,
        "Longitude"
    ] = np.nan


    # ========================================================
    # RENAME COLUMNS
    # ========================================================

    df = df[
        [
            "timestamp",
            "device_id",
            "Latitude",
            "Longitude",
            "Location Name",
            "cpm",
            "Height"
        ]
    ].copy()


    df = df.rename(
        columns={
            "Latitude": "latitude",
            "Longitude": "longitude",
            "Location Name": "location_name",
            "Height": "height"
        }
    )


    # ========================================================
    # REMOVE EXACT DUPLICATES WITHIN CHUNK
    # ========================================================

    before = len(df)

    df = df.drop_duplicates(
        subset=[
            "device_id",
            "timestamp",
            "latitude",
            "longitude",
            "cpm"
        ]
    ).copy()

    removed_duplicates += (
        before - len(df)
    )


    # ========================================================
    # ADD DEVICE QUALITY INFORMATION
    # ========================================================

    df = df.merge(
        quality_lookup,
        on="device_id",
        how="left"
    )


    # ========================================================
    # SORT CURRENT CHUNK
    # ========================================================

    df = df.sort_values(
        [
            "device_id",
            "timestamp"
        ]
    ).copy()


    # ========================================================
    # CREATE BASIC QUALITY FLAG
    # ========================================================

    df["quality_flag"] = "valid"


    # --------------------------------------------------------
    # Missing location
    # --------------------------------------------------------

    missing_location = (
        df["latitude"].isna() |
        df["longitude"].isna()
    )


    df.loc[
        missing_location,
        "quality_flag"
    ] = "missing_location"


    # ========================================================
    # FINAL COLUMN ORDER
    # ========================================================

    columns = [
        "timestamp",
        "device_id",
        "latitude",
        "longitude",
        "location_name",
        "cpm",
        "height",
        "device_quality_score",
        "device_quality",
        "quality_flag"
    ]


    df = df[
        columns
    ]


    # ========================================================
    # WRITE CLEAN CHUNK
    # ========================================================

    if len(df) > 0:

        df.to_csv(
            OUTPUT_FILE,
            mode=(
                "w"
                if first_write
                else "a"
            ),
            header=first_write,
            index=False
        )

        first_write = False

        clean_rows += len(df)


    # ========================================================
    # PROGRESS REPORT
    # ========================================================

    if chunk_no % 10 == 0:

        elapsed = (
            time.time() -
            start_time
        ) / 60

        print(
            f"Chunk {chunk_no:4d} | "
            f"Rows scanned: {total_rows:,} | "
            f"CPM: {cpm_rows:,} | "
            f"Candidates: {candidate_rows:,} | "
            f"Clean: {clean_rows:,} | "
            f"Time: {elapsed:.1f} min"
        )


# ============================================================
# 14. FINAL SUMMARY
# ============================================================

elapsed = (
    time.time() -
    start_time
) / 60


print()
print("=" * 70)
print("CLEANING COMPLETE")
print("=" * 70)

print(
    f"Total rows scanned:       "
    f"{total_rows:,}"
)

print(
    f"CPM rows:                 "
    f"{cpm_rows:,}"
)

print(
    f"Candidate-device rows:    "
    f"{candidate_rows:,}"
)

print(
    f"Clean radiation rows:     "
    f"{clean_rows:,}"
)

print()

print(
    f"Invalid removed:          "
    f"{removed_invalid:,}"
)

print(
    f"Bad timestamps removed:   "
    f"{removed_bad_dates:,}"
)

print(
    f"Corrupt CPM removed:      "
    f"{removed_corrupt:,}"
)

print(
    f"Duplicates removed:       "
    f"{removed_duplicates:,}"
)

print()

print(
    f"Processing time:          "
    f"{elapsed:.2f} minutes"
)

print()

print(
    "Output:"
)

print(
    OUTPUT_FILE
)

print("=" * 70)