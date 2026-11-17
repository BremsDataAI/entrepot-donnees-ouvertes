from pathlib import Path

import duckdb
import knoema

root = Path(__file__).resolve().parents[2]

data_dir = root / "data/raw/ansd"
data_dir.mkdir(parents=True, exist_ok=True)

csv_path = data_dir / "ObservationData_xccvfug.csv"

df = knoema.get(
    "tsghpfc",
    timerange="2016M1-2026M12",
    Indicateurs="011",
)

if df.empty:
    raise RuntimeError("Aucune donnée récupérée depuis Knoema.")

df.reset_index().to_csv(csv_path, index=False)

con = duckdb.connect(str(root / "entrepot.duckdb"))

con.execute("CREATE SCHEMA IF NOT EXISTS raw")

con.execute(
    """
    CREATE OR REPLACE TABLE raw.ansd_ihpc AS
    SELECT *
    FROM read_csv(?, all_varchar = true, header = true)
    """,
    [str(csv_path)],
)

con.close()

print("Ingestion ANSD terminée.")
