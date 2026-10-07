import duckdb
import os
import time
import shutil

# ============================================================
# CARE++ — SAFECAST MODELING DATASET DERIVATION
# ============================================================
#
# INPUT:
#   safecast_radiation_clean.csv
#
# OUTPUT:
#   safecast_5min_radiation.parquet
#   safecast_radiation_events.parquet
#   safecast_device_summary.csv
#
# IMPORTANT:
#   - Does NOT load the complete CSV into RAM
#   - Uses DuckDB streaming/external processing
#   - Uses disk for temporary operations
# ============================================================


# ============================================================
# 1. PATHS
# ============================================================

INPUT_FILE = (
    r"E:\Android\measurements\CARE_dataset"
    r"\safecast_radiation_clean.csv"
)

OUTPUT_DIR = (
    r"E:\Android\measurements\CARE_dataset"
    r"\modeling"
)

TEMP_DIR = (
    r"E:\Android\measurements\CARE_dataset"
    r"\modeling\duckdb_temp"
)

# ============================================================
# 2. CREATE DIRECTORIES
# ============================================================

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

FIVE_MIN_FILE = os.path.join(
    OUTPUT_DIR,
    "safecast_5min_radiation.parquet"
)

EVENT_FILE = os.path.join(
    OUTPUT_DIR,
    "safecast_radiation_events.parquet"
)

SUMMARY_FILE = os.path.join(
    OUTPUT_DIR,
    "safecast_device_summary.csv"
)

DB_FILE = os.path.join(
    OUTPUT_DIR,
    "care_safecast_modeling.duckdb"
)


# ============================================================
# 3. CHECK INPUT
# ============================================================

if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(
        f"Input dataset not found:\n{INPUT_FILE}"
    )

input_size_gb = (
    os.path.getsize(INPUT_FILE)
    / (1024 ** 3)
)

print("=" * 75)
print("CARE++ SAFECAST MODELING DATASET DERIVATION")
print("=" * 75)

print(f"Input file:")
print(INPUT_FILE)

print(f"\nInput size: {input_size_gb:.2f} GB")

print(f"\nOutput directory:")
print(OUTPUT_DIR)


# ============================================================
# 4. REMOVE PREVIOUS OUTPUTS
# ============================================================

for file in [
    FIVE_MIN_FILE,
    EVENT_FILE,
    SUMMARY_FILE
]:

    if os.path.exists(file):
        os.remove(file)
        print(f"Removed old file: {os.path.basename(file)}")


# ============================================================
# 5. CONNECT DUCKDB
# ============================================================

print("\nStarting DuckDB...")

con = duckdb.connect(DB_FILE)

# ------------------------------------------------------------
# MEMORY LIMIT
# ------------------------------------------------------------

# Keep this conservative.
# Increase only if your machine has plenty of RAM.

con.execute(
    "SET memory_limit='2GB'"
)

# ------------------------------------------------------------
# TEMPORARY DISK STORAGE
# ------------------------------------------------------------

con.execute(
    f"SET temp_directory='{TEMP_DIR}'"
)

# ------------------------------------------------------------
# REDUCE RAM pressure
# ------------------------------------------------------------

con.execute(
    "SET preserve_insertion_order=false"
)

con.execute(
    "SET threads=2"
)

print("DuckDB configured.")
print("Memory limit: 2 GB")
print("Temporary directory:")
print(TEMP_DIR)


# ============================================================
# 6. DEFINE SAFECAST CSV VIEW
# ============================================================
#
# Explicit column types are VERY important.
#
# We do NOT use read_csv_auto().
#
# ============================================================

print("\nCreating streaming CSV view...")

