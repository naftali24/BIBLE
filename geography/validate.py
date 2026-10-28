"""Structural checks only; does not certify historical truth."""
import json,re
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parents[1]
events=json.loads((R/'geography/events.json').read_text());coverage=json.loads((R/'geography/coverage.json').read_text());errors=[];warnings=[]
ids=[]
for event in events:
 ids.append(event['id']);facts=event['facts']
 if len(facts)<6:errors.append(event['id']+': fewer than six facts')
 for lang in ['he','en']:
  text=[f[lang].strip() for f in facts]
  if not all(text) or len(set(text))!=len(text):errors.append(event['id']+': missing or duplicate '+lang)
  if not event['title'][lang] or not event['quote'][lang]:errors.append(event['id']+': missing text '+lang)
 if any(not f['source'].startswith('https://') for f in facts):errors.append(event['id']+': source missing')
 if any(f['type'] not in ['F','U','B'] for f in facts):errors.append(event['id']+': unclassified fact')
 if not (R/event['image']['src']).is_file():errors.append(event['id']+': missing image')
 c=json.loads((R/event['book']/f"chapter_{event['chapter']:03}"/'chapter.json').read_text())
 if event['quote']['he']!=c['verses'][event['verse']-1] or event['quote']['en']!=c['english'][event['verse']-1]:errors.append(event['id']+': changed source verse')
 for lang,clip in event['audio'].items():
  if 'start' in clip and (not isinstance(clip['start'],(int,float)) or clip['start']<0 or clip['end']<=clip['start']):errors.append(event['id']+': invalid audio '+lang)
 for f in facts:
  if re.search(r'ערים עתיקות היו חשובות|דרכים שימשו למסחר ולתנועה|הרים השפיעו על החיים|האזור היה בעל חשיבות גיאוגרפית',f['he']):errors.append(event['id']+': filler')
if len(ids)!=len(set(ids)):errors.append('duplicate ids')
for lang in ['he','en']:
 count=Counter(f[lang] for it in events for f in it['facts'])
 for text,n in count.items():
  if n>1:warnings.append({'type':'cross-event repeated fact','language':lang,'count':n,'text':text})
assert len(coverage['books'])==39
assert sum(len(b['chapters']) for b in coverage['books'])==929
assert not any(b['completed'] for b in coverage['books'])
report={'events':len(events),'facts_per_language':sum(len(e['facts']) for e in events),'errors':errors,'warnings':warnings,'scope':'Structure, source verse equality, local image existence and media timing shape only; truth, source support and site identification require editorial review.'}
(R/'geography/validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
