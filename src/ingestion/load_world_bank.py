from pathlib import Path

import duckdb

root = Path(__file__).resolve().parents[2]

con = duckdb.connect(str(root / "entrepot.duckdb"))

con.sql("CREATE SCHEMA IF NOT EXISTS raw")

con.sql(f"""
    CREATE OR REPLACE TABLE raw.wb_cpi_annual AS
    SELECT *
    FROM read_csv(
        '{root / "data/raw/world_bank/API_FP.CPI.TOTL.ZG_DS2_en_csv_v2_259659.csv"}',
        skip = 4,
        all_varchar = true,
        header = true
    )
""")

con.close()
