import json, hashlib, random
from pathlib import Path
from html import escape
ROOT=Path(__file__).parent
OUT=ROOT/'dist'
(OUT/'diagrams').mkdir(exist_ok=True)
bank=[]
SOURCES={
 'skript':{'title':'AC Nautik · Boat Skipper B · Skriptum','url':'https://www.kuestenpatent-kroatien.at/Skriptum.pdf'},
 'kvr':{'title':'KVR / COLREG · International Rules (USCG)','url':'https://www.navcen.uscg.gov/navigation-rules-amalgamated'},
 'hr25':{'title':'Kroatien · NN 52/2025 · Art. 49–50','url':'https://narodne-novine.nn.hr/clanci/sluzbeni/2025_03_52_685.html'},
 'hr26':{'title':'Kroatien · Änderung NN 40/2026 · Art. 3','url':'https://narodne-novine.nn.hr/clanci/sluzbeni/full/2026_04_40_495.html'},
 'special':{'title':'Trinity House · Special Marks','url':'https://www.trinityhouse.co.uk/mariners-information/navigation-buoys/special-marks'},
 'sar':{'title':'Kroatische Regierung · Seenotrettung 195','url':'https://gov.hr/en/195-maritime-search-and-rescue-service/1188'},
 'dsc':{'title':'ITU-R M.541-11 · DSC-Verfahren','url':'https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.541-11-202311-I!!PDF-E.pdf'}
}
def add(topic,page,q,a,e,wrong=None,**kw):
 ident='q-'+hashlib.sha256(q.encode()).hexdigest()[:10]
 rec=dict(id=ident,topic=topic,page=int(page),question=q,answer=a,explanation=e,type='choice' if wrong else 'open',difficulty='Anwendung' if any(s in q.lower() for s in ['warum','du ','übung','formuliere','praktische','welchen kompass','wie lange','wie weit','welcher kompass']) else 'Grundwissen',sample=int(page)>=60,sources=['skript'])
 if wrong:rec['options']=[a,*wrong]
 rec.update(kw);bank.append(rec);return rec
for line in (ROOT/'bank.txt').read_text().splitlines():
 if line.startswith('@'):topic=line[1:];continue
 if not line:continue
 parts=line.split('|');assert len(parts) in [4,5],line
 page,q,a,e=parts[:4]
 r=add(topic,page,q,a,e,parts[4].split(';') if len(parts)==5 else None)
 if topic in ['Lichterführung','Ausweichregeln','Schallsignale']:r['sources'].append('kvr')
 if topic=='Vorschriften' and int(page)==51:r.update(sources=['skript','hr25']+(['hr26'] if 'Badebereich' in q else []),note='Aktualisiert gegenüber dem Skript: aktuelle kroatische Abstands-/Geschwindigkeitsregeln, geprüft am 11.09.2026. Für Prüfungsunterschiede die Kursleitung ansprechen.')
 if topic=='Ausrüstung':r['note']='Skript-Lernstoff. Die alte Ausrüstungsliste ist keine vollständig auf heutigen Rechtsstand geprüfte Checkliste; Bootszulassung und aktuelle Flaggenstaat-Regeln sind maßgebend.'
 if 'gelbes Sonderzeichen' in q:r.update(sources=['skript','special'],note='Korrektur: Ein gelbes Sonderzeichen bedeutet nicht allgemein „neue Gefahr“.')
 if 'Telefonnummern' in q:r['sources'].append('sar')
 if 'DSC' in q or 'MMSI' in q:r['sources'].append('dsc')
 for fragment,note in {
  'Rot über Grün am Mast':'Korrektur: Die zusätzlichen Segler-Rundumlichter sind optional, nicht erst ab 20 m vorgeschrieben.',
  'Lotsenfahrzeug im Lotsendienst':'Korrektur: Ein Lotsenfahrzeug im Lotsendienst führt die Sonderlichter anstelle normaler Maschinenfahrzeug-Topplichter.',
  'Pfeife, Glocke':'Aktualisierung: Glocke ab 20 m; das Skript nennt veraltet 12 m.',
  'Fähren haben immer':'Korrektur: Es gibt in den KVR keinen pauschalen Fährenvorrang. Örtliche Vorschriften können zusätzliche Regeln enthalten.',
  'DSC korrekt':'Korrektur eines Begriffsfehlers im Skript.',
  'Wann ist MAYDAY':'Präzisierung: Nicht erforderlich ist, dass gleichzeitig Mannschaft UND Schiff gefährdet sind.',
  'Was bedeutet Quebec':'Präzisierung der im Skript verkürzten Flaggenbedeutung.',
  'feste Wellenhöhe':'Die Beaufort-/Wellentabelle des Skripts wird nicht als feste Zuordnung übernommen.'
 }.items():
  if fragment in q:r['note']=note

