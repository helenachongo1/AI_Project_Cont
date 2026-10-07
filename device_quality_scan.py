import pandas as pd
import numpy as np
import os
import time
from collections import defaultdict

# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = r"E:\Android\measurements\measurements-out.csv"

OUTPUT_DIR = r"E:\Android\measurements\CARE_dataset"

CHUNK_SIZE = 500_000

# Only analyze CPM radiation records
TARGET_UNIT = "cpm"

# Minimum records required for a candidate device
MIN_RECORDS = 100_000

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 75)
print("CARE++ DEVICE QUALITY SCAN")
print("=" * 75)

start_time = time.time()

# ============================================================
# STORAGE FOR DEVICE STATISTICS
# ============================================================

device_stats = defaultdict(lambda: {
    "rows": 0,
    "valid": 0,
    "invalid": 0,

    "negative": 0,
    "zero": 0,

    "min_value": np.inf,
    "max_value": -np.inf,

    "sum_value": 0.0,
    "sum_squared": 0.0,

    "timestamps": [],
    "locations": set(),

    "values_sample": []
})

chunk_number = 0
total_rows = 0
total_cpm_rows = 0

# ============================================================
# READ CSV IN CHUNKS
# ============================================================

print("\nStarting scan...\n")

reader = pd.read_csv(
    INPUT_FILE,
    chunksize=CHUNK_SIZE,
    low_memory=False
)

