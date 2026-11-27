import csv
import io
import urllib.request
from pathlib import Path
from urllib.error import HTTPError

import duckdb
import knoema
import pandas as pd
from curl_cffi import requests as cffi
from knoema.api_config import ApiConfig


def _open(self, req, data=None, timeout=60):
    # knoema passe par urllib, bloqué par Cloudflare (empreinte TLS) : on passe par curl_cffi.
    req = req if isinstance(req, urllib.request.Request) else urllib.request.Request(req, data)
    headers = {
        k: v
        for k, v in req.header_items()
        if k.lower() not in ("user-agent", "accept-encoding", "host")
    }
    r = cffi.request(
        req.get_method(),
        req.full_url,
        headers=headers,
        data=req.data,
        impersonate="chrome",
        timeout=60,
    )
    if r.status_code >= 400:
        raise HTTPError(req.full_url, r.status_code, r.reason, r.headers, io.BytesIO(r.content))
    resp = io.BytesIO(r.content)
    resp.status = resp.code = r.status_code
    resp.headers, resp.url = r.headers, str(r.url)
    resp.getcode, resp.info, resp.geturl = (
        (lambda: r.status_code),
        (lambda: r.headers),
        (lambda: resp.url),
    )
    return resp


urllib.request.OpenerDirector.open = _open
ApiConfig().host = "senegal.opendataforafrica.org"

root = Path(__file__).resolve().parents[2]
csv_path = root / "data/raw/ansd/ObservationData_xccvfug.csv"
csv_path.parent.mkdir(parents=True, exist_ok=True)

df = knoema.get("tsghpfc", timerange="2016M1-2026M12", Indicateurs="011")
df.index.name = "date"
long = df.melt(ignore_index=False, value_name="valeur").reset_index()
long.columns = [str(c).lower() for c in long.columns]
long["date"] = pd.to_datetime(long["date"])
long = long.dropna(subset=["valeur"])
long = long[(long["indicateurs"] == "Produits alimentaires") & (long["date"] >= "2016-01-01")]
if long.empty:
    raise RuntimeError("Aucune donnée 'Produits alimentaires' récupérée depuis Knoema.")

pd.DataFrame(
    {
        "indicateurs": long["indicateurs"],
        "Unit": "",
        "Date": long["date"].dt.year.astype(str) + "M" + long["date"].dt.month.astype(str),
        "Value": long["valeur"].map(lambda v: f"{v:g}"),
    }
).to_csv(csv_path, index=False, quoting=csv.QUOTE_ALL)

con = duckdb.connect(str(root / "entrepot.duckdb"))
con.execute("CREATE SCHEMA IF NOT EXISTS raw")
con.execute(
    "CREATE OR REPLACE TABLE raw.ansd_ihpc AS "
    "SELECT * FROM read_csv(?, all_varchar = true, header = true)",
    [str(csv_path)],
)
con.close()
print("Ingestion ANSD terminée.")
