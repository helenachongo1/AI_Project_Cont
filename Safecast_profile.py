import pandas as pd
import os
import time
from collections import defaultdict

# ============================================================
# CONFIGURATION
# ============================================================

FILE_PATH = r"E:\Android\measurements\measurements-out.csv"

CHUNK_SIZE = 100_000

# Output files
DEVICE_STATS_FILE = "safecast_device_stats.csv"
UNIT_STATS_FILE = "safecast_unit_stats.csv"
DATE_STATS_FILE = "safecast_date_stats.csv"
LOCATION_STATS_FILE = "safecast_location_stats.csv"


# ============================================================
# COLUMNS WE NEED
# ============================================================

USECOLS = [
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


# ============================================================
# STATISTICS CONTAINERS
# ============================================================

device_stats = defaultdict(lambda: {
    "rows": 0,
    "valid_value": 0,
    "min_value": float("inf"),
    "max_value": float("-inf"),
    "sum_value": 0.0,
    "units": set(),
    "min_time": None,
    "max_time": None
})

unit_stats = defaultdict(lambda: {
    "rows": 0,
    "valid_value": 0,
    "min_value": float("inf"),
    "max_value": float("-inf"),
    "sum_value": 0.0,
    "min_time": None,
    "max_time": None
})

date_stats = defaultdict(lambda: {
    "rows": 0,
    "valid_value": 0
})

location_stats = defaultdict(lambda: {
    "rows": 0,
    "valid_value": 0
})


# ============================================================
# GLOBAL STATISTICS
# ============================================================

total_rows = 0
valid_rows = 0
invalid_rows = 0

global_min = float("inf")
global_max = float("-inf")

first_timestamp = None
last_timestamp = None

start_time = time.time()


# ============================================================
# PROCESS FILE IN CHUNKS
# ============================================================

print("=" * 70)
print("SAFECAST DATASET PROFILING")
print("=" * 70)

print("\nFile:")
print(FILE_PATH)

print("\nChunk size:", CHUNK_SIZE)
print("\nStarting scan...\n")


reader = pd.read_csv(
    FILE_PATH,
    usecols=USECOLS,
    chunksize=CHUNK_SIZE,
    low_memory=True
)


for chunk_number, chunk in enumerate(reader, start=1):

    print(
        f"Processing chunk {chunk_number} | "
        f"rows processed: {total_rows:,}"
    )

    # --------------------------------------------------------
    # Timestamp
    # --------------------------------------------------------

    chunk["Captured Time"] = pd.to_datetime(
        chunk["Captured Time"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Numeric radiation value
    # --------------------------------------------------------

    chunk["Value_numeric"] = pd.to_numeric(
        chunk["Value"],
        errors="coerce"
    )

    valid = chunk["Value_numeric"].notna()

    total_rows += len(chunk)
    valid_rows += valid.sum()
    invalid_rows += (~valid).sum()

    # --------------------------------------------------------
    # Global statistics
    # --------------------------------------------------------

    if valid.any():

        values = chunk.loc[valid, "Value_numeric"]

        chunk_min = values.min()
        chunk_max = values.max()

        global_min = min(global_min, chunk_min)
        global_max = max(global_max, chunk_max)

    # --------------------------------------------------------
    # Time statistics
    # --------------------------------------------------------

    valid_times = chunk["Captured Time"].dropna()

    if len(valid_times) > 0:

        current_min = valid_times.min()
        current_max = valid_times.max()

        if first_timestamp is None:
            first_timestamp = current_min
        else:
            first_timestamp = min(
                first_timestamp,
                current_min
            )

        if last_timestamp is None:
            last_timestamp = current_max
        else:
            last_timestamp = max(
                last_timestamp,
                current_max
            )

    # --------------------------------------------------------
    # DATE statistics
    # --------------------------------------------------------

    chunk["Date"] = chunk["Captured Time"].dt.date

    grouped_dates = chunk.groupby("Date")

    for date, group in grouped_dates:

        if pd.isna(date):
            continue

        date_stats[str(date)]["rows"] += len(group)

        date_stats[str(date)]["valid_value"] += (
            group["Value_numeric"].notna().sum()
        )

    # --------------------------------------------------------
    # UNIT statistics
    # --------------------------------------------------------

    for unit, group in chunk.groupby("Unit", dropna=False):

        unit_name = str(unit)

        values = group["Value_numeric"].dropna()

        unit_stats[unit_name]["rows"] += len(group)

        unit_stats[unit_name]["valid_value"] += len(values)

        if len(values) > 0:

            unit_stats[unit_name]["min_value"] = min(
                unit_stats[unit_name]["min_value"],
                values.min()
            )

            unit_stats[unit_name]["max_value"] = max(
                unit_stats[unit_name]["max_value"],
                values.max()
            )

            unit_stats[unit_name]["sum_value"] += values.sum()

        times = group["Captured Time"].dropna()

        if len(times) > 0:

            tmin = times.min()
            tmax = times.max()

            if unit_stats[unit_name]["min_time"] is None:
                unit_stats[unit_name]["min_time"] = tmin
            else:
                unit_stats[unit_name]["min_time"] = min(
                    unit_stats[unit_name]["min_time"],
                    tmin
                )

            if unit_stats[unit_name]["max_time"] is None:
                unit_stats[unit_name]["max_time"] = tmax
            else:
                unit_stats[unit_name]["max_time"] = max(
                    unit_stats[unit_name]["max_time"],
                    tmax
                )

    # --------------------------------------------------------
    # DEVICE statistics
    # --------------------------------------------------------

    for device, group in chunk.groupby(
        "Device ID",
        dropna=False
    ):

        device_name = str(device)

        values = group["Value_numeric"].dropna()

        device_stats[device_name]["rows"] += len(group)

        device_stats[device_name]["valid_value"] += len(values)

        device_stats[device_name]["units"].update(
            group["Unit"].dropna().astype(str).unique()
        )

        if len(values) > 0:

            device_stats[device_name]["min_value"] = min(
                device_stats[device_name]["min_value"],
                values.min()
            )

            device_stats[device_name]["max_value"] = max(
                device_stats[device_name]["max_value"],
                values.max()
            )

            device_stats[device_name]["sum_value"] += values.sum()

        times = group["Captured Time"].dropna()

        if len(times) > 0:

            tmin = times.min()
            tmax = times.max()

            if device_stats[device_name]["min_time"] is None:
                device_stats[device_name]["min_time"] = tmin
            else:
                device_stats[device_name]["min_time"] = min(
                    device_stats[device_name]["min_time"],
                    tmin
                )

            if device_stats[device_name]["max_time"] is None:
                device_stats[device_name]["max_time"] = tmax
            else:
                device_stats[device_name]["max_time"] = max(
                    device_stats[device_name]["max_time"],
                    tmax
                )

    # --------------------------------------------------------
    # LOCATION statistics
    # --------------------------------------------------------

    for location, group in chunk.groupby(
        "Location Name",
        dropna=False
    ):

        location_name = str(location)

        location_stats[location_name]["rows"] += len(group)

        location_stats[location_name]["valid_value"] += (
            group["Value_numeric"].notna().sum()
        )


# ============================================================
# CONVERT DEVICE STATISTICS
# ============================================================

device_records = []

for device, stats in device_stats.items():

    if stats["rows"] == 0:
        continue

    if stats["min_value"] == float("inf"):
        min_value = None
    else:
        min_value = stats["min_value"]

    if stats["max_value"] == float("-inf"):
        max_value = None
    else:
        max_value = stats["max_value"]

    device_records.append({
        "Device ID": device,
        "Rows": stats["rows"],
        "Valid Values": stats["valid_value"],
        "Valid Percentage":
            100 * stats["valid_value"] / stats["rows"],
        "Min Value": min_value,
        "Max Value": max_value,
        "Units": ", ".join(sorted(stats["units"])),
        "Start Time": stats["min_time"],
        "End Time": stats["max_time"]
    })


device_df = pd.DataFrame(device_records)

device_df = device_df.sort_values(
    "Rows",
    ascending=False
)

device_df.to_csv(
    DEVICE_STATS_FILE,
    index=False
)


# ============================================================
# UNIT STATISTICS
# ============================================================

unit_records = []

for unit, stats in unit_stats.items():

    if stats["min_value"] == float("inf"):
        min_value = None
    else:
        min_value = stats["min_value"]

    if stats["max_value"] == float("-inf"):
        max_value = None
    else:
        max_value = stats["max_value"]

    unit_records.append({
        "Unit": unit,
        "Rows": stats["rows"],
        "Valid Values": stats["valid_value"],
        "Valid Percentage":
            100 * stats["valid_value"] / stats["rows"],
        "Min Value": min_value,
        "Max Value": max_value,
        "Start Time": stats["min_time"],
        "End Time": stats["max_time"]
    })


unit_df = pd.DataFrame(unit_records)

unit_df = unit_df.sort_values(
    "Rows",
    ascending=False
)

unit_df.to_csv(
    UNIT_STATS_FILE,
    index=False
)


# ============================================================
# DATE STATISTICS
# ============================================================

date_df = pd.DataFrame([
    {
        "Date": date,
        "Rows": stats["rows"],
        "Valid Values": stats["valid_value"]
    }
    for date, stats in date_stats.items()
])

date_df = date_df.sort_values("Date")

date_df.to_csv(
    DATE_STATS_FILE,
    index=False
)


# ============================================================
# LOCATION STATISTICS
# ============================================================

location_df = pd.DataFrame([
    {
        "Location": location,
        "Rows": stats["rows"],
        "Valid Values": stats["valid_value"]
    }
    for location, stats in location_stats.items()
])

location_df = location_df.sort_values(
    "Rows",
    ascending=False
)

location_df.to_csv(
    LOCATION_STATS_FILE,
    index=False
)


# ============================================================
# FINAL REPORT
# ============================================================

elapsed = time.time() - start_time

print("\n")
print("=" * 70)
print("SCAN COMPLETE")
print("=" * 70)

print(f"\nTotal rows:        {total_rows:,}")
print(f"Valid values:      {valid_rows:,}")
print(f"Invalid values:    {invalid_rows:,}")

if total_rows > 0:
    print(
        f"Valid percentage:  "
        f"{100 * valid_rows / total_rows:.2f}%"
    )

print(f"\nGlobal minimum:    {global_min}")
print(f"Global maximum:    {global_max}")

print(f"\nFirst timestamp:   {first_timestamp}")
print(f"Last timestamp:    {last_timestamp}")

print(f"\nNumber of devices: {len(device_df):,}")
print(f"Number of units:   {len(unit_df):,}")
print(f"Number of dates:   {len(date_df):,}")
print(f"Locations:         {len(location_df):,}")

print(f"\nProcessing time:    {elapsed / 60:.2f} minutes")

print("\nOutput files:")
print(" -", DEVICE_STATS_FILE)
print(" -", UNIT_STATS_FILE)
print(" -", DATE_STATS_FILE)
print(" -", LOCATION_STATS_FILE)

print("\nTop 20 devices:")
print(device_df.head(20).to_string(index=False))

print("\nUnits:")
print(unit_df.to_string(index=False))

print("\nTop 20 locations:")
print(location_df.head(20).to_string(index=False))

print("\nDone.")