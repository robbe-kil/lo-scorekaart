// Service worker: bewaart de app offline.
// Verhoog VERSION bij elke release; de check-workflow op GitHub controleert dat elk bestand in ASSETS bestaat.
const VERSION = "lo-scorekaart-v3";
const ASSETS = [
  "./",
  "index.html",
  "manifest.webmanifest",
  "assets/vendor/jspdf.umd.min.js",
  "assets/icons/apple-touch-icon.png",
  "assets/icons/icon-192.png",
  "assets/icons/icon-512.png",
  "assets/icons/icon-maskable-512.png",
  "assets/icons/icon.svg"
];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(VERSION).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(ks => Promise.all(ks.filter(k => k !== VERSION).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  const url = new URL(e.request.url);
  if (url.origin !== location.origin) return;

  // Pagina: eerst netwerk (nieuwste versie), anders de bewaarde kopie.
  if (e.request.mode === "navigate") {
    e.respondWith(fetch(e.request)
      .then(r => { const c = r.clone(); caches.open(VERSION).then(x => x.put("index.html", c)); return r; })
      .catch(() => caches.match("index.html")));
    return;
  }

  // Overige bestanden: meteen uit de cache, en op de achtergrond verversen.
  // Zo komt een nieuwe versie ook binnen als VERSION eens vergeten werd.
  e.respondWith(caches.open(VERSION).then(cache => cache.match(e.request).then(hit => {
    const net = fetch(e.request).then(r => { if (r.ok) cache.put(e.request, r.clone()); return r; }).catch(() => hit);
    return hit || net;
  })));
});