con.execute(
    f"""
    CREATE OR REPLACE VIEW safecast_clean AS

    SELECT

        TRY_CAST(timestamp AS TIMESTAMP)
            AS timestamp,

        TRY_CAST(device_id AS BIGINT)
            AS device_id,

        TRY_CAST(latitude AS DOUBLE)
            AS latitude,

        TRY_CAST(longitude AS DOUBLE)
            AS longitude,

        location_name,

        TRY_CAST(cpm AS DOUBLE)
            AS cpm,

        TRY_CAST(height AS DOUBLE)
            AS height,

        TRY_CAST(device_quality_score AS DOUBLE)
            AS device_quality_score,

        device_quality,

        quality_flag

    FROM read_csv(
        '{INPUT_FILE.replace("\\", "/")}',
        header=true,
        auto_detect=false,

        columns={{
            'timestamp': 'VARCHAR',
            'device_id': 'VARCHAR',
            'latitude': 'VARCHAR',
            'longitude': 'VARCHAR',
            'location_name': 'VARCHAR',
            'cpm': 'VARCHAR',
            'height': 'VARCHAR',
            'device_quality_score': 'VARCHAR',
            'device_quality': 'VARCHAR',
            'quality_flag': 'VARCHAR'
        }},

        ignore_errors=false,
        null_padding=true
    )
    """
)

print("CSV view created successfully.")


# ============================================================
# 7. CHECK NUMBER OF EXCELLENT DEVICES
# ============================================================

print("\nChecking excellent devices...")

result = con.execute(
    """
    SELECT
        COUNT(DISTINCT device_id) AS devices,
        COUNT(*) AS rows
    FROM safecast_clean
    WHERE device_quality = 'Excellent'
    """
).fetchone()

excellent_devices = result[0]
excellent_rows = result[1]

print(f"Excellent devices: {excellent_devices:,}")
print(f"Excellent rows:    {excellent_rows:,}")


# ============================================================
# 8. CREATE 5-MINUTE RADIATION DATASET
# ============================================================
#
# Each row represents approximately one 5-minute interval
# for one device/location.
#
# Features:
#
# timestamp
# device_id
# latitude
# longitude
# location_name
# cpm_mean
# cpm_median
# cpm_std
# cpm_min
# cpm_max
# readings
# height_mean
# quality_score
#
# ============================================================

print("\n")
print("=" * 75)
print("STEP 1 — CREATING 5-MINUTE RADIATION DATASET")
print("=" * 75)

start = time.time()

query = f"""
COPY (

    SELECT

        date_trunc(
            'minute',
            timestamp
        )
        -
        INTERVAL (
            EXTRACT(
                MINUTE FROM timestamp
            ) % 5
        ) MINUTE
        AS timestamp,

        device_id,

        AVG(latitude) AS latitude,

        AVG(longitude) AS longitude,

        MAX(location_name) AS location_name,

        AVG(cpm) AS cpm_mean,

        MEDIAN(cpm) AS cpm_median,

        STDDEV_POP(cpm) AS cpm_std,

        MIN(cpm) AS cpm_min,

        MAX(cpm) AS cpm_max,

        COUNT(*) AS readings,

        AVG(height) AS height_mean,

        MAX(device_quality_score)
            AS device_quality_score,

        MAX(device_quality)
            AS device_quality

    FROM safecast_clean

    WHERE

        device_quality = 'Excellent'

        AND timestamp IS NOT NULL

        AND cpm IS NOT NULL

        AND cpm >= 0

        AND latitude BETWEEN -90 AND 90

        AND longitude BETWEEN -180 AND 180

    GROUP BY

        1,
        device_id

    ORDER BY

        device_id,
        timestamp

)
TO '{FIVE_MIN_FILE.replace("\\", "/")}'
(
    FORMAT PARQUET,
    COMPRESSION ZSTD
)
"""

con.execute(query)

elapsed = (time.time() - start) / 60

print(
    f"\n5-minute dataset created "
    f"in {elapsed:.2f} minutes."
)

print(FIVE_MIN_FILE)


# ============================================================
# 9. INSPECT 5-MINUTE DATASET
# ============================================================

print("\nInspecting 5-minute dataset...")

