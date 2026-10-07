import os
import glob
import time
from collections import defaultdict

import pandas as pd
import pyarrow.parquet as pq


# ============================================================
# CARE++ — SAFE PARQUET INSPECTION
# ============================================================

PARQUET_DIR = (
    r"E:\Android\measurements\CARE_dataset"
    r"\modeling\excellent_temp"
)

OUTPUT_SUMMARY = (
    r"E:\Android\measurements\CARE_dataset"
    r"\modeling\excellent_parquet_inspection.csv"
)

# IMPORTANT:
# Number of rows read at a time from each Parquet file.
# This keeps RAM usage very small.
BATCH_SIZE = 10_000

# Number of rows sampled from the beginning of each file.
SAMPLE_ROWS = 5_000


# ============================================================
# START
# ============================================================

print("=" * 75)
print("CARE++ — SAFE PARQUET INSPECTION")
print("=" * 75)

start_time = time.time()


# ============================================================
# 1. FIND PARQUET FILES
# ============================================================

files = sorted(
    glob.glob(
        os.path.join(
            PARQUET_DIR,
            "part_*.parquet"
        )
    )
)

if not files:

    print()
    print("ERROR: No Parquet files found.")
    print()
    print("Directory:")
    print(PARQUET_DIR)

    raise SystemExit


print()
print(f"Parquet directory:")
print(PARQUET_DIR)

print()
print(f"Parquet files found: {len(files)}")


# ============================================================
# 2. GLOBAL CONTAINERS
# ============================================================

total_rows = 0
total_row_groups = 0
total_size = 0

all_devices = set()

device_rows = defaultdict(int)

global_first_timestamp = None
global_last_timestamp = None

summary_rows = []


# ============================================================
# 3. INSPECT EACH PARQUET FILE
# ============================================================

for file_no, file_path in enumerate(files, start=1):

    print()
    print("-" * 75)
    print(
        f"[{file_no}/{len(files)}] "
        f"{os.path.basename(file_path)}"
    )
    print("-" * 75)

    file_size = os.path.getsize(file_path)

    total_size += file_size

    # --------------------------------------------------------
    # Read metadata ONLY
    # --------------------------------------------------------

    parquet_file = pq.ParquetFile(file_path)

    metadata = parquet_file.metadata

    rows = metadata.num_rows
    row_groups = metadata.num_row_groups

    total_rows += rows
    total_row_groups += row_groups

    print(
        f"Size:       {file_size / (1024 ** 2):.2f} MB"
    )

    print(
        f"Rows:       {rows:,}"
    )

    print(
        f"Row groups: {row_groups:,}"
    )

    print()
    print("Columns:")

    for i in range(metadata.schema.num_columns):

        column = metadata.schema.column(i)

        print(
            f"  {column.name:<25} "
            f"{column.physical_type}"
        )

    # ========================================================
    # 4. READ ONLY A SMALL SAMPLE
    # ========================================================

    print()
    print(
        f"Reading sample of up to {SAMPLE_ROWS:,} rows..."
    )

    sample_table = parquet_file.read_row_groups(
        list(
            range(
                min(
                    row_groups,
                    max(
                        1,
                        SAMPLE_ROWS // max(rows // row_groups, 1)
                    )
                )
            )
        )
    )

    sample_df = sample_table.to_pandas()

    print(
        f"Sample loaded: {len(sample_df):,} rows"
    )

    print()
    print("Sample columns:")

    print(
        sample_df.columns.tolist()
    )

    # --------------------------------------------------------
    # Show first few rows
    # --------------------------------------------------------

    print()
    print("First rows:")

    print(
        sample_df.head(3).to_string(index=False)
    )

    # ========================================================
    # 5. DETERMINE IMPORTANT COLUMNS
    # ========================================================

    columns = set(
        sample_df.columns
    )

    device_column = None

    for candidate in [
        "device_id",
        "Device ID",
        "device"
    ]:

        if candidate in columns:

            device_column = candidate
            break


    timestamp_column = None

    for candidate in [
        "timestamp",
        "Captured Time",
        "captured_time"
    ]:

        if candidate in columns:

            timestamp_column = candidate
            break


    # ========================================================
    # 6. DEVICE INFORMATION FROM SMALL SAMPLE
    # ========================================================

    sample_devices = set()

    if device_column is not None:

        sample_devices = set(
            pd.to_numeric(
                sample_df[device_column],
                errors="coerce"
            )
            .dropna()
            .astype("int64")
            .unique()
        )

        print()
        print(
            f"Devices in sample: "
            f"{len(sample_devices)}"
        )

        print(
            sorted(sample_devices)
        )

        all_devices.update(
            sample_devices
        )


    # ========================================================
    # 7. STREAM THROUGH FILE IN SMALL BATCHES
    # ========================================================

    print()
    print(
        "Scanning device/timestamp information "
        "in small batches..."
    )

    file_devices = set()

    file_first_timestamp = None
    file_last_timestamp = None

    file_null_counts = defaultdict(int)

    batch_number = 0

    for batch in parquet_file.iter_batches(
        batch_size=BATCH_SIZE
    ):

        batch_number += 1

        batch_df = batch.to_pandas()

        # ----------------------------------------------------
        # Device IDs
        # ----------------------------------------------------

        if device_column is not None:

            devices = (
                pd.to_numeric(
                    batch_df[device_column],
                    errors="coerce"
                )
                .dropna()
                .astype("int64")
            )

            if len(devices) > 0:

                unique_devices = devices.unique()

                for device in unique_devices:

                    count = int(
                        (devices == device).sum()
                    )

                    device_rows[int(device)] += count

                file_devices.update(
                    unique_devices.tolist()
                )

                all_devices.update(
                    unique_devices.tolist()
                )

        # ----------------------------------------------------
        # Timestamp
        # ----------------------------------------------------

        if timestamp_column is not None:

            timestamps = pd.to_datetime(
                batch_df[timestamp_column],
                errors="coerce"
            )

            timestamps = timestamps.dropna()

            if len(timestamps) > 0:

                batch_min = timestamps.min()
                batch_max = timestamps.max()

                if (
                    file_first_timestamp is None
                    or batch_min < file_first_timestamp
                ):
                    file_first_timestamp = batch_min

                if (
                    file_last_timestamp is None
                    or batch_max > file_last_timestamp
                ):
                    file_last_timestamp = batch_max

                if (
                    global_first_timestamp is None
                    or batch_min < global_first_timestamp
                ):
                    global_first_timestamp = batch_min

                if (
                    global_last_timestamp is None
                    or batch_max > global_last_timestamp
                ):
                    global_last_timestamp = batch_max

        # ----------------------------------------------------
        # Null counts
        # ----------------------------------------------------

        for column in batch_df.columns:

            file_null_counts[column] += int(
                batch_df[column].isna().sum()
            )

        # ----------------------------------------------------
        # Explicitly release batch
        # ----------------------------------------------------

        del batch_df

    # ========================================================
    # 8. FILE SUMMARY
    # ========================================================

    print()
    print(
        f"Devices in file: {len(file_devices)}"
    )

    print(
        f"First timestamp: {file_first_timestamp}"
    )

    print(
        f"Last timestamp:  {file_last_timestamp}"
    )

    # --------------------------------------------------------
    # Save summary
    # --------------------------------------------------------

    summary_rows.append(
        {
            "file": os.path.basename(file_path),
            "size_mb": round(
                file_size / (1024 ** 2),
                2
            ),
            "rows": rows,
            "row_groups": row_groups,
            "devices": len(file_devices),
            "first_timestamp": file_first_timestamp,
            "last_timestamp": file_last_timestamp
        }
    )