alphabet='Alfa Bravo Charlie Delta Echo Foxtrot Golf Hotel India Juliett Kilo Lima Mike November Oscar Papa Quebec Romeo Sierra Tango Uniform Victor Whiskey X-ray Yankee Zulu'.split()
for i,word in enumerate(alphabet):
 letter=chr(65+i)
 wrong=[alphabet[(i+n)%26] for n in [3,8,17]]
 add('Funkalphabet',40,f'Wie buchstabierst du den Buchstaben {letter} im internationalen Funkalphabet?',word,f'{letter} wird mit {word} eindeutig übertragen. Auch ohne Auswahlmöglichkeiten laut üben.',wrong,sample=letter in 'KRCA FHM'.replace(' ',''))
terms=[('cv','Knoten','Geschwindigkeitseinheit: Seemeilen pro Stunde.'),('M','Seemeile','Einheit der nautischen Entfernung.'),('Var','Missweisung','Magnetische Korrektur, deren Bezugsjahr wichtig ist.'),('B','Weiß','Bei Leuchtfeuerkennungen die Farbe Weiß.'),('Z','Grün','Nicht mit Ž für Gelb verwechseln.'),('Ž','Gelb','Das diakritische Zeichen unterscheidet Gelb von Grün.'),('C','Rot','Eine Farbangabe, beispielsweise in einer Feuerkennung.'),('Cr','Schwarz','Bei Seezeichen etwa zusammen mit Gelb verwendet.'),('Pl','Blau','Die genaue Schrift und Legende der Karte beachten.'),('Or','Orange','Kroatische Farbbezeichnung.'),('Lj','Violett','Kroatische Farbbezeichnung.'),('Gr','Riff','Kennzeichnet eine mögliche Navigationsgefahr.'),('Hr','Fels','Tiefen und weitere Symbole bestimmen die Gefahr.'),('Bk','Riff','Die konkrete Kartenlegende ist maßgebend.'),('Plic','Untiefe','Mit Tiefgang und Sicherheitsreserve abgleichen.'),('L','Hafen','Kroatisch Luka.'),('O','Insel','Kroatisch Otok.'),('U','Bucht','Kroatisch Uvala.'),('k','Steine','Beschaffenheit des Grundes.'),('p','Sand','Beschaffenheit des Grundes.'),('m','Schlamm','Beschaffenheit des Grundes.'),('s','Kies','Beschaffenheit des Grundes.')]
for i,(term,answer,exp) in enumerate(terms):
 pool=list(dict.fromkeys(a for _,a,_ in terms if a!=answer));rng=random.Random(term);rng.shuffle(pool)
 add('Seekarte & Leuchtfeuer',59,f'Was bedeutet „{term}“ in der Abkürzungsliste kroatischer Seekarten?',answer,exp,pool[:3])
