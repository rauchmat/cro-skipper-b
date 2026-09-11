import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const dist=path.join(root,'dist');
const B=JSON.parse(fs.readFileSync(path.join(dist,'fragenkatalog.json'),'utf8'));
assert.equal(B.questions.length,308);assert.equal(new Set(B.questions.map(q=>q.id)).size,308);
for(const q of B.questions){assert.ok(q.question&&q.answer&&q.explanation&&q.topic);assert.ok(q.page>=5&&q.page<=64);for(const s of q.sources)assert.ok(B.sources[s]);if(q.options){assert.equal(q.options.length,4);assert.equal(new Set(q.options).size,4);assert.equal(q.options.filter(o=>o===q.answer).length,1);}if(q.image)assert.ok(fs.existsSync(path.join(dist,q.image)));}
const html=fs.readFileSync(path.join(dist,'index.html'),'utf8');
for(const match of html.matchAll(/(?:src|href)="\.\/([^"#]+)"/g))assert.ok(fs.existsSync(path.join(dist,match[1])),match[1]);
const manifest=JSON.parse(fs.readFileSync(path.join(dist,'manifest.webmanifest'),'utf8'));for(const icon of manifest.icons)assert.ok(fs.existsSync(path.join(dist,icon.src)));
const storage=new Map();let nodes=[],tools=[];
function element(attrs=''){const n={style:{},dataset:{},focus(){},click(){return this.onclick?.({preventDefault(){}});},textContent:'',value:'',files:[]};for(const a of attrs.matchAll(/([\w-]+)(?:="([^"]*)")?/g)){const [_,key,v='']=a;if(key.startsWith('data-'))n.dataset[key.slice(5)]=v;else n[key]=v;}return n;}
const app=element();Object.defineProperty(app,'innerHTML',{get(){return this.html||'';},set(html){this.html=html;nodes=[];for(const m of html.matchAll(/<(button|input|textarea|select|h1)\b([^>]*)>/g)){const n=element(m[2]);n.tag=m[1];nodes.push(n);}const c=nodes.find(n=>n.id==='examCount');if(c)c.value='20';}});
const fixed={app,notice:element(),connection:element(),brand:element(),infoBtn:element()};
const document={getElementById:id=>fixed[id],querySelector(s){if(s.startsWith('#'))return fixed[s.slice(1)]||nodes.find(n=>n.id===s.slice(1))||null;if(s==='main h1')return nodes.find(n=>n.tag==='h1');return null;},querySelectorAll(s){const m=s.match(/^\[data-(.+)\]$/);return m?nodes.filter(n=>m[1]in n.dataset):[];},modelContext:{registerTool(t){tools.push(t);}}};
const window={ADRIA_BANK:B,addEventListener(){},scrollTo(){}};
const context={window,document,navigator:{onLine:true},localStorage:{getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)},confirm:()=>true,location:{origin:'https://example.test',pathname:'/cro-skipper-b/'},setTimeout:()=>0,clearTimeout(){},console,Date,URL,Blob};vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(dist,'app.js'),'utf8'),context);
const c=window.AdriaCore;assert.ok(c);assert.ok(app.innerHTML.includes('308 Fragen'));
for(let i=0;i<100;i++){const session=c.makeSession('exam',B.questions,20);assert.equal(session.ids.length,20);assert.equal(new Set(session.ids).size,20);const count={};for(const id of session.ids){const q=B.questions.find(q=>q.id===id);count[q.topic]=(count[q.topic]||0)+1;}assert.equal(Object.keys(count).length,15);assert.ok(Math.max(...Object.values(count))<=2);}
assert.throws(()=>c.validCards({[B.questions[0].id]:{last:7}}));
const id=B.questions[0].id;c.record(id,1);c.record(id,1);assert.equal(c.getData().cards[id].streak,2);c.record(id,0);assert.equal(c.getData().cards[id].streak,0);
c.start('quick');let s=c.getData().session,q=B.questions.find(q=>q.id===s.ids[0]);c.commitRating(s,q,1);let attempts=c.getData().cards[q.id].attempts;c.commitRating(s,q,0);assert.equal(c.getData().cards[q.id].attempts,attempts);
// Walk an entire exam through the actual UI callbacks; no solutions during answering.
c.start('exam',null,20);s=c.getData().session;
while(s.phase==='answer'){
 assert.ok(!app.innerHTML.includes('Musterantwort'));q=B.questions.find(q=>q.id===s.ids[s.pos]);
 if(q.options){const i=s.orders[q.id].indexOf(q.answer);document.querySelectorAll('[data-option]').find(b=>Number(b.dataset.option)===i).onclick();}
 else document.querySelector('#written').oninput({target:{value:'Meine selbst formulierte Testantwort'}});
 document.querySelector('#next').onclick();
}
assert.equal(s.phase,'review');let reviewed=0;while(s.phase==='review'){assert.ok(app.innerHTML.includes('Musterantwort'));document.querySelectorAll('[data-score]').find(n=>n.dataset.score==='1').onclick();reviewed++;assert.ok(reviewed<21);}
assert.equal(s.phase,'result');assert.ok(app.innerHTML.includes('100'));assert.equal(s.ids.reduce((n,id)=>n+s.responses[id].score,0),20);assert.ok(c.sessionValid(JSON.parse(storage.get('adria-progress-v1')).session));
// Oral mode must suppress choices even for a choice-only pool.
c.getData().session=null;c.start('oral','Funkalphabet',1);assert.equal(document.querySelectorAll('[data-option]').length,0);assert.ok(document.querySelector('#reveal'));document.querySelector('#reveal').onclick();assert.ok(app.innerHTML.includes('Musterantwort'));document.querySelectorAll('[data-score]').find(n=>n.dataset.score==='0.5').onclick();document.querySelector('#continue').onclick();assert.equal(c.getData().session.phase,'result');
// Import validation strips unknown IDs and rejects malformed values; current data unchanged.
const before=JSON.stringify(c.getData());assert.throws(()=>c.validCards({[id]:{last:0,attempts:-1,streak:0,due:0,lastAt:0}}));assert.equal(JSON.stringify(c.getData()),before);
assert.equal(tools.length,1);assert.throws(()=>tools[0].execute({topic:'not-a-topic'}));assert.equal(JSON.stringify(c.getData()),before);tools[0].execute({topic:'Navigation',count:3});assert.equal(c.getData().session.ids.length,3);assert.throws(()=>tools[0].execute({count:3}));
// Offline manifest includes every served local resource; parse SW and validate install cache.
let handlers={};let cached=[];const fakeCache={async addAll(a){cached=[...a];},async match(){return {ok:true};}};
const swContext={self:{addEventListener:(n,f)=>handlers[n]=f,skipWaiting:async()=>{},registration:{scope:'https://example.test/cro-skipper-b/'},clients:{claim:async()=>{}},location:{origin:'https://example.test'}},caches:{open:async()=>fakeCache,keys:async()=>[],delete:async()=>{},match:async()=>({ok:true})},URL,Response,fetch:async()=>({ok:true})};vm.runInNewContext(fs.readFileSync(path.join(dist,'sw.js'),'utf8'),swContext);let work;handlers.install({waitUntil:p=>work=p});await work;for(const asset of cached)assert.ok(asset==='./'||fs.existsSync(path.join(dist,asset)),asset);let ready=false;handlers.message({data:{type:'CHECK_OFFLINE'},ports:[{postMessage:r=>ready=r.ready}],waitUntil:p=>work=p});await work;assert.ok(ready);assert.equal(cached.length,25);
console.log('PASS: 308 questions, assets, 100 balanced exams, complete exam/review flow, oral mode, persistence, duplicate-rating guard, import validation, optional agent action and offline cache manifest.');
