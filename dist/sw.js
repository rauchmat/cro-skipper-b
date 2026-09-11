'use strict';
const CACHE="adria-4264fbed054e6c", ASSETS=["./", "./app.js", "./diagrams/cardinal-0.svg", "./diagrams/cardinal-1.svg", "./diagrams/cardinal-2.svg", "./diagrams/cardinal-3.svg", "./diagrams/day-0.svg", "./diagrams/day-1.svg", "./diagrams/day-2.svg", "./diagrams/day-3.svg", "./diagrams/day-4.svg", "./diagrams/signal-0.svg", "./diagrams/signal-1.svg", "./diagrams/signal-2.svg", "./diagrams/signal-3.svg", "./diagrams/signal-4.svg", "./diagrams/signal-5.svg", "./diagrams/signal-6.svg", "./fragenkatalog.json", "./icon-192.png", "./icon-512.png", "./index.html", "./manifest.webmanifest", "./questions.js", "./style.css"];
self.addEventListener('install',event=>event.waitUntil((async()=>{const cache=await caches.open(CACHE);await cache.addAll(ASSETS);await self.skipWaiting();})()));
self.addEventListener('activate',event=>event.waitUntil((async()=>{for(const key of await caches.keys())if(key.startsWith('adria-')&&key!==CACHE)await caches.delete(key);await self.clients.claim();})()));
self.addEventListener('message',event=>{if(event.data?.type==='CHECK_OFFLINE')event.waitUntil((async()=>{const cache=await caches.open(CACHE);const complete=(await Promise.all(ASSETS.map(p=>cache.match(new URL(p,self.registration.scope).href)))).every(Boolean);event.ports[0]?.postMessage({ready:complete});})());});
self.addEventListener('fetch',event=>{
 const url=new URL(event.request.url);
 if(event.request.method!=='GET'||url.origin!==self.location.origin)return;
 const paths=new Set(ASSETS.map(p=>new URL(p,self.registration.scope).pathname));
 if(!paths.has(url.pathname))return;
 if(event.request.mode==='navigate'){
  event.respondWith((async()=>{try{return await fetch(event.request);}catch{const cached=await caches.match(new URL('./index.html',self.registration.scope).href);return cached||new Response('Bitte zuerst online laden.',{status:503,headers:{'Content-Type':'text/plain;charset=utf-8'}});}})());return;
 }
 event.respondWith((async()=>{const cache=await caches.open(CACHE);const cached=await cache.match(event.request);return cached||fetch(event.request);})());
});