glossary=[('Backbord','Linke Schiffsseite in Blickrichtung zum Bug.'),('Steuerbord','Rechte Schiffsseite in Blickrichtung zum Bug.'),('Bug','Vorderer Teil des Bootes.'),('Achtern','Hinten bzw. im hinteren Bereich des Bootes.'),('Luv','Die dem Wind zugewandte Seite.'),('Lee','Die dem Wind abgewandte Seite.'),('Schot','Leine zum Einstellen bzw. Trimmen eines Segels.'),('Fall','Leine zum Setzen oder Bergen eines Segels.'),('Koje','Schlafplatz an Bord.'),('Bändsel','Kurzes dünnes Tauwerk zum Binden oder Sichern.'),('Winsch','Winde zum Holen und Halten belasteter Leinen.'),('Kajüte','Raum unter Deck.'),('Cockpit','Arbeits- und Sitzbereich, von dem aus das Boot bedient wird.'),('Pantry','Küche an Bord.'),('Bilge','Tiefer Innenbereich des Rumpfes, in dem sich Wasser sammeln kann.'),('Poller','Fester Pfosten zum Belegen von Leinen.'),('Klampe','Beschlag mit Hörnern zum Belegen von Tauwerk.'),('Fender','Schutzpolster zwischen Boot und Liegeplatz bzw. Nachbarboot.'),('Impeller','Flügelrad, beispielsweise in einer Seewasserpumpe.')]
for term,answer in glossary:
 rec=add('Seemanns ABC',58,f'Was bedeutet der seemännische Begriff „{term}“?',answer,'Erkläre den Begriff zusätzlich mit einem Beispiel an Bord.')
 if term in ['Winsch','Schot','Fall']:rec['note']='Begriff präzisiert: Die stark vereinfachte Definition im Skript ist nicht allgemein ausreichend.'

def svg(name,body,day=False):
 data=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 260"><rect width="400" height="260" rx="16" fill="{"#eaf3f6" if day else "#10222f"}"/>{body}</svg>'
 (OUT/'diagrams'/f'{name}.svg').write_text(data)
 return 'diagrams/'+name+'.svg'
lights=[(['white','red'],'Lotsenfahrzeug im Lotsendienst',26),(['green','white'],'Trawlender Fischer',26),(['red','white'],'Nichttrawlender Fischer',27),(['red','red'],'Manövrierunfähiges Fahrzeug',28),(['red','white','red'],'Manövrierbehindertes Fahrzeug',29),(['red','red','red'],'Tiefgangbehindertes Maschinenfahrzeug',29),(['red','green'],'Segelfahrzeug unter Segeln mit optionalen Zusatzlichtern',24)]
colors={'red':'#ff515a','green':'#39e49d','white':'#ffffff'}
german={'red':'Rot','green':'Grün','white':'Weiß'}
for i,(cs,a,page) in enumerate(lights):
 body=''.join(f'<circle cx="200" cy="{65+n*62}" r="17" fill="{colors[c]}"/><text x="233" y="{71+n*62}" fill="#b7ccd7" font-family="sans-serif" font-size="15">{german[c]}</text>' for n,c in enumerate(cs))
 path=svg('signal-'+str(i),body)
 add('Lichterführung',page,'Welches Fahrzeug kennzeichnet diese Kombination von Sonderlichtern? ('+str(i+1)+')',a,'Gezeigt sind nur die Sonderlichter, nicht das vollständige Lichterbild. Zusätzliche Lichter hängen von Fahrtzustand und Fahrzeug ab.',[x[1] for j,x in enumerate(lights) if j!=i][:3],image=path,alt='Senkrechte Sonderlichter: '+' über '.join(german[c] for c in cs),sources=['skript','kvr'],difficulty='Bilderkennung',imageCaption='Nur Sonderlichter · keine vollständige Schiffsansicht')
def shape(kind,y):
 if kind=='ball':return f'<circle cx="200" cy="{y}" r="19" fill="#172735"/>'
 if kind=='diamond':return f'<path d="M200 {y-23} L220 {y} L200 {y+23} L180 {y}Z" fill="#172735"/>'
 return f'<rect x="182" y="{y-25}" width="36" height="50" fill="#172735"/>'
