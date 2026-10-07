import pandas as pd
import os
import time

# ============================================================
# CARE++ — EXTRACT EXCELLENT SAFECAST DEVICES
# ============================================================

CLEAN_FILE = (
    r"E:\Android\measurements\CARE_dataset"
    r"\safecast_radiation_clean.csv"
)

QUALITY_FILE = (
    r"E:\Android\measurements\CARE_dataset"
    r"\device_quality_ranking.csv"
)

OUTPUT_DIR = (
    r"E:\Android\measurements\CARE_dataset"
    r"\modelling"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "safecast_excellent.parquet"
)

CHUNK_SIZE = 500_000

# ============================================================
# START
# ============================================================

print("=" * 70)
print("CARE++ — EXCELLENT DEVICE EXTRACTION")
print("=" * 70)

start_time = time.time()

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

# ============================================================
# LOAD QUALITY RANKING
# ============================================================

quality = pd.read_csv(
    QUALITY_FILE
)

quality["Device ID"] = pd.to_numeric(
    quality["Device ID"],
    errors="coerce"
)

quality = quality.dropna(
    subset=["Device ID"]
)

quality["Device ID"] = (
    quality["Device ID"]
    .astype("int64")
)

# ------------------------------------------------------------
# Select Excellent devices
# ------------------------------------------------------------

excellent = quality[
    quality["Quality"].astype(str).str.strip().str.lower()
    == "excellent"
].copy()

excellent_ids = set(
    excellent["Device ID"]
)

print(
    f"Excellent devices: {len(excellent_ids)}"
)

print(
    "Device IDs:"
)

print(
    sorted(excellent_ids)
)

# ============================================================
# COLUMNS
# ============================================================

usecols = [
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

# ============================================================
# REMOVE PREVIOUS OUTPUT
# ============================================================

if os.path.exists(OUTPUT_FILE):

    os.remove(OUTPUT_FILE)

    print(
        "\nPrevious output removed."
    )

# ============================================================
# PROCESS CSV IN CHUNKS
# ============================================================

total_rows = 0
selected_rows = 0
chunks_processed = 0

reader = pd.read_csv(
    CLEAN_FILE,
    usecols=usecols,
    chunksize=CHUNK_SIZE,
    low_memory=False
)

# ------------------------------------------------------------
# Because Parquet cannot be safely appended with to_parquet()
# in the same way as CSV, collect temporary chunk files.
# ------------------------------------------------------------

TEMP_DIR = os.path.join(
    OUTPUT_DIR,
    "excellent_temp"
)

os.makedirs(
    TEMP_DIR,
    exist_ok=True
)

# Remove old temporary files

for filename in os.listdir(TEMP_DIR):

    path = os.path.join(
        TEMP_DIR,
        filename
    )

    if os.path.isfile(path):
        os.remove(path)

# ============================================================
# CHUNK PROCESSING
# ============================================================

for chunk_no, df in enumerate(
    reader,
    start=1
):

    chunks_processed += 1

    total_rows += len(df)

    # --------------------------------------------------------
    # Normalize device ID
    # --------------------------------------------------------

    df["device_id"] = pd.to_numeric(
        df["device_id"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Select Excellent devices
    # --------------------------------------------------------

    df = df[
        df["device_id"].isin(excellent_ids)
    ].copy()

    if len(df) == 0:

        if chunk_no % 10 == 0:

            print(
                f"Chunk {chunk_no:4d} | "
                f"Rows scanned: {total_rows:,}"
            )

        continue

    # --------------------------------------------------------
    # Device ID as integer
    # --------------------------------------------------------

    df["device_id"] = (
        df["device_id"]
        .astype("int64")
    )

    # --------------------------------------------------------
    # Timestamp
    # --------------------------------------------------------

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "timestamp",
            "cpm"
        ]
    )

    # --------------------------------------------------------
    # Sort within chunk
    # --------------------------------------------------------

    df = df.sort_values(
        [
            "device_id",
            "timestamp"
        ]
    )

    # --------------------------------------------------------
    # Save temporary parquet
    # --------------------------------------------------------

    temp_file = os.path.join(
        TEMP_DIR,
        f"part_{chunk_no:05d}.parquet"
    )

    df.to_parquet(
        temp_file,
        index=False
    )

    selected_rows += len(df)

    # --------------------------------------------------------
    # Progress
    # --------------------------------------------------------

    if chunk_no % 10 == 0:

        elapsed = (
            time.time() - start_time
        ) / 60

        print(
            f"Chunk {chunk_no:4d} | "
            f"Rows scanned: {total_rows:,} | "
            f"Excellent rows: {selected_rows:,} | "
            f"Time: {elapsed:.1f} min"
        )

# ============================================================
# COMBINE TEMPORARY FILES
# ============================================================

print()
print("Combining temporary files...")

temp_files = sorted(
    [
        os.path.join(
            TEMP_DIR,
            f
        )
        for f in os.listdir(TEMP_DIR)
        if f.endswith(".parquet")
    ]
)

frames = []

for file in temp_files:

    frames.append(
        pd.read_parquet(file)
    )

if frames:

    excellent_df = pd.concat(
        frames,
        ignore_index=True
    )

    # --------------------------------------------------------
    # GLOBAL SORT
    # --------------------------------------------------------

    excellent_df = excellent_df.sort_values(
        [
            "device_id",
            "timestamp"
        ]
    )

    # --------------------------------------------------------
    # Save final dataset
    # --------------------------------------------------------

    excellent_df.to_parquet(
        OUTPUT_FILE,
        index=False
    )

    print(
        f"Final rows: {len(excellent_df):,}"
    )

else:

    raise RuntimeError(
        "No Excellent-device records were found."
    )

# ============================================================
# REMOVE TEMPORARY FILES
# ============================================================

for file in temp_files:

    os.remove(file)

try:
    os.rmdir(TEMP_DIR)
except OSError:
    pass

# ============================================================
# SUMMARY
# ============================================================

elapsed = (
    time.time() - start_time
) / 60

print()
print("=" * 70)
print("EXTRACTION COMPLETE")
print("=" * 70)

print(
    f"Rows scanned:       {total_rows:,}"
)

print(
    f"Excellent rows:     {len(excellent_df):,}"
)

print(
    f"Devices:            "
    f"{excellent_df['device_id'].nunique()}"
)

print(
    f"Time range:         "
    f"{excellent_df['timestamp'].min()} "
    f"→ "
    f"{excellent_df['timestamp'].max()}"
)

print(
    f"Output size:        "
    f"{os.path.getsize(OUTPUT_FILE) / (1024**3):.2f} GB"
)

print(
    f"Processing time:    {elapsed:.2f} minutes"
)

print()
print("Output:")
print(OUTPUT_FILE)

print("=" * 70)