info = con.execute(
    f"""
    SELECT

        COUNT(*) AS rows,

        COUNT(DISTINCT device_id)
            AS devices,

        MIN(timestamp)
            AS first_timestamp,

        MAX(timestamp)
            AS last_timestamp,

        AVG(cpm_mean)
            AS mean_cpm,

        MIN(cpm_min)
            AS minimum_cpm,

        MAX(cpm_max)
            AS maximum_cpm

    FROM read_parquet(
        '{FIVE_MIN_FILE.replace("\\", "/")}'
    )
    """
).fetchone()

print("\n5-MINUTE DATASET SUMMARY")
print("-" * 50)

print(f"Rows:             {info[0]:,}")
print(f"Devices:          {info[1]:,}")
print(f"First timestamp:  {info[2]}")
print(f"Last timestamp:   {info[3]}")
print(f"Mean CPM:         {info[4]:.3f}")
print(f"Minimum CPM:      {info[5]:.3f}")
print(f"Maximum CPM:      {info[6]:.3f}")


# ============================================================
# 10. CREATE DEVICE SUMMARY
# ============================================================

print("\n")
print("=" * 75)
print("STEP 2 — CREATING DEVICE SUMMARY")
print("=" * 75)

start = time.time()

con.execute(
    f"""
    COPY (

        SELECT

            device_id,

            COUNT(*) AS intervals,

            MIN(timestamp)
                AS first_timestamp,

            MAX(timestamp)
                AS last_timestamp,

            COUNT(DISTINCT
                CAST(timestamp AS DATE)
            )
            AS days_observed,

            AVG(cpm_mean)
                AS mean_cpm,

            MEDIAN(cpm_median)
                AS median_cpm,

            STDDEV_POP(cpm_mean)
                AS std_cpm,

            MIN(cpm_min)
                AS minimum_cpm,

            MAX(cpm_max)
                AS maximum_cpm,

            AVG(readings)
                AS mean_readings_per_interval,

            AVG(latitude)
                AS mean_latitude,

            AVG(longitude)
                AS mean_longitude,

            MAX(device_quality_score)
                AS device_quality_score

        FROM read_parquet(
            '{FIVE_MIN_FILE.replace("\\", "/")}'
        )

        GROUP BY device_id

        ORDER BY intervals DESC

    )

    TO '{SUMMARY_FILE.replace("\\", "/")}'
    (
        HEADER,
        DELIMITER ','
    )
    """
)

elapsed = (time.time() - start) / 60

print(
    f"Device summary created "
    f"in {elapsed:.2f} minutes."
)

print(SUMMARY_FILE)


# ============================================================
# 11. CREATE RADIATION EVENT DATASET
# ============================================================
#
# IMPORTANT:
#
# We are NOT claiming that a particular CPM value is
# medically dangerous.
#
# Events are statistical anomalies relative to each device's
# own recent radiation baseline.
#
# We use:
#
# rolling median
# rolling standard deviation
#
# and calculate a statistical anomaly score.
#
# ============================================================

print("\n")
print("=" * 75)
print("STEP 3 — CREATING RADIATION EVENT DATASET")
print("=" * 75)

start = time.time()

query = f"""
COPY (

    SELECT

        *,

        AVG(cpm_mean)
            OVER (
                PARTITION BY device_id
                ORDER BY timestamp
                ROWS BETWEEN 12 PRECEDING
                AND 1 PRECEDING
            )
            AS previous_mean_cpm,

        STDDEV_POP(cpm_mean)
            OVER (
                PARTITION BY device_id
                ORDER BY timestamp
                ROWS BETWEEN 12 PRECEDING
                AND 1 PRECEDING
            )
            AS previous_std_cpm,

        MEDIAN(cpm_mean)
            OVER (
                PARTITION BY device_id
                ORDER BY timestamp
                ROWS BETWEEN 12 PRECEDING
                AND 1 PRECEDING
            )
            AS previous_median_cpm

    FROM read_parquet(
        '{FIVE_MIN_FILE.replace("\\", "/")}'
    )

)
TO '{EVENT_FILE.replace("\\", "/")}'
(
    FORMAT PARQUET,
    COMPRESSION ZSTD
)
"""