days=[(['ball'],'Ankerlieger',27),(['ball','ball'],'Manövrierunfähiges Fahrzeug',28),(['ball','diamond','ball'],'Manövrierbehindertes Fahrzeug',29),(['ball','ball','ball'],'Fahrzeug auf Grund',28),(['cylinder'],'Tiefgangbehindertes Maschinenfahrzeug',29)]
for i,(ss,a,page) in enumerate(days):
 path=svg('day-'+str(i),''.join(shape(s,55+n*65) for n,s in enumerate(ss)),True)
 add('Lichterführung',page,f'Welche Bedeutung hat dieses Tagzeichen? ({i+1})',a,'Tagzeichen sind schwarze Signalkörper. Die hier gezeigte Kombination kennzeichnet den Zustand des Fahrzeugs.',[x[1] for j,x in enumerate(days) if j!=i][:3],image=path,alt='Tagzeichen: '+' – '.join({'ball':'Ball','diamond':'Rhombus','cylinder':'Zylinder'}[s] for s in ss),sources=['skript','kvr'],difficulty='Bilderkennung',day=True)
cards=[('Nord',['#162633','#f4cc31'],[1,1]),('Ost',['#162633','#f4cc31','#162633'],[1,-1]),('Süd',['#f4cc31','#162633'],[-1,-1]),('West',['#f4cc31','#162633','#f4cc31'],[-1,1])]
for i,(d,cols,dirs) in enumerate(cards):
 body='<path d="M140 226 H260" stroke="#52778c" stroke-width="3"/>'
 for n,c in enumerate(cols):body+=f'<rect x="184" y="{115+n*100/len(cols)}" width="32" height="{100/len(cols)}" fill="{c}"/>'
 for n,dr in enumerate(dirs):
  y=37+n*35
  body+=f'<path d="M182 {y+15*dr} L218 {y+15*dr} L200 {y-15*dr}Z" fill="#162633"/>'
 path=svg('cardinal-'+str(i),body,True)
 add('Seezeichen',21,f'Auf welcher Seite dieses Kardinalzeichens liegt das sichere Wasser? ({i+1})',d+'lich des Zeichens.' if d!='Ost' else 'Östlich des Zeichens.','Name, Kegel und Farbbänder des Kardinalzeichens zeigen die geografische Passierseite an.',image=path,alt='Kardinalzeichen mit zwei Kegeln und schwarz-gelben Farbbändern.',difficulty='Bilderkennung',day=True)
# Normalize umlauts in generated compass answers.
for r in bank:
 if r['answer']=='Südlich des Zeichens.':pass
 if r['answer']=='Nordlich des Zeichens.':r['answer']='Nördlich des Zeichens.'
 if r['answer']=='Westlich des Zeichens.':pass
for i,(q,a,exp) in enumerate([
 ('Buchstabiere den Bootsnamen ADRIA.','Alfa – Delta – Romeo – India – Alfa.','Sprich langsam und trenne die einzelnen Wörter klar.'),
 ('Buchstabiere das Rufzeichen OEX.','Oscar – Echo – X-ray.','Rufzeichen nicht durch einen Bootsnamen ersetzen.'),
 ('Buchstabiere den Ortsnamen RIJEKA.','Romeo – India – Juliett – Echo – Kilo – Alfa.','Juliett und Alfa sind die standardisierten Schreibweisen.'),
 ('Gib die Position 45° 23′ N, 014° 35′ E in einer englischen Übungsmeldung an.','Four five degrees two three minutes north; zero one four degrees three five minutes east.','Nord und Ost sowie Grad und Minuten ausdrücklich nennen.')]):add('Funk & Flaggen',41,q,a,exp,difficulty='Anwendung')
assert len({r['id'] for r in bank})==len(bank)
for r in bank:
 if r['type']=='choice':assert len(r['options'])==4 and len(set(r['options']))==4,r
payload={'version':1,'reviewed':'2026-09-11','questions':bank,'sources':SOURCES}
(OUT/'questions.js').write_text('window.ADRIA_BANK='+json.dumps(payload,ensure_ascii=False,separators=(',',':'))+';\n')
(OUT/'fragenkatalog.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2))
from collections import Counter
print(json.dumps({'total':len(bank),'images':sum('image' in r for r in bank),'choices':sum(r['type']=='choice' for r in bank),'topics':dict(Counter(r['topic'] for r in bank))},ensure_ascii=False))
