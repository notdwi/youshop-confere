"""Executar com a API local no modo ao vivo. Uma chamada por lote."""
import csv
import argparse
import json
import time
from itertools import groupby
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

parser = argparse.ArgumentParser()
parser.add_argument("--conjunto", choices=["casos", "reserva"], default="casos")
conjunto = parser.parse_args().conjunto

url = "http://127.0.0.1:8000/api/"
with urlopen(url + "demo/", timeout=10) as response:
    if json.load(response)["example"]:
        raise SystemExit("Ative a extração ao vivo para avaliar o modelo.")

with Path(__file__).with_name(f"{conjunto}.tsv").open(encoding="utf-8") as source:
    cases = list(csv.DictReader(source, delimiter="\t"))
passed = 0
for batch, rows in groupby(cases, key=lambda row: row["lote"]):
    rows = list(rows)
    payload = {"scope": "Básico", "discount": 20, "texts": {r["id"]: r["legenda"] for r in rows}}
    req = Request(url + "analises/", json.dumps(payload).encode(), {"Content-Type": "application/json"})
    start = time.monotonic()
    try:
        with urlopen(req, timeout=100) as response:
            data = json.load(response)
    except HTTPError as exc:
        print(batch, "falha HTTP", exc.code, flush=True)
        continue
    results = {item["campaign"]["id"]: item for item in data["results"]}
    print(batch, round(time.monotonic() - start, 2), "s")
    for row in rows:
        item = results[row["id"]]
        actual = [item["status"], item["before"], item["after"]]
        expected = [row["status"], *[None if row[k] == "-" else int(row[k]) for k in ("antes", "depois")]]
        evidence = item["evidence"]
        ok = actual == expected and bool(evidence) and evidence in row["legenda"]
        if batch == "4" and row["id"] == "ana":
            ok &= {d["status"] for d in item["details"]} == {"Compatível", "Impactada"}
        print(row["id"], "OK" if ok else "FALHA", actual, evidence, flush=True)
        passed += ok
print(f"{passed}/{len(cases)}")
raise SystemExit(passed != len(cases))
