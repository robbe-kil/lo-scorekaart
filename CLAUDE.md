# LO Scorekaart: afspraken voor Claude

PWA voor de iPhone om leerlingen per LO-oefening te beoordelen. De app wordt gebruikt door een familielid van Robbe, niet door Robbe zelf. Houd de interface eenvoudig en in het Nederlands (Vlaams).

## Opbouw

- Geen build, geen frameworks en geen npm. Alles staat in `index.html` (HTML, CSS en JS inline), plus `sw.js` en `manifest.webmanifest` in de root.
- Externe bibliotheken komen lokaal in `assets/vendor/` (nu alleen jsPDF), nooit via een CDN, want de app moet offline werken.
- Gegevens staan in `localStorage` op het toestel (`lo-db` = `{exercises, students, scores}`). Er is geen server.
- Ingebouwde oefeningen staan in `data/oefeningen.json`. Bij elke start voegt `syncBuiltins()` in `index.html` nieuwe toe en werkt onbewerkte oefeningen bij. Oefeningen die ze zelf bewerkte, en ingebouwde oefeningen die ze verwijderde (`lo-removed`), blijven ongemoeid.
- Screenshots van de rubrieken staan in `docs/rubrieken/<id>.jpg`. Het veld `rubriek` van een oefening verwijst ernaar, en de app toont ze via *Bekijk rubriek*.

## Bij elke wijziging

1. Wijzig je `index.html`, `manifest.webmanifest` of `assets/`? Verhoog dan `VERSION` in `sw.js`. Nieuwe app-bestanden komen ook in `ASSETS`. Voor alleen `data/oefeningen.json` of `docs/` is dat niet nodig.
2. Draai `python3 scripts/check_pwa.py`. Die moet slagen.
3. Test in een browser met Playwright, bij een smal scherm (390 px), en kijk naar fouten in de console.
4. Bestaande gegevens op het toestel mogen nooit verloren gaan. Een wijziging aan de opslag moet oude data automatisch omzetten.
5. Commit met dezelfde auteur als de vorige commit, en schrijf het commitbericht in het Nederlands.

## Nieuwe oefeningen

Gebruik de skill `lo-scorekaart-nieuwe-rubrieken`. Het formaat staat in de README onder *Nieuwe oefeningen toevoegen*.

## Git en token

- Pushen gaat met de credential helper `store --file=.git/lo-credentials`. Toon dat bestand nooit en zet nooit een token in de remote-URL. Filter `github_pat_…` uit alle output.
- In een Cowork-sessie: vraag eerst verwijderrechten voor de repo-map. Anders blijven `.git/*.lock` en `tmp_obj_*` achter.
