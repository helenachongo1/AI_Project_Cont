import os
import csv
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# ============================================================
# CONFIGURATION
# ============================================================

INPUT_FILE = r"D:\Android\measurements\CARE_dataset\safecast_gps_join.csv"

OUTPUT_DIR = r"D:\Android\measurements\CARE_dataset\safecast_gps_parquet"

ROWS_PER_FILE = 500_000


# ============================================================
# CREATE OUTPUT DIRECTORY
# ============================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ============================================================
# REMOVE OLD PARQUET FILES
# ============================================================

for filename in os.listdir(OUTPUT_DIR):

    if filename.endswith(".parquet"):

        os.remove(
            os.path.join(OUTPUT_DIR, filename)
        )


# ============================================================
# PROCESS CSV AS A STREAM
# ============================================================

print("=" * 70)
print("SAFECAST GPS → PARQUET CHUNK CONVERSION")
print("=" * 70)

print("\nInput:")
print(INPUT_FILE)

print("\nOutput directory:")
print(OUTPUT_DIR)

print(f"\nRows per Parquet file: {ROWS_PER_FILE:,}")

print("\nStarting conversion...")


buffer = []

file_number = 0
total_rows = 0


with open(
    INPUT_FILE,
    "r",
    encoding="utf-8",
    newline=""
) as f:

    reader = csv.DictReader(f)

    for row in reader:

        buffer.append({
            "device_id": row["device_id"],
            "timestamp": row["timestamp"],
            "lat": row["lat"],
            "lon": row["lon"]
        })

        total_rows += 1

        # ----------------------------------------------------
        # Write one Parquet chunk
        # ----------------------------------------------------

        if len(buffer) >= ROWS_PER_FILE:

            file_number += 1

            output_file = os.path.join(
                OUTPUT_DIR,
                f"safecast_gps_part_{file_number:04d}.parquet"
            )

            df_chunk = pd.DataFrame(buffer)

            # Convert types
            df_chunk["device_id"] = (
                df_chunk["device_id"]
                .astype("string")
            )

            df_chunk["timestamp"] = pd.to_datetime(
                df_chunk["timestamp"],
                errors="coerce",
                utc=True
            )

            df_chunk["lat"] = pd.to_numeric(
                df_chunk["lat"],
                errors="coerce"
            )

            df_chunk["lon"] = pd.to_numeric(
                df_chunk["lon"],
                errors="coerce"
            )

            # Remove invalid rows
            df_chunk = df_chunk.dropna(
                subset=[
                    "device_id",
                    "timestamp",
                    "lat",
                    "lon"
                ]
            )

            # Write Parquet
            df_chunk.to_parquet(
                output_file,
                index=False,
                engine="pyarrow",
                compression="snappy"
            )

            print(
                f"Created: "
                f"{os.path.basename(output_file)} "
                f"| {len(df_chunk):,} rows "
                f"| total processed: {total_rows:,}"
            )

            del df_chunk

            buffer = []


# ============================================================
# WRITE FINAL CHUNK
# ============================================================

if len(buffer) > 0:

    file_number += 1

    output_file = os.path.join(
        OUTPUT_DIR,
        f"safecast_gps_part_{file_number:04d}.parquet"
    )

    df_chunk = pd.DataFrame(buffer)

    df_chunk["device_id"] = (
        df_chunk["device_id"]
        .astype("string")
    )

    df_chunk["timestamp"] = pd.to_datetime(
        df_chunk["timestamp"],
        errors="coerce",
        utc=True
    )

    df_chunk["lat"] = pd.to_numeric(
        df_chunk["lat"],
        errors="coerce"
    )

    df_chunk["lon"] = pd.to_numeric(
        df_chunk["lon"],
        errors="coerce"
    )

    df_chunk = df_chunk.dropna(
        subset=[
            "device_id",
            "timestamp",
            "lat",
            "lon"
        ]
    )

    df_chunk.to_parquet(
        output_file,
        index=False,
        engine="pyarrow",
        compression="snappy"
    )

    print(
        f"Created: "
        f"{os.path.basename(output_file)} "
        f"| {len(df_chunk):,} rows"
    )


# ============================================================
# FINAL REPORT
# ============================================================

print("\n" + "=" * 70)
print("CONVERSION COMPLETE")
print("=" * 70)

print(f"\nTotal rows processed: {total_rows:,}")
print(f"Parquet files created: {file_number}")

print("\nOutput directory:")
print(OUTPUT_DIR)

print("\nFiles:")

for filename in sorted(os.listdir(OUTPUT_DIR)):

    if filename.endswith(".parquet"):

        filepath = os.path.join(
            OUTPUT_DIR,
            filename
        )

        size_mb = os.path.getsize(filepath) / (
            1024 * 1024
        )

        print(
            f"  {filename} "
            f"({size_mb:.2f} MB)"
        )

print("\nDone.")