"""Build the atlas and an explicit coverage ledger without editing source applications."""
import json, re, hashlib, unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
HERE=ROOT/'geography'
SOURCES=json.loads((HERE/'sources.json').read_text())
BOOKS=dict(zip('בראשית|שמות|ויקרא|במדבר|דברים|יהושע|שופטים|שמואל א|שמואל ב|מלכים א|מלכים ב|ישעיהו|ירמיהו|יחזקאל|הושע|יואל|עמוס|עובדיה|יונה|מיכה|נחום|חבקוק|צפניה|חגי|זכריה|מלאכי|תהילים|משלי|איוב|שיר השירים|רות|איכה|קהלת|אסתר|דניאל|עזרא|נחמיה|דברי הימים א|דברי הימים ב'.split('|'),'Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|1 Samuel|2 Samuel|1 Kings|2 Kings|Isaiah|Jeremiah|Ezekiel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|Haggai|Zechariah|Malachi|Psalms|Proverbs|Job|Song of Songs|Ruth|Lamentations|Ecclesiastes|Esther|Daniel|Ezra|Nehemiah|1 Chronicles|2 Chronicles'.split('|')))
def norm(s):return ''.join(c for c in unicodedata.normalize('NFD',s) if c.isalnum())
def chapter(book,n):return json.loads((ROOT/book/f'chapter_{n:03}'/'chapter.json').read_text())
def bible_source(alias,item):
 parts=alias.split(':');ch,v=(map(int,parts[1:]) if len(parts)==3 else (item['chapter'],item['verse']))
 b={'bible':'בראשית','bibleNum':'במדבר','bibleChr':'דברי הימים ב','bibleJosh':'יהושע'}[parts[0]]
 return f'https://www.sefaria.org/{BOOKS[b].replace(" ","_")}.{ch}.{v}?lang=bi'
all_items=[]
for line in (HERE/'events.txt').read_text().splitlines():
 if not line.strip():continue
 if line.startswith('@'):
  ref,he,en,key=line[1:].split('|');ch,v=map(int,ref.split(':'))
  item={'id':f'gen-{ch}-{v}-{key}','book':'בראשית','chapter':ch,'verse':v,'title':{'he':he,'en':en},'placeKey':key,'facts':[]};all_items.append(item)
 else:
  kind,he,en,source=line.split('|')
  item['facts'].append({'type':kind,'he':he,'en':en,'source':bible_source(source,item) if source.startswith('bible') else SOURCES[source]})
# Explicit editorial corrections after source comparison.
for it in all_items:
 if it['placeKey']=='on':
  it['facts'][4]['he']=it['facts'][4]['he'].replace('הלიოפוליס','הליופוליס')
 if it['placeKey']=='jabbok':
  it['facts'][3]={'type':'F','he':'הנהר מגיע אל הירדן מדרום לשפך הירמוך ומצפון לים המלח.','en':'The river reaches the Jordan south of the Yarmuk confluence and north of the Dead Sea.','source':SOURCES['jordan']}
 if it['placeKey']=='gerarWells':
  it['facts'][1]={'type':'U','he':'הקישור בין נחל גרר המודרני לנחל שבבראשית הוא משוער, גם אם שניהם במערב הנגב.','en':'Equating modern Nahal Gerar with Genesis’s valley is tentative, even though both belong to the western Negev.','source':'https://www.kkl.org.il/travel/trips/1838/'}
 if it['placeKey']=='ur':
  it['facts'][0]['source']='https://classic.net.bible.org/dictionary.php?word=Ur'
  it['facts'][3]={'type':'F','he':'במרגלות הזיקורת נמצאו שברי לבנים מזוגגות מן המקדש שבראשה, המתוארכים לתקופה הבבלית המאוחרת.','en':'Glazed brick fragments from the ziggurat’s summit shrine were found at its foot and date to the Late Babylonian period.','source':'https://www.britishmuseum.org/collection/object/W_1924-0920-242'}
  it['facts'][4]['source']='https://www.metmuseum.org/art/collection/search/322903'
 if it['placeKey']=='bethlehem':
  it['facts'][3]={'type':'F','he':'בבתיר, ממערב לבית לחם, השתמרו מדרגות אבן ותעלות השקיה הניזונות ממעיינות.','en':'At Battir west of Bethlehem, stone terraces and spring-fed irrigation channels survive.','source':SOURCES['bethlehemLandscape']}
 if it['placeKey']=='on':
  it['facts'][2]={'type':'F','he':'הליופוליס הייתה מרכז דתי חשוב; חפירות המשלחת האיטלקית נערכו בה בשנים 1903–1906.','en':'Heliopolis was a major religious centre; the Italian mission excavated there in 1903–1906.','source':SOURCES['on']}
  it['facts'][3]={'type':'F','he':'המחקר משווה מפות ותיעוד חפירות ישן עם שכונות קהיר המכסות כיום את האתר.','en':'Research compares historical excavation records and maps with Cairo neighbourhoods now covering the site.','source':SOURCES['on']}
 if it['placeKey']=='edom':
  it['facts'][3]={'type':'F','he':'באזור פינאן שבערבה הירדנית התגלו מכרות, סיגים ואתרי הפקת נחושת קדומים.','en':'The Faynan region of Jordan’s Arabah contains mines, slag and ancient copper-production sites.','source':SOURCES['copper']}
