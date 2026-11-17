from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
from zipfile import ZipFile

import duckdb

root = Path(__file__).resolve().parents[2]

data_dir = root / "data/raw/world_bank"
data_dir.mkdir(parents=True, exist_ok=True)

csv_path = data_dir / "API_FP.CPI.TOTL.ZG_DS2_en_csv_v2_259659.csv"

url = (
    "https://api.worldbank.org/v2/country/sn/"
    "indicator/FP.CPI.TOTL.ZG"
    "?date=2000:2025&downloadformat=csv"
)

request = Request(url, headers={"User-Agent": "Mozilla/5.0"})

with urlopen(request, timeout=120) as response:
    archive_data = response.read()

with ZipFile(BytesIO(archive_data)) as archive:
    csv_files = [
        name
        for name in archive.namelist()
        if name.startswith("API_FP.CPI.TOTL.ZG_DS2_en_csv_v2_") and name.endswith(".csv")
    ]

    if not csv_files:
        raise RuntimeError("Aucun fichier CSV CPI trouvé dans l'archive.")

    with archive.open(csv_files[0]) as source:
        csv_path.write_bytes(source.read())

con = duckdb.connect(str(root / "entrepot.duckdb"))

con.execute("CREATE SCHEMA IF NOT EXISTS raw")

con.execute(
    """
    CREATE OR REPLACE TABLE raw.wb_cpi_annual AS
    SELECT *
    FROM read_csv(
        ?,
        skip = 4,
        all_varchar = true,
        header = true
    )
    """,
    [str(csv_path)],
)

con.close()

print("Ingestion Banque mondiale terminée.")
