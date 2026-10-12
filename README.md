# LO Scorekaart

Een app voor op de iPhone om leerlingen per LO-oefening te beoordelen. Je installeert ze als PWA vanaf GitHub Pages.

## Online zetten op GitHub Pages

1. Ga naar https://github.com/new
   - Repository name: `lo-scorekaart`
   - Kies **Public**
   - Klik op **Create repository**
2. Klik op **uploading an existing file**.
3. Sleep de volledige inhoud van deze map in het venster: `index.html`, `manifest.webmanifest`, `sw.js`, `README.md` en de mappen `icons` en `vendor`.
4. Klik op **Commit changes**.
5. Ga naar **Settings → Pages**.
   - Source: **Deploy from a branch**
   - Branch: **main**, map: **/ (root)**
   - Klik op **Save**
6. Na ongeveer een minuut staat de app online op `https://<jouw-gebruikersnaam>.github.io/lo-scorekaart/`.

Werk je liever met de Terminal op je Mac:

```bash
cd "~/Projects/Lichamelijke opvoeding/lo-scorekaart-pwa"
git init -b main
git add .
git commit -m "LO Scorekaart PWA"
git remote add origin https://github.com/<jouw-gebruikersnaam>/lo-scorekaart.git
git push -u origin main
```

Daarna schakel je Pages in zoals in stap 5.

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
2. Verhoog `VERSION` in `sw.js`, bijvoorbeeld van `lo-scorekaart-v1` naar `lo-scorekaart-v2`.
3. Upload of push de bestanden opnieuw.

De iPhone haalt de nieuwe versie op zodra je de app opent terwijl je internet hebt.