# Withdraw inadequate candidate; retained in the ledger, never padded.
pending=[];items=[]
for it in all_items:
 if it['placeKey']=='atad':
  pending.append({'id':it['id'],'book':it['book'],'chapter':it['chapter'],'verse':it['verse'],'title':it['title'],'reason':{'he':'אין שש עובדות גיאוגרפיות עצמאיות; רוב הטיוטה עוסקת במגבלות הזיהוי.','en':'Six independent geographical facts are not available; most draft lines concern identification limits.'}});continue
 c=chapter(it['book'],it['chapter']);it['quote']={'he':c['verses'][it['verse']-1],'en':c['english'][it['verse']-1]}
 it['era']={'he':'מסורת האבות — ללא תיארוך מוסכם' if it['chapter']>=12 else 'מסורות ראשית — ללא תיארוך מוסכם','en':'Patriarchal tradition — no agreed dating' if it['chapter']>=12 else 'Primeval traditions — no agreed dating'}
 p=ROOT/it['book']/f"chapter_{it['chapter']:03}"/'images';files=sorted(p.glob('*'))
 matches=[f for f in files if (m:=re.search(r'_v(\d+)-(\d+)',f.name)) and int(m[1])<=it['verse']<=int(m[2])]
 chosen=(matches or files)[0]
 # A generated map in the legacy Sidon illustration has unverified labels: exclude it.
 if it['placeKey']=='sidon':chosen=ROOT/'בראשית/chapter_010/images/idea_03_v8-12.jpg'
 it['image']={'src':str(chosen.relative_to(ROOT)),'kind':'artistic','caption':{'he':f"איור אמנותי לפרק בראשית {it['chapter']} בלבד. הנוף והמבנים אינם תיעוד מזוהה של {it['title']['he'].split(' — ')[0]}.",'en':f"Artistic illustration for Genesis {it['chapter']} only. Its landscape and buildings are not identified views of {it['title']['en'].split(':')[0]}."}}
 it['audio']={'en':{'url':c.get('audio_en_url','')}}
 times=c.get('times_en',[])
 if times and it['verse']<=len(times):
  t=times[it['verse']-1];it['audio']['en'].update(start=t.get('start'),end=t.get('end'))
 try:
  raw=json.loads((p.parent/'readalong_words.json').read_text());words=raw.get('words',[])
  # Exact canonical-verse string matching; never guess adjacent verse timings.
  ws=[];stream='';offset=[0]
  for w in words:
   h=norm(str(w.get('hebrew',w.get('h',''))));
   if not h:continue
   ws.append(w);stream+=h;offset.append(len(stream))
  target=norm(it['quote']['he']);at=stream.find(target)
  if at>=0 and at in offset and at+len(target) in offset:
   a=offset.index(at);b=offset.index(at+len(target));w1,w2=ws[a],ws[b-1]
   url=(p.parent/'audio_url.txt').read_text().strip()
   it['audio']['he']={'url':url,'start':float(w1.get('start',w1.get('s'))),'end':float(w2.get('end',w2.get('e')))}
 except (OSError,ValueError,KeyError,TypeError):pass
 it['review']={'structural':'passed','editorial':'initial review; independent scholarly review pending','image':'artistic chapter illustration, explicitly labelled'}
 items.append(it)
items.sort(key=lambda it:(list(BOOKS).index(it['book']),it['chapter'],it['verse']))
# All chapters are indexed; only Genesis has undergone a first geography pass.
ledger=[]
for book,en in BOOKS.items():
 entries=[]
 for p in sorted((ROOT/book).glob('chapter_*/chapter.json')):
  c=json.loads(p.read_text());n=int(p.parent.name[8:]);v=c.get('verses',[])
  entries.append({'chapter':n,'verses':len(v),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'scan':'initial geographical pass' if book=='בראשית' else 'not reviewed','events':sum(it['book']==book and it['chapter']==n for it in items)})
 ledger.append({'book':book,'nameEn':en,'chapters':entries,'events':sum(it['book']==book for it in items),'completed':False})
coverage={'updated':'2026-10-28','status':'in progress — not a completed atlas','books':ledger,'pending':pending,'scope_note':'Genesis first pass only. Remaining books have been indexed, not geographically reviewed. A chapter with zero selected events is not certified free of relevant places. No book is marked complete.'}
(HERE/'events.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')
(HERE/'coverage.json').write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+'\n')
data=json.dumps({'books':BOOKS,'events':items,'coverage':coverage},ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
html=(HERE/'template.html').read_text().replace('/*ATLAS_DATA*/',data)
(ROOT/'geographical_bible.html').write_text(html)
print(f'Built {len(items)} events, {sum(len(i["facts"]) for i in items)} bilingual facts; {len(pending)} withdrawn; {sum(len(b["chapters"]) for b in ledger)} indexed chapters. No book complete.')
