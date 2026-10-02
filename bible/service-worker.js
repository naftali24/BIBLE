const C='the-bible-v5';
self.addEventListener('install',e=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('fetch',e=>{
 if(e.request.method!=='GET')return;
 if(e.request.mode==='navigate'){
   e.respondWith(fetch(e.request).catch(()=>caches.match('./index.html')));
 }
});
