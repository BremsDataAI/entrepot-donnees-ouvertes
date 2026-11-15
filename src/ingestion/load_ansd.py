from pathlib import Path

import duckdb

root = Path(__file__).resolve().parents[2]

con = duckdb.connect(str(root / "entrepot.duckdb"))

con.sql("CREATE SCHEMA IF NOT EXISTS raw")

con.sql(f"""
    CREATE OR REPLACE TABLE raw.ansd_ihpc AS
    SELECT *
    FROM read_csv(
        '{root / "data/raw/ansd/ObservationData_xccvfug.csv"}',
        all_varchar = true,
        header = true
    )
""")

con.close()
