// Service worker: permite instalar la app y usarla sin conexión.
// Sube el número de versión cuando cambies archivos para forzar la actualización de la caché.
const CACHE = 'carnet-fr-v2';
const ASSETS = ['./', './index.html','./manifest.webmanifest', './icon-192.png', './icon-512.png'];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(async c => {
      await c.addAll(ASSETS);
      // Audios de pronunciación: si algo falla aquí no pasa nada, se guardan al reproducirlos.
      try {
        const list = await (await fetch('./audio/index.json')).json();
        await Promise.all(list.map(f => c.add('./audio/' + f).catch(() => {})));
      } catch (err) {}
    }).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const isPage = req.mode === 'navigate' || url.pathname.endsWith('.html');
  const isFont = /fonts\.(googleapis|gstatic)\.com$/.test(url.hostname);

  if (isPage) {
    // red primero (para recibir actualizaciones); si no hay conexión, la copia guardada
    e.respondWith(
      fetch(req).then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy));
        return res;
      }).catch(() => caches.match(req).then(r => r || caches.match('./index.html')))
    );
  } else if (url.origin === location.origin || isFont) {
    // caché primero; si no está, se descarga y se guarda
    e.respondWith(
      caches.match(req).then(hit => hit || fetch(req).then(res => {
        const copy = res.clone();
        caches.open(CACHE).then(c => c.put(req, copy));
        return res;
      }))
    );
  }
});
