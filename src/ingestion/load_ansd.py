import os
import urllib.error
import urllib.request
from pathlib import Path

# Doit être défini avant l'import de knoema (host du portail ANSD)
os.environ.setdefault("KNOEMA_HOST", "senegal.opendataforafrica.org")

import duckdb  # noqa: E402
import knoema  # noqa: E402

# User-Agent explicite (celui par défaut de urllib peut être refusé par le portail)
_orig_init = urllib.request.OpenerDirector.__init__


def _init_with_ua(self):
    _orig_init(self)
    self.addheaders = [("User-Agent", "entrepot-donnees-ouvertes/1.0 (projet open data, Dakar)")]


urllib.request.OpenerDirector.__init__ = _init_with_ua

root = Path(__file__).resolve().parents[2]

data_dir = root / "data/raw/ansd"
data_dir.mkdir(parents=True, exist_ok=True)

csv_path = data_dir / "ObservationData_xccvfug.csv"

try:
    df = knoema.get(
        "tsghpfc",
        timerange="2016M1-2026M12",
        Indicateurs="011",
    )
    if df.empty:
        raise RuntimeError("Aucune donnée récupérée depuis le portail ANSD.")
    df.reset_index().to_csv(csv_path, index=False)
except (urllib.error.URLError, RuntimeError) as e:
    if not csv_path.exists():
        raise
    print(f"Téléchargement impossible ({e}), utilisation du CSV existant.")

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