# ============================================================
# 9. SAVE FILE SUMMARY
# ============================================================

summary_df = pd.DataFrame(
    summary_rows
)

summary_df.to_csv(
    OUTPUT_SUMMARY,
    index=False
)


# ============================================================
# 10. FINAL REPORT
# ============================================================

elapsed = (
    time.time() - start_time
) / 60


print()
print("=" * 75)
print("INSPECTION COMPLETE")
print("=" * 75)

print()
print(
    f"Parquet files:       {len(files):,}"
)

print(
    f"Total size:          "
    f"{total_size / (1024 ** 3):.3f} GB"
)

print(
    f"Total rows:          {total_rows:,}"
)

print(
    f"Total row groups:    {total_row_groups:,}"
)

print()
print(
    f"Unique devices:      {len(all_devices)}"
)

print(
    f"Device IDs:"
)

print(
    sorted(all_devices)
)

print()
print(
    f"Global first timestamp:"
)

print(
    global_first_timestamp
)

print()
print(
    f"Global last timestamp:"
)

print(
    global_last_timestamp
)


# ============================================================
# 11. DEVICE ROW COUNTS
# ============================================================

print()
print("=" * 75)
print("DEVICE DISTRIBUTION")
print("=" * 75)

device_summary = pd.DataFrame(
    [
        {
            "device_id": device,
            "rows": count
        }
        for device, count
        in device_rows.items()
    ]
)

device_summary = device_summary.sort_values(
    "rows",
    ascending=False
)

print(
    device_summary.to_string(
        index=False
    )
)


# ============================================================
# 12. EXPECTED EXCELLENT DEVICES
# ============================================================

expected_devices = {
    19,
    63,
    69,
    106,
    107,
    108,
    116,
    204,
    205,
    209,
    216,
    224,
    256,
    4841,
    62007,
    65000,
    65001,
    65002,
    65003,
    65007,
    65109,
    65123,
    65128,
    65132
}

present = (
    expected_devices
    .intersection(all_devices)
)

missing = (
    expected_devices
    .difference(all_devices)
)

unexpected = (
    all_devices
    .difference(expected_devices)
)


print()
print("=" * 75)
print("EXCELLENT DEVICE CHECK")
print("=" * 75)

print()
print(
    f"Expected excellent devices: {len(expected_devices)}"
)

print(
    f"Present:                    {len(present)}"
)

print(
    f"Missing:                    {len(missing)}"
)

print(
    f"Unexpected:                 {len(unexpected)}"
)

print()

if missing:

    print(
        "MISSING DEVICES:"
    )

    print(
        sorted(missing)
    )

else:

    print(
        "All 24 expected excellent devices are present."
    )


if unexpected:

    print()
    print(
        "UNEXPECTED DEVICE IDs:"
    )

    print(
        sorted(unexpected)
    )


# ============================================================
# 13. OUTPUT
# ============================================================

print()
print("=" * 75)
print("OUTPUT")
print("=" * 75)

print()
print(
    "File summary:"
)

print(
    OUTPUT_SUMMARY
)

print()
print(
    f"Processing time: {elapsed:.2f} minutes"
)

print()
print(
    "IMPORTANT:"
)

print(
    "No full Parquet dataset was loaded into RAM."
)

print(
    f"Maximum batch size: {BATCH_SIZE:,} rows."
)

print("=" * 75)