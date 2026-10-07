import duckdb
import os
import time

# ============================================================
# CARE++ — SAFECAST MODELING DATASET GENERATION
# DISK-BASED DUCKDB VERSION
# ============================================================

INPUT_FILE = (
    r"E:\Android\measurements\CARE_dataset"
    r"\safecast_radiation_clean.csv"
)

OUTPUT_DIR = (
    r"E:\Android\measurements\CARE_dataset"
    r"\modeling"
)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# OUTPUTS
# ============================================================

TIMESERIES_FILE = os.path.join(
    OUTPUT_DIR,
    "safecast_5min_timeseries.parquet"
)

ANOMALY_FILE = os.path.join(
    OUTPUT_DIR,
    "safecast_anomaly_dataset.parquet"
)

ML_FILE = os.path.join(
    OUTPUT_DIR,
    "safecast_ml_dataset.parquet"
)

# ============================================================
# EXCELLENT DEVICES
# ============================================================

EXCELLENT_DEVICES = [
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
]

DEVICE_LIST = ",".join(
    str(x)
    for x in EXCELLENT_DEVICES
)

# ============================================================
# SETTINGS
# ============================================================

# Use a limited amount of RAM.
# DuckDB will spill intermediate operations to disk.

MEMORY_LIMIT = "4GB"

TEMP_DIRECTORY = os.path.join(
    OUTPUT_DIR,
    "duckdb_temp"
)

os.makedirs(
    TEMP_DIRECTORY,
    exist_ok=True
)

# ============================================================
# START
# ============================================================

print("=" * 70)
print("CARE++ SAFECAST MODELING DATASET GENERATION")
print("=" * 70)

print()
print("Input:")
print(INPUT_FILE)

print()
print("Output:")
print(OUTPUT_DIR)

print()
print(
    f"Excellent devices: "
    f"{len(EXCELLENT_DEVICES)}"
)

start_time = time.time()

# ============================================================
# CONNECT TO DUCKDB
# ============================================================

DB_FILE = os.path.join(
    OUTPUT_DIR,
    "care_safecast.duckdb"
)

con = duckdb.connect(
    DB_FILE
)

# ------------------------------------------------------------
# Memory configuration
# ------------------------------------------------------------

con.execute(
    f"SET memory_limit='{MEMORY_LIMIT}'"
)

con.execute(
    f"SET temp_directory='{TEMP_DIRECTORY}'"
)

# Allow parallel processing
con.execute(
    "SET threads=4"
)

print()
print("DuckDB configured.")
print(
    f"Memory limit: {MEMORY_LIMIT}"
)

# ============================================================
# STEP 1 — CREATE 5-MINUTE TIME SERIES
# ============================================================

print()
print("=" * 70)
print("STEP 1 — 5-MINUTE RADIATION TIME SERIES")
print("=" * 70)

if os.path.exists(TIMESERIES_FILE):
    os.remove(TIMESERIES_FILE)

query = f"""
COPY (

    SELECT

        device_id,

        date_trunc(
            'minute',
            timestamp
        )
        -
        (
            EXTRACT(
                minute FROM timestamp
            ) % 5
        ) * INTERVAL '1 minute'
        AS timestamp,

        AVG(cpm) AS cpm_mean,

        MEDIAN(cpm) AS cpm_median,

        STDDEV_SAMP(cpm) AS cpm_std,

        MIN(cpm) AS cpm_min,

        MAX(cpm) AS cpm_max,

        COUNT(*) AS measurement_count,

        MEDIAN(latitude) AS latitude,

        MEDIAN(longitude) AS longitude

    FROM read_csv_auto(
        '{INPUT_FILE}',
        header=true,
        ignore_errors=true
    )

    WHERE
        device_id IN ({DEVICE_LIST})
        AND cpm IS NOT NULL
        AND cpm >= 0
        AND cpm <= 100000
        AND timestamp IS NOT NULL

    GROUP BY

        device_id,

        date_trunc(
            'minute',
            timestamp
        )
        -
        (
            EXTRACT(
                minute FROM timestamp
            ) % 5
        ) * INTERVAL '1 minute'

)
TO '{TIMESERIES_FILE}'
(
    FORMAT PARQUET,
    COMPRESSION ZSTD
);
"""

print("Creating 5-minute time series...")

con.execute(query)

print("5-minute dataset created.")

# ============================================================
# CHECK DATASET
# ============================================================

result = con.execute(
    f"""
    SELECT
        COUNT(*) AS rows,
        COUNT(DISTINCT device_id) AS devices,
        MIN(timestamp) AS first_timestamp,
        MAX(timestamp) AS last_timestamp
    FROM read_parquet(
        '{TIMESERIES_FILE}'
    )
    """
).fetchone()

print()
print("5-minute dataset:")
print(
    f"Rows:       {result[0]:,}"
)
print(
    f"Devices:    {result[1]}"
)
print(
    f"First time: {result[2]}"
)
print(
    f"Last time:  {result[3]}"
)

# ============================================================
# STEP 2 — ANOMALY FEATURES
# ============================================================

print()
print("=" * 70)
print("STEP 2 — ANOMALY FEATURES")
print("=" * 70)

if os.path.exists(ANOMALY_FILE):
    os.remove(ANOMALY_FILE)

