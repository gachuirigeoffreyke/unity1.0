/* UNITY offline cache. Network first, so updates arrive when online; cache when offline. */
const CACHE = "unity-v17";
const FILES = ["./", "index.html", "manifest.webmanifest", "icon.svg", "icon-192.png", "icon-512.png", "inter.woff2",
  "lib/marked.min.js", "lib/katex.min.js",
  "volumes/Mvuke_Programme_Control_Pack.md", "volumes/Mvuke_V01_Foundation_People_Governance.md", "volumes/Mvuke_V04_Sourcing_Growing_Quality.md", "volumes/Mvuke_V05_Products_Pricing.md", "volumes/Mvuke_V06_Marketing_Sales.md", "volumes/Mvuke_V07_Operations_Fulfilment.md", "volumes/Mvuke_V08_Finance_Funding.md", "volumes/Mvuke_V09_Technology.md", "volumes/Mvuke_V11_Group_Merger_Shop.md", "volumes/Planties_Pilot_Holiday_Market_Test.md", "volumes/Planties_R04_Horticulture_Production.md", "volumes/Planties_V00_Overview.md", "volumes/Planties_V06_Marketing_Sales.md", "volumes/Planties_V07_Operations_Fulfilment.md",
  "volumes/THE_FRAME_V0_Navigator.md", "volumes/THE_FRAME_V1_Principles_and_Evidence.md", "volumes/THE_FRAME_V2_Phase_I_120-Day_Build.md",
  "volumes/FSE-C01-Workbench.md", "volumes/FSE-C02a-Python.md", "volumes/FSE-C11a-CSFoundations.md", "volumes/STR-V01-Mechanics-Maths.md"];
self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  const req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== self.location.origin) return;
  e.respondWith(
    fetch(req).then(res => {
      if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); }
      return res;
    }).catch(() => caches.match(req, { ignoreSearch: true }).then(r => r || caches.match("index.html")))
  );
});
