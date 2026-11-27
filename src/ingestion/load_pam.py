from pathlib import Path
from urllib.request import Request, urlopen

import duckdb

root = Path(__file__).resolve().parents[2]

data_dir = root / "data/raw/pam"
data_dir.mkdir(parents=True, exist_ok=True)

csv_path = data_dir / "wfp_food_prices_sen.csv"

url = (
    "https://data.humdata.org/dataset/"
    "77b76bc7-1edd-43f6-a5e4-784498ff6aca/"
    "resource/04ffc070-6d05-4653-a9f6-9f3f893a229e/"
    "download/wfp_food_prices_sen.csv"
)

request = Request(url, headers={"User-Agent": "Mozilla/5.0"})

with urlopen(request, timeout=120) as response:
    csv_path.write_bytes(response.read())

con = duckdb.connect(str(root / "entrepot.duckdb"))

con.execute("CREATE SCHEMA IF NOT EXISTS raw")

# Le CSV HDX contient une 2e ligne de balises HXL (#date, #adm1+name...) :
# on l'écarte explicitement, car DuckDB ne la saute pas toujours seul.
con.execute(
    """
    CREATE OR REPLACE TABLE raw.pam_prix AS
    SELECT *
    FROM read_csv(?, all_varchar = true, header = true)
    WHERE date NOT LIKE '#%'
    """,
    [str(csv_path)],
)

con.close()

print("Ingestion PAM terminée.")
