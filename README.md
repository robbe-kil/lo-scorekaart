# LO Scorekaart

Een app voor op de iPhone om leerlingen per LO-oefening te beoordelen. Je installeert ze als PWA vanaf GitHub Pages.

## Mapstructuur

```
lo-scorekaart/
├── index.html              # de app (moet in de root blijven)
├── manifest.webmanifest    # PWA-instellingen (naam, kleuren, iconen)
├── sw.js                   # service worker: offline werken (moet in de root blijven)
├── .nojekyll               # GitHub Pages serveert alles zoals het is
├── assets/
│   ├── icons/              # app-iconen
│   └── vendor/             # externe bibliotheken (jsPDF + licentie)
├── docs/
│   └── rubrieken/          # bronbeoordelingen per oefening (niet in de app geladen)
│       └── koprol-voorwaarts.jpg
├── scripts/
│   └── check_pwa.py        # controleert dat alle bestanden van de PWA bestaan
└── .github/workflows/
    └── check-pwa.yml       # voert die controle uit bij elke push naar main
```

`index.html`, `manifest.webmanifest` en `sw.js` blijven in de root: GitHub Pages serveert de app vanaf de root van `main`, en een service worker kan alleen de map waarin hij staat (en alles daaronder) beheren.

## Online (GitHub Pages)

De app staat online op https://robbe-kil.github.io/lo-scorekaart/ en wordt gepubliceerd vanaf **Settings → Pages → Deploy from a branch → main → / (root)**. Elke push naar `main` zet de nieuwe versie automatisch online.

Bij elke push naar `main` draait ook de workflow **PWA-controle** (tabblad *Actions*). Die faalt als `index.html`, `manifest.webmanifest` of `sw.js` verwijst naar een bestand dat niet bestaat, en geeft een waarschuwing als je app-bestanden wijzigde zonder `VERSION` in `sw.js` te verhogen. Je kan de controle ook lokaal draaien:

```bash
python3 scripts/check_pwa.py
```

## Installeren op de iPhone

1. Open de link in **Safari**.
2. Tik op **Deel** (het vierkantje met de pijl).
3. Kies **Zet op beginscherm** en tik op **Voeg toe**.

De app opent dan schermvullend en werkt ook zonder internet.

## Gegevens

- Alles wordt als JSON bewaard op het toestel zelf (in `localStorage`). Er gaat niets naar een server.
- De gegevens worden niet gedeeld tussen je iPhone, je Mac of de versie in Claude.
- Neem regelmatig een back-up via **Oefeningen → Exporteer JSON**. Met **Importeer JSON** zet je die terug, of breng je scores over van een ander toestel.
- Wis je de websitegegevens van Safari of verwijder je de app van je beginscherm, dan verdwijnen ook de scores.

## Een nieuwe versie uitrollen

1. Pas de bestanden aan.
2. Voeg je een nieuw bestand toe dat de app nodig heeft (bv. een icoon), zet het dan ook in de `ASSETS`-lijst in `sw.js`.
3. Verhoog `VERSION` in `sw.js`, bijvoorbeeld van `lo-scorekaart-v3` naar `lo-scorekaart-v4`.
4. Push naar `main` en kijk in *Actions* of de PWA-controle groen is.

De iPhone haalt de nieuwe versie op zodra je de app opent terwijl je internet hebt. Vergeet je `VERSION` eens, dan worden gewijzigde bestanden toch op de achtergrond ververst en zie je ze bij de volgende keer openen.