con.execute(query)

elapsed = (time.time() - start) / 60

print(
    f"\nRadiation event base dataset created "
    f"in {elapsed:.2f} minutes."
)


# ============================================================
# 12. FINAL EVENT CLASSIFICATION
# ============================================================
#
# We now replace the intermediate event file with a final
# event-oriented dataset.
#
# Statistical event:
#
# cpm_mean > previous_mean + 3 * previous_std
#
# This is a MODELING/ANOMALY criterion, NOT a health threshold.
#
# ============================================================

EVENT_FINAL = os.path.join(
    OUTPUT_DIR,
    "safecast_radiation_events_final.parquet"
)

if os.path.exists(EVENT_FINAL):
    os.remove(EVENT_FINAL)

print("\nClassifying statistical radiation events...")

con.execute(
    f"""
    COPY (

        SELECT

            timestamp,

            device_id,

            latitude,

            longitude,

            location_name,

            cpm_mean,

            cpm_median,

            cpm_std,

            cpm_min,

            cpm_max,

            readings,

            previous_mean_cpm,

            previous_std_cpm,

            previous_median_cpm,

            CASE

                WHEN
                    previous_std_cpm IS NOT NULL
                    AND previous_std_cpm > 0
                    AND cpm_mean >
                        previous_mean_cpm
                        + 3 * previous_std_cpm

                THEN 1

                ELSE 0

            END AS statistical_event,

            CASE

                WHEN
                    previous_std_cpm IS NOT NULL
                    AND previous_std_cpm > 0

                THEN
                    (
                        cpm_mean
                        - previous_mean_cpm
                    )
                    / previous_std_cpm

                ELSE NULL

            END AS anomaly_score

        FROM read_parquet(
            '{EVENT_FILE.replace("\\", "/")}'
        )

        WHERE

            previous_mean_cpm IS NOT NULL

    )

    TO '{EVENT_FINAL.replace("\\", "/")}'
    (
        FORMAT PARQUET,
        COMPRESSION ZSTD
    )
    """
)

# Remove intermediate event file

if os.path.exists(EVENT_FILE):
    os.remove(EVENT_FILE)

print("Final event dataset created.")
print(EVENT_FINAL)


# ============================================================
# 13. EVENT SUMMARY
# ============================================================

event_stats = con.execute(
    f"""
    SELECT

        COUNT(*) AS rows,

        SUM(statistical_event)
            AS events,

        COUNT(DISTINCT device_id)
            AS devices,

        AVG(anomaly_score)
            AS mean_anomaly_score,

        MAX(anomaly_score)
            AS maximum_anomaly_score

    FROM read_parquet(
        '{EVENT_FINAL.replace("\\", "/")}'
    )
    """
).fetchone()

print("\nEVENT DATASET SUMMARY")
print("-" * 50)

print(f"Rows:              {event_stats[0]:,}")
print(f"Statistical events:{event_stats[1]:,}")
print(f"Devices:           {event_stats[2]:,}")
print(f"Mean anomaly score:{event_stats[3]:.3f}")
print(f"Max anomaly score: {event_stats[4]:.3f}")


# ============================================================
# 14. FINAL DATASET INVENTORY
# ============================================================

print("\n")
print("=" * 75)
print("CARE++ MODELING DATASETS READY")
print("=" * 75)

files = [
    FIVE_MIN_FILE,
    SUMMARY_FILE,
    EVENT_FINAL
]

for file in files:

    if os.path.exists(file):

        size_mb = (
            os.path.getsize(file)
            / (1024 ** 2)
        )

        print(
            f"{os.path.basename(file):45s}"
            f"{size_mb:10.2f} MB"
        )

# ============================================================
# 15. CLOSE DATABASE
# ============================================================

con.close()

print("\nDuckDB closed.")

print("\nDONE.")
print("=" * 75)