const CACHE='tanakh-by-ideas-v3';
const APP='./index.html';
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll([
 './','./index.html','./manifest.webmanifest','./tanakh-ideas-192.png','./tanakh-ideas-512.png'
])).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{
  if(e.request.method!=='GET') return;
  if(e.request.mode==='navigate'){
    e.respondWith(fetch(e.request).catch(()=>caches.match(APP)));
  }
});