for chunk in reader:

    chunk_number += 1
    total_rows += len(chunk)

    if chunk_number % 10 == 0:
        elapsed = time.time() - start_time

        print(
            f"Chunk {chunk_number:,} | "
            f"Rows scanned: {total_rows:,} | "
            f"Time: {elapsed/60:.1f} min"
        )

    # --------------------------------------------------------
    # Standardize column names
    # --------------------------------------------------------

    chunk.columns = chunk.columns.str.strip()

    required_columns = [
        "Captured Time",
        "Latitude",
        "Longitude",
        "Value",
        "Unit",
        "Location Name",
        "Device ID"
    ]

    missing = [
        c for c in required_columns
        if c not in chunk.columns
    ]

    if missing:
        raise ValueError(
            f"Missing columns: {missing}"
        )

    # --------------------------------------------------------
    # Keep CPM only
    # --------------------------------------------------------

    unit = (
        chunk["Unit"]
        .astype(str)
        .str.strip()
        .str.lower()
    )

    mask = unit == TARGET_UNIT

    cpm = chunk.loc[mask].copy()

    total_cpm_rows += len(cpm)

    if len(cpm) == 0:
        continue

    # --------------------------------------------------------
    # Convert timestamp
    # --------------------------------------------------------

    cpm["Captured Time"] = pd.to_datetime(
        cpm["Captured Time"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Numeric radiation value
    # --------------------------------------------------------

    cpm["Value"] = pd.to_numeric(
        cpm["Value"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Device ID
    # --------------------------------------------------------

    cpm["Device ID"] = pd.to_numeric(
        cpm["Device ID"],
        errors="coerce"
    )

    # Remove records without device ID
    cpm = cpm[cpm["Device ID"].notna()]

    if len(cpm) == 0:
        continue

    # --------------------------------------------------------
    # Process each device in this chunk
    # --------------------------------------------------------

    for device_id, df in cpm.groupby("Device ID"):

        device_id = int(device_id)

        stats = device_stats[device_id]

        stats["rows"] += len(df)

        # ----------------------------------------------------
        # Valid numeric values
        # ----------------------------------------------------

        valid_mask = (
            df["Value"].notna() &
            np.isfinite(df["Value"])
        )

        valid = df.loc[valid_mask]

        stats["valid"] += len(valid)
        stats["invalid"] += len(df) - len(valid)

        if len(valid) == 0:
            continue

        values = valid["Value"].to_numpy()

        # ----------------------------------------------------
        # Basic statistics
        # ----------------------------------------------------

        stats["min_value"] = min(
            stats["min_value"],
            float(np.min(values))
        )

        stats["max_value"] = max(
            stats["max_value"],
            float(np.max(values))
        )

        stats["sum_value"] += float(np.sum(values))

        stats["sum_squared"] += float(
            np.sum(values ** 2)
        )

        stats["negative"] += int(
            np.sum(values < 0)
        )

        stats["zero"] += int(
            np.sum(values == 0)
        )

        # ----------------------------------------------------
        # Store timestamps
        # ----------------------------------------------------

        timestamps = valid["Captured Time"].dropna()

        if len(timestamps) > 0:

            # Store timestamps for continuity analysis
            stats["timestamps"].extend(
                timestamps.tolist()
            )

        # ----------------------------------------------------
        # Locations
        # ----------------------------------------------------

        locations = (
            df["Location Name"]
            .dropna()
            .astype(str)
            .str.strip()
        )

        stats["locations"].update(
            locations.unique().tolist()
        )

        # ----------------------------------------------------
        # Store sample of values for IQR
        # ----------------------------------------------------

        # We don't need every value.
        # Keep at most 500 values per chunk/device.
        sample_size = min(500, len(values))

        if sample_size > 0:

            sampled = np.random.choice(
                values,
                size=sample_size,
                replace=False
            )

            stats["values_sample"].extend(
                sampled.tolist()
            )

# ============================================================
# BUILD FINAL DEVICE TABLE
# ============================================================

print("\n")
print("=" * 75)
print("BUILDING DEVICE QUALITY TABLE")
print("=" * 75)

results = []

for device_id, stats in device_stats.items():

    if stats["rows"] < MIN_RECORDS:
        continue

    valid = stats["valid"]

    if valid == 0:
        continue

    # --------------------------------------------------------
    # Sort timestamps
    # --------------------------------------------------------

    timestamps = pd.Series(
        stats["timestamps"]
    ).dropna()

    if len(timestamps) > 1:

        timestamps = (
            pd.to_datetime(timestamps)
            .sort_values()
            .drop_duplicates()
        )

        diffs = (
            timestamps
            .diff()
            .dt.total_seconds()
            .dropna()
        )

        # Remove impossible negative/zero intervals
        diffs = diffs[diffs > 0]

        if len(diffs) > 0:

            median_interval = float(
                diffs.median()
            )

            mean_interval = float(
                diffs.mean()
            )

            p90_interval = float(
                diffs.quantile(0.90)
            )

            p95_interval = float(
                diffs.quantile(0.95)
            )

            gaps_1min = int(
                (diffs > 60).sum()
            )

            gaps_5min = int(
                (diffs > 300).sum()
            )

            gaps_1hour = int(
                (diffs > 3600).sum()
            )

            longest_gap = float(
                diffs.max()
            )

        else:

            median_interval = np.nan
            mean_interval = np.nan
            p90_interval = np.nan
            p95_interval = np.nan
            gaps_1min = 0
            gaps_5min = 0
            gaps_1hour = 0
            longest_gap = np.nan

        start_time_device = timestamps.min()
        end_time_device = timestamps.max()

        days = (
            end_time_device -
            start_time_device
        ).total_seconds() / 86400

        days = max(days, 1)

    else:

        median_interval = np.nan
        mean_interval = np.nan
        p90_interval = np.nan
        p95_interval = np.nan
        gaps_1min = 0
        gaps_5min = 0
        gaps_1hour = 0
        longest_gap = np.nan
        start_time_device = timestamps.min()
        end_time_device = timestamps.max()
        days = np.nan

    # --------------------------------------------------------
    # Value statistics
    # --------------------------------------------------------

    sample = np.array(
        stats["values_sample"],
        dtype=float
    )

    sample = sample[
        np.isfinite(sample)
    ]

    if len(sample) > 0:

        median_value = float(
            np.median(sample)
        )

        q1 = float(
            np.percentile(sample, 25)
        )

        q3 = float(
            np.percentile(sample, 75)
        )

        iqr = q3 - q1

    else:

        median_value = np.nan
        q1 = np.nan
        q3 = np.nan
        iqr = np.nan

    # --------------------------------------------------------
    # Valid percentage
    # --------------------------------------------------------

    valid_percentage = (
        valid /
        stats["rows"]
    ) * 100

    negative_percentage = (
        stats["negative"] /
        valid
    ) * 100

    zero_percentage = (
        stats["zero"] /
        valid
    ) * 100

    # --------------------------------------------------------
    # Preliminary quality score
    # --------------------------------------------------------

    score = 0

    # Data volume
    if valid >= 1_000_000:
        score += 25
    elif valid >= 500_000:
        score += 20
    elif valid >= 100_000:
        score += 15

    # Validity
    if valid_percentage >= 99.9:
        score += 20
    elif valid_percentage >= 99:
        score += 15
    elif valid_percentage >= 95:
        score += 10

    # Sampling interval
    if not np.isnan(median_interval):

        if median_interval <= 60:
            score += 20
        elif median_interval <= 300:
            score += 15
        elif median_interval <= 900:
            score += 10

    # Temporal continuity
    if not np.isnan(p90_interval):

        if p90_interval <= 300:
            score += 15
        elif p90_interval <= 1800:
            score += 10
        elif p90_interval <= 3600:
            score += 5

    # Negative measurements
    if negative_percentage == 0:
        score += 10
    elif negative_percentage < 0.1:
        score += 5

    # Location availability
    if len(stats["locations"]) > 0:
        score += 10

    # --------------------------------------------------------
    # Quality category
    # --------------------------------------------------------

    if score >= 85:
        quality = "Excellent"

    elif score >= 70:
        quality = "Good"

    elif score >= 50:
        quality = "Moderate"

    else:
        quality = "Poor"

    results.append({

        "Device ID": device_id,

        "Rows": stats["rows"],

        "Valid Values": valid,

        "Invalid Values": stats["invalid"],

        "Valid Percentage": valid_percentage,

        "Negative Values": stats["negative"],

        "Negative Percentage": negative_percentage,

        "Zero Values": stats["zero"],

        "Zero Percentage": zero_percentage,

        "Min Value": stats["min_value"],

        "Max Value": stats["max_value"],

        "Median Value": median_value,

        "IQR": iqr,

        "Start Time": start_time_device,

        "End Time": end_time_device,

        "Days Covered": days,

        "Median Interval (sec)": median_interval,

        "Mean Interval (sec)": mean_interval,

        "P90 Interval (sec)": p90_interval,

        "P95 Interval (sec)": p95_interval,

        "Gaps >1min": gaps_1min,

        "Gaps >5min": gaps_5min,

        "Gaps >1hour": gaps_1hour,

        "Longest Gap (sec)": longest_gap,

        "Locations": len(stats["locations"]),

        "Quality Score": score,

        "Quality": quality
    })

# ============================================================
# SAVE RESULTS
# ============================================================

result_df = pd.DataFrame(results)

result_df = result_df.sort_values(
    "Quality Score",
    ascending=False
)

output_file = os.path.join(
    OUTPUT_DIR,
    "device_quality_ranking.csv"
)

result_df.to_csv(
    output_file,
    index=False
)

# ============================================================
# PRINT SUMMARY
# ============================================================

elapsed = time.time() - start_time

print("\n")
print("=" * 75)
print("SCAN COMPLETE")
print("=" * 75)

print(f"Total rows scanned:     {total_rows:,}")
print(f"CPM rows:               {total_cpm_rows:,}")
print(f"Candidate devices:      {len(result_df):,}")
print(f"Processing time:        {elapsed/60:.2f} minutes")

print("\nTOP 20 DEVICES")
print("-" * 75)

display_columns = [
    "Device ID",
    "Rows",
    "Valid Percentage",
    "Days Covered",
    "Median Interval (sec)",
    "P90 Interval (sec)",
    "Gaps >5min",
    "Locations",
    "Quality Score",
    "Quality"
]

print(
    result_df[
        display_columns
    ].head(20).to_string(index=False)
)

print("\nQuality distribution:")
print(
    result_df["Quality"]
    .value_counts()
)

print("\nSaved:")
print(output_file)

print("\n" + "=" * 75)
