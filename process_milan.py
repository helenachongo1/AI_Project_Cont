from pathlib import Path
import pandas as pd


# ============================================================
# 1. FOLDERS
# ============================================================

INPUT_DIR = Path(r"E:\Android\ICT_2025\ICT_26_27\CP\dataset_10_samples")
OUTPUT_DIR = Path(r"E:\Android\ICT_2025\ICT_26_27\CP\dataset_10_samples\processed")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# 2. RAW DATA COLUMN NAMES
# ============================================================

column_names = [
    "SquareID",
    "Timestamp",
    "CountryCode",
    "SMS_IN",
    "SMS_OUT",
    "CALL_IN",
    "CALL_OUT",
    "InternetTraffic"
]


# ============================================================
# 3. TRAFFIC COLUMNS TO AGGREGATE
# ============================================================

traffic_columns = [
    "SMS_IN",
    "SMS_OUT",
    "CALL_IN",
    "CALL_OUT",
    "InternetTraffic"
]


# ============================================================
# 4. PROCESS ONE FILE
# ============================================================

def process_file(input_file, output_file, chunksize=200_000):

    print("\n" + "=" * 70)
    print(f"Processing: {input_file.name}")
    print("=" * 70)

    processed_chunks = []

    chunk_number = 0

    for chunk in pd.read_csv(
        input_file,
        sep="\t",
        names=column_names,
        chunksize=chunksize
    ):

        chunk_number += 1

        print(
            f"  Reading chunk {chunk_number} "
            f"({len(chunk):,} raw rows)"
        )

        # ----------------------------------------------------
        # Convert Unix timestamp (milliseconds) to datetime
        # ----------------------------------------------------

        chunk["Timestamp"] = pd.to_datetime(
            chunk["Timestamp"],
            unit="ms"
        )

        # ----------------------------------------------------
        # Same aggregation as your original preprocessing
        # ----------------------------------------------------

        chunk = (
            chunk
            .groupby(
                ["SquareID", "Timestamp"],
                as_index=False
            )
            .agg({
                "SMS_IN": "sum",
                "SMS_OUT": "sum",
                "CALL_IN": "sum",
                "CALL_OUT": "sum",
                "InternetTraffic": "sum"
            })
        )

        processed_chunks.append(chunk)

    # ========================================================
    # Combine the processed chunks
    # ========================================================

    print("\nCombining processed chunks...")

    df = pd.concat(
        processed_chunks,
        ignore_index=True
    )

    # ========================================================
    # IMPORTANT:
    #
    # The same SquareID + Timestamp could exist in different
    # chunks, so aggregate one more time.
    # ========================================================

    df = (
        df
        .groupby(
            ["SquareID", "Timestamp"],
            as_index=False
        )
        .agg({
            "SMS_IN": "sum",
            "SMS_OUT": "sum",
            "CALL_IN": "sum",
            "CALL_OUT": "sum",
            "InternetTraffic": "sum"
        })
    )

    # ========================================================
    # Sort
    # ========================================================

    df = df.sort_values(
        ["SquareID", "Timestamp"]
    ).reset_index(drop=True)

    # ========================================================
    # Save as Parquet
    # ========================================================

    df.to_parquet(
        output_file,
        index=False
    )

    # ========================================================
    # Validation information
    # ========================================================

    print("\nFinished processing.")

    print(f"Raw file:")
    print(f"  {input_file}")

    print(f"\nProcessed file:")
    print(f"  {output_file}")

    print(f"\nProcessed shape:")
    print(f"  {df.shape}")

    print(f"\nNumber of SquareIDs:")
    print(f"  {df['SquareID'].nunique():,}")

    print(f"\nTime range:")
    print(f"  {df['Timestamp'].min()}")
    print(f"  {df['Timestamp'].max()}")

    print("\nRows per SquareID:")
    print(
        df.groupby("SquareID")
          .size()
          .describe()
    )

    print("\nMissing values:")
    print(df.isnull().sum())

    return df


# ============================================================
# 5. FIND RAW FILES
# ============================================================

files = sorted(
    INPUT_DIR.glob("sms-call-internet-mi-*.txt")
)


# ============================================================
# 6. CHECK FILES
# ============================================================

print("=" * 70)
print("MILAN DATASET PROCESSING")
print("=" * 70)

print(f"\nInput directory:")
print(f"  {INPUT_DIR}")

print(f"\nOutput directory:")
print(f"  {OUTPUT_DIR}")

print(f"\nRaw files found: {len(files)}")

for file in files:
    print(f"  - {file.name}")


# ============================================================
# 7. PROCESS EACH FILE
# ============================================================

for input_file in files:

    output_file = (
        OUTPUT_DIR /
        f"{input_file.stem}.parquet"
    )

    # Avoid processing again if the output already exists
    if output_file.exists():

        print(
            f"\nSkipping {input_file.name} "
            f"(already processed)."
        )

        continue

    process_file(
        input_file=input_file,
        output_file=output_file,
        chunksize=200_000
    )


# ============================================================
# 8. FINISHED
# ============================================================

print("\n" + "=" * 70)
print("ALL FILES PROCESSED")
print("=" * 70)

print(f"\nProcessed files are located at:")
print(OUTPUT_DIR)