#!/usr/bin/env python3
"""Move period after closing quote in Hebrew verse text (both quote styles).
Preview by default; --apply writes changes. No JSON reserialization.
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERN = re.compile(r'\.\s*["״]\s*')
HEBREW = re.compile(r'[\u0590-\u05ff]')
VERSE_KEYS = {'he', 'hebrew', 'hebrewtext', 'hebrew_text', 'text_he',
              'versetext', 'verse_text', 'versehe', 'verse_he',
              'versehebrew', 'verse_hebrew', 'pasuk', 'verse'}
EXCLUDE = {'.git', '.github', 'node_modules', 'image', 'images', 'audio',
           'readalong', 'karaoke', 'backup', 'backups'}

def fix(value):
    return PATTERN.sub('". ', value)

def locate_strings(raw):
    """Return ranges of JSON string *values* (not keys), with parent keys."""
    decoder = json.JSONDecoder()
    # JSON parsed to validate, then locate lexical values using a small tokenizer.
    # Use regex tokenization to retain exact formatting/escapes.
    token = re.compile(r'"(?:\\.|[^"\\])*"|[{}\[\]:,]|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?|true|false|null', re.S)
    stack = []
    pending = None
    for m in token.finditer(raw):
        t = m.group()
        if t in ('{','['):
            stack.append({'type':t,'key':pending,'expect_key':t=='{'})
            pending = None
        elif t in ('}',']'):
            if stack: stack.pop()
            pending = None
        elif t == ':':
            pass
        elif t == ',':
            if stack and stack[-1]['type']=='{': stack[-1]['expect_key']=True
        elif t.startswith('"'):
            if stack and stack[-1]['type']=='{' and stack[-1]['expect_key']:
                pending=json.loads(t)
                stack[-1]['expect_key']=False
            else:
                keys=[x['key'] for x in stack if isinstance(x['key'],str)]
                if pending is not None: keys.append(pending)
                yield m.start(),m.end(),t,keys
                pending=None
        else:
            pending=None

def process(path, apply):
    raw=path.read_text(encoding='utf-8-sig')
    if path.suffix.lower() not in ('.json',):
        # CHAPTER source files may be HTML/text, not JSON.
        n=len(PATTERN.findall(raw))
        if apply and n:
            path.write_text(fix(raw),encoding='utf-8')
        return n
    try: json.loads(raw)
    except (ValueError, UnicodeError): return 0
    edits=[]
    for start,end,quoted,keys in locate_strings(raw):
        try: val=json.loads(quoted)
        except ValueError: continue
        if not HEBREW.search(val) or not PATTERN.search(val): continue
        # Explicit verse field, or Hebrew value inside a verse object.
        if not any(str(k).lower() in VERSE_KEYS for k in keys): continue
        new=fix(val)
        if new==val: continue
        # Preserve original JSON layout; JSON-escape replacement text.
        replacement=json.dumps(new,ensure_ascii=False)
        edits.append((start,end,replacement,len(PATTERN.findall(val))))
    if apply and edits:
        for start,end,replacement,_ in reversed(edits):
            raw=raw[:start]+replacement+raw[end:]
        path.write_text(raw,encoding='utf-8')
    return sum(e[3] for e in edits)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--apply',action='store_true')
    args=ap.parse_args()
    total=files=0
    for path in ROOT.rglob('*'):
        if not path.is_file() or path.suffix.lower() not in ('.json', '.html', '.htm', '.txt'): continue
        if 'chapter' not in str(path.relative_to(ROOT)).lower(): continue
        rel=path.relative_to(ROOT)
        if any(p.lower() in EXCLUDE for p in rel.parts[:-1]): continue
        if path.stat().st_size>10_000_000: continue
        n=process(path,args.apply)
        if n:
            print(f'{rel}: {n} replacements')
            total+=n;files+=1
    print(f'{"APPLIED" if args.apply else "PREVIEW"}: {total} replacements in {files} files')
if __name__=='__main__': main()
