#!/usr/bin/env python3
"""Controleert dat de PWA na een push naar main nog volledig werkt:
elk bestand waarnaar index.html, manifest.webmanifest en sw.js verwijzen moet bestaan."""
import json, re, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
errors = []

def check(path, origin):
    p = path.split("?")[0].split("#")[0]
    if not p or p in ("./", "/") or "${" in p or re.match(r"^(https?:|data:|mailto:)", p):
        return
    if not (root / p).is_file():
        errors.append(f"{origin}: '{path}' bestaat niet")

html = (root / "index.html").read_text(encoding="utf-8")
for ref in re.findall(r'<(?:link|script|img)[^>]+(?:href|src)="([^"]+)"', html):
    check(ref, "index.html")

manifest = json.loads((root / "manifest.webmanifest").read_text(encoding="utf-8"))
for icon in manifest.get("icons", []):
    check(icon["src"], "manifest.webmanifest")

sw = (root / "sw.js").read_text(encoding="utf-8")
m = re.search(r"const ASSETS\s*=\s*\[(.*?)\];", sw, re.S)
if not m:
    errors.append("sw.js: ASSETS-lijst niet gevonden")
else:
    for ref in re.findall(r'"([^"]+)"', m.group(1)):
        check(ref, "sw.js")
if not re.search(r'const VERSION\s*=\s*"[^"]+"', sw):
    errors.append("sw.js: VERSION niet gevonden")

# data/oefeningen.json: geldige oefeningen met criteria en niveaus
ex_path = root / "data" / "oefeningen.json"
if not ex_path.is_file():
    errors.append("data/oefeningen.json bestaat niet")
else:
    try:
        exs = json.loads(ex_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        exs = {}
        errors.append(f"data/oefeningen.json: geen geldige JSON ({e})")
    if not isinstance(exs, dict):
        errors.append("data/oefeningen.json: verwacht een object {id: oefening}")
        exs = {}
    for ex_id, ex in exs.items():
        where = f"data/oefeningen.json › {ex_id}"
        if not re.fullmatch(r"[a-z0-9-]+", ex_id):
            errors.append(f"{where}: id mag enkel kleine letters, cijfers en '-' bevatten")
        if not isinstance(ex, dict) or not str(ex.get("name", "")).strip():
            errors.append(f"{where}: 'name' ontbreekt"); continue
        if ex.get("rubriek"):
            check(ex["rubriek"], where)
        crits = ex.get("criteria")
        if not isinstance(crits, list) or not crits:
            errors.append(f"{where}: geen criteria"); continue
        ids = [c.get("id") for c in crits if isinstance(c, dict)]
        if len(set(ids)) != len(crits):
            errors.append(f"{where}: criterium-id's ontbreken of zijn dubbel")
        for c in crits:
            lv = c.get("levels") if isinstance(c, dict) else None
            if not isinstance(lv, list) or len(lv) != 4:
                errors.append(f"{where} › {c.get('name') if isinstance(c, dict) else c}: verwacht 4 niveaus"); continue
            for l in lv:
                if not isinstance(l.get("points"), (int, float)) or not str(l.get("desc", "")).strip():
                    errors.append(f"{where} › {c.get('name')}: elk niveau heeft 'points' (getal) en 'desc' nodig")
                    break
    if exs:
        print(f"{len(exs)} oefening(en) in data/oefeningen.json gecontroleerd.")

if errors:
    print("PWA-controle mislukt:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("PWA-controle geslaagd: alle bestanden gevonden.")
