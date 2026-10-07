import pandas as pd
import os
import gc

RAW_FILE = r"D:\Android\measurements\measurements-out.csv"


OUTPUT_FILE = r"D:\Android\measurements\CARE_dataset\safecast_gps_join.csv"


CHUNK_SIZE = 100_000


# ============================================================
# REQUIRED RAW SAFECAST COLUMNS
# ============================================================

USECOLS = [
    "Captured Time",
    "Latitude",
    "Longitude",
    "Device ID"
]


# ============================================================
# CHECK FILE
# ============================================================

if not os.path.exists(RAW_FILE):
    raise FileNotFoundError(
        f"Raw Safecast file not found:\n{RAW_FILE}"
    )

print("=" * 70)
print("CARE++ LOCAL SAFECAST GPS EXTRACTION")
print("=" * 70)

print("\nInput file:")
print(RAW_FILE)

print("\nOutput file:")
print(OUTPUT_FILE)

print("\nProcessing in chunks...")
print("This avoids loading the entire Safecast file into RAM.")


# ============================================================
# REMOVE OLD OUTPUT IF IT EXISTS
# ============================================================

if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)
    print("\nExisting output file removed.")


# ============================================================
# PROCESS RAW SAFECAST FILE IN CHUNKS
# ============================================================

first_chunk = True

total_rows_read = 0
total_rows_saved = 0
chunk_number = 0

reader = pd.read_csv(
    RAW_FILE,
    usecols=USECOLS,
    chunksize=CHUNK_SIZE,
    low_memory=True,
    dtype={
        "Device ID": "string"
    }
)


for chunk in reader:

    chunk_number += 1

    total_rows_read += len(chunk)

    print(
        f"\nProcessing chunk {chunk_number} "
        f"| rows read so far: {total_rows_read:,}"
    )

    # --------------------------------------------------------
    # Rename to CARE++ join names
    # --------------------------------------------------------

    chunk = chunk.rename(columns={
        "Captured Time": "timestamp",
        "Latitude": "lat",
        "Longitude": "lon",
        "Device ID": "device_id"
    })

    # --------------------------------------------------------
    # Convert timestamp
    # --------------------------------------------------------

    chunk["timestamp"] = pd.to_datetime(
        chunk["timestamp"],
        errors="coerce",
        utc=True
    )

    # --------------------------------------------------------
    # Convert GPS coordinates
    # --------------------------------------------------------

    chunk["lat"] = pd.to_numeric(
        chunk["lat"],
        errors="coerce"
    )

    chunk["lon"] = pd.to_numeric(
        chunk["lon"],
        errors="coerce"
    )

    # --------------------------------------------------------
    # Remove invalid rows
    # --------------------------------------------------------

    chunk = chunk.dropna(
        subset=[
            "device_id",
            "timestamp",
            "lat",
            "lon"
        ]
    )

    # --------------------------------------------------------
    # Keep only required columns
    # --------------------------------------------------------

    chunk = chunk[
        [
            "device_id",
            "timestamp",
            "lat",
            "lon"
        ]
    ]

    # --------------------------------------------------------
    # Remove duplicate records inside this chunk
    # --------------------------------------------------------

    chunk = chunk.drop_duplicates(
        subset=[
            "device_id",
            "timestamp"
        ]
    )

    # --------------------------------------------------------
    # Append to output CSV
    # --------------------------------------------------------

    if len(chunk) > 0:

        chunk.to_csv(
            OUTPUT_FILE,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False
        )

        first_chunk = False

        total_rows_saved += len(chunk)

    # --------------------------------------------------------
    # Release memory
    # --------------------------------------------------------

    del chunk
    gc.collect()


# ============================================================
# VERIFY OUTPUT
# ============================================================

print("\n" + "=" * 70)
print("EXTRACTION COMPLETED")
print("=" * 70)

print(f"\nTotal raw rows processed: {total_rows_read:,}")
print(f"GPS rows written:         {total_rows_saved:,}")

print(f"\nOutput file:")
print(OUTPUT_FILE)

if os.path.exists(OUTPUT_FILE):

    file_size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)

    print(
        f"\nOutput file size: "
        f"{file_size_mb:.2f} MB"
    )

    # Read only the reduced file for verification
    gps_check = pd.read_csv(
        OUTPUT_FILE,
        nrows=10
    )

    print("\nOutput columns:")
    print(gps_check.columns.tolist())

    print("\nFirst 10 rows:")
    print(gps_check)

    del gps_check
    gc.collect()

print("\n" + "=" * 70)
print("READY FOR GOOGLE COLAB")
print("=" * 70)

