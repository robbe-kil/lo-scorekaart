#!/usr/bin/env python3
"""Controleert dat de PWA na een push naar main nog volledig werkt:
elk bestand waarnaar index.html, manifest.webmanifest en sw.js verwijzen moet bestaan."""
import json, re, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
errors = []

def check(path, origin):
    p = path.split("?")[0].split("#")[0]
    if not p or p in ("./", "/") or re.match(r"^(https?:|data:|mailto:)", p):
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

if errors:
    print("PWA-controle mislukt:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
print("PWA-controle geslaagd: alle bestanden gevonden.")
