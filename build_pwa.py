"""Rebuild app icons and a content-versioned offline manifest. Requires Pillow."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw
root=Path(__file__).parent/'dist'
for size in (192,512):
 im=Image.new('RGB',(size,size),'#102e40');d=ImageDraw.Draw(im);s=size/64
 d.ellipse((12*s,12*s,52*s,52*s),outline='#c8e9ef',width=max(2,int(1.2*s)))
 d.polygon([(32*s,14*s),(44*s,46*s),(32*s,39*s),(20*s,46*s)],fill='#3be0bd')
 im.save(root/f'icon-{size}.png')
files=sorted(p for p in root.rglob('*') if p.is_file() and p.name!='sw.js')
digest=hashlib.sha256(b''.join(p.relative_to(root).as_posix().encode()+p.read_bytes() for p in files)).hexdigest()[:14]
assets=['./']+['./'+p.relative_to(root).as_posix() for p in files]
template="""'use strict';
const CACHE=__CACHE__, ASSETS=__ASSETS__;
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
"""
(root/'sw.js').write_text(template.replace('__CACHE__',json.dumps('adria-'+digest)).replace('__ASSETS__',json.dumps(assets)))
print(f'PWA: {len(assets)} cached paths, cache adria-{digest}')