query = f"""
COPY (

    WITH base AS (

        SELECT

            *,

            MEDIAN(cpm_median)
            OVER (
                PARTITION BY device_id
                ORDER BY timestamp
                ROWS BETWEEN 12 PRECEDING
                AND CURRENT ROW
            )
            AS rolling_median

        FROM read_parquet(
            '{TIMESERIES_FILE}'
        )

    ),

    deviations AS (

        SELECT

            *,

            MEDIAN(
                ABS(
                    cpm_median -
                    rolling_median
                )
            )
            OVER (
                PARTITION BY device_id
                ORDER BY timestamp
                ROWS BETWEEN 12 PRECEDING
                AND CURRENT ROW
            )
            AS rolling_mad

        FROM base

    )

    SELECT

        *,

        CASE

            WHEN rolling_mad IS NULL
                 OR rolling_mad = 0

            THEN 0

            ELSE

                0.6745 *
                (
                    cpm_median -
                    rolling_median
                )
                /
                rolling_mad

        END
        AS robust_z,

        CASE

            WHEN rolling_mad IS NULL
                 OR rolling_mad = 0

            THEN 0

            WHEN ABS(
                0.6745 *
                (
                    cpm_median -
                    rolling_median
                )
                /
                rolling_mad
            ) >= 3.5

            THEN 1

            ELSE 0

        END
        AS anomaly_flag

    FROM deviations

)
TO '{ANOMALY_FILE}'
(
    FORMAT PARQUET,
    COMPRESSION ZSTD
);
"""

print("Creating anomaly dataset...")

con.execute(query)

print("Anomaly dataset created.")

# ============================================================
# STEP 3 — ML DATASET
# ============================================================

print()
print("=" * 70)
print("STEP 3 — SUPERVISED ML DATASET")
print("=" * 70)

if os.path.exists(ML_FILE):
    os.remove(ML_FILE)

query = f"""
COPY (

    WITH features AS (

        SELECT

            *,

            LAG(cpm_median, 1)
            OVER (
                PARTITION BY device_id
                ORDER BY timestamp
            )
            AS lag_1,

            LAG(cpm_median, 2)
            OVER (
                PARTITION BY device_id
                ORDER BY timestamp
            )
            AS lag_2,

            LAG(cpm_median, 3)
            OVER (
                PARTITION BY device_id
                ORDER BY timestamp
            )
            AS lag_3,

            LAG(cpm_median, 6)
            OVER (
                PARTITION BY device_id
                ORDER BY timestamp
            )
            AS lag_6,

            LAG(cpm_median, 12)
            OVER (
                PARTITION BY device_id
                ORDER BY timestamp
            )
            AS lag_12,

            LEAD(cpm_median, 1)
            OVER (
                PARTITION BY device_id
                ORDER BY timestamp
            )
            AS target_future_cpm

        FROM read_parquet(
            '{ANOMALY_FILE}'
        )

    )

    SELECT

        timestamp,

        device_id,

        latitude,

        longitude,

        cpm_mean,

        cpm_median,

        cpm_std,

        cpm_min,

        cpm_max,

        measurement_count,

        rolling_median,

        rolling_mad,

        robust_z,

        anomaly_flag,

        lag_1,

        lag_2,

        lag_3,

        lag_6,

        lag_12,

        target_future_cpm

    FROM features

    WHERE

        lag_1 IS NOT NULL
        AND lag_2 IS NOT NULL
        AND lag_3 IS NOT NULL
        AND lag_6 IS NOT NULL
        AND lag_12 IS NOT NULL
        AND target_future_cpm IS NOT NULL

)
TO '{ML_FILE}'
(
    FORMAT PARQUET,
    COMPRESSION ZSTD
);
"""

print("Creating ML dataset...")

con.execute(query)

print("ML dataset created.")

# ============================================================
# STEP 4 — DATASET SUMMARY
# ============================================================

print()
print("=" * 70)
print("DATASET SUMMARY")
print("=" * 70)

for name, file in [
    ("5-minute time series", TIMESERIES_FILE),
    ("Anomaly dataset", ANOMALY_FILE),
    ("ML dataset", ML_FILE)
]:

    result = con.execute(
        f"""
        SELECT
            COUNT(*),
            COUNT(DISTINCT device_id),
            MIN(timestamp),
            MAX(timestamp)
        FROM read_parquet(
            '{file}'
        )
        """
    ).fetchone()

    size_gb = (
        os.path.getsize(file)
        /
        (1024 ** 3)
    )

    print()
    print(name)
    print("-" * 50)
    print(
        f"Rows:       {result[0]:,}"
    )
    print(
        f"Devices:    {result[1]}"
    )
    print(
        f"First time: {result[2]}"
    )
    print(
        f"Last time:  {result[3]}"
    )
    print(
        f"File size:  {size_gb:.3f} GB"
    )

# ============================================================
# FINISH
# ============================================================

con.close()

elapsed = (
    time.time() -
    start_time
) / 60

print()
print("=" * 70)
print("COMPLETE")
print("=" * 70)

print(
    f"Processing time: "
    f"{elapsed:.2f} minutes"
)

print()
print("Created:")

print(TIMESERIES_FILE)
print(ANOMALY_FILE)
print(ML_FILE)

print("=" * 70)