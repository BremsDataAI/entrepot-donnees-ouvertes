from pathlib import Path

import duckdb

root = Path(__file__).resolve().parents[2]

con = duckdb.connect(str(root / "entrepot.duckdb"))

con.sql("CREATE SCHEMA IF NOT EXISTS raw")

con.sql(f"""
    CREATE OR REPLACE TABLE raw.pam_prix AS
    SELECT *
    FROM read_csv(
        '{root / "data/raw/pam/wfp_food_prices_sen.csv"}',
        all_varchar = true,
        header = true
    )
""")

con.close()
