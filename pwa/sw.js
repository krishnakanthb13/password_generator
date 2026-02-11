const CACHE_NAME = 'passforge-v1.1.8';
const CORE_ASSETS = [
    './',
    './index.html',
    './offline.html',
    './css/style.css?v=1.1.8',
    './js/app.js?v=1.1.8',
    './manifest.json',
    './favicon.png',
    './assets/icon-192.png',
    './assets/icon-512.png'
];

const EXTERNAL_ASSETS = [
    'https://unpkg.com/lucide@0.344.0/dist/umd/lucide.min.js',
    'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            // Atomic precaching for core assets
            const corePromise = cache.addAll(CORE_ASSETS);

            // Individual caching for external assets to prevent one failure from blocking all
            const externalPromises = EXTERNAL_ASSETS.map(url =>
                fetch(url).then(response => {
                    if (response.ok) return cache.put(url, response);
                }).catch(err => console.warn(`Failed to cache external asset: ${url}`, err))
            );

            return Promise.all([corePromise, ...externalPromises]);
        })
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.filter(key => key !== CACHE_NAME).map(key => caches.delete(key))
            );
        })
    );
});

self.addEventListener('fetch', (event) => {
    // Only handle GET requests
    if (event.request.method !== 'GET') return;

    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            if (cachedResponse) return cachedResponse;

            return fetch(event.request)
                .then((networkResponse) => {
                    // Runtime caching for external fonts/scripts if they weren't precached
                    if (networkResponse.ok && (event.request.url.includes('fonts.gstatic.com') || event.request.url.includes('unpkg.com'))) {
                        const responseClone = networkResponse.clone();
                        caches.open(CACHE_NAME).then(cache => cache.put(event.request, responseClone));
                    }
                    return networkResponse;
                })
                .catch(() => {
                    // Network failure fallback
                    if (event.request.mode === 'navigate') {
                        return caches.match('./offline.html');
                    }
                    return new Response('Network error occurred', {
                        status: 408,
                        statusText: 'Network error occurred'
                    });
                });
        })
    );
});
