#!/usr/bin/env python3
"""Safely fix Hebrew verse closing punctuation in */chapter_NNN/chapter.json only.

Example: לְמִינָהּ. ״ וַיְהִי כֵן. -> לְמִינָהּ". וַיְהִי כֵן.
No other JSON fields or files are modified. Dry run by default.
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Dot + optional whitespace + closing quote + whitespace, with Hebrew text before.
PATTERN = re.compile(r'(?<=[\u0590-\u05FF])\.[ \t\u00a0]*[״”"](?=[ \t\u00a0]+)')
# Do not match end-of-verse punctuation or JSON delimiters.
OPENING = re.compile(r'(?<=[ :;,])״(?=[\u0590-\u05FF])')

def fix_verse(verse):
    def replace(m):
        return '".'
    # Leave following whitespace exactly as it was.
    verse = PATTERN.sub(replace, verse)
    return OPENING.sub('"', verse)

def chapter_files():
    for p in sorted(ROOT.rglob('chapter.json')):
        if re.fullmatch(r'chapter_\d+', p.parent.name, re.I):
            yield p

def run(apply):
    files=changes=0
    for path in chapter_files():
        files+=1
        original=path.read_text(encoding='utf-8-sig')
        try:
            data=json.loads(original)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f'Invalid JSON before changes: {path}: {exc}') from exc
        verses=data.get('verses') if isinstance(data,dict) else None
        if not isinstance(verses,list) or not all(isinstance(v,str) for v in verses):
            continue
        revised=[fix_verse(v) for v in verses]
        count=sum(len(PATTERN.findall(v)) + len(OPENING.findall(PATTERN.sub('".',v))) for v in verses)
        if not count:
            continue
        # Replace only the exact serialized verse strings within the verses array.
        # We verify the full parsed JSON remains identical except for verses.
        # Preserve all other fields via line-level replacement, avoiding reformatting.
        lines=original.splitlines(keepends=True)
        cursor=0
        for old,new in zip(verses,revised):
            if old==new: continue
            old_json=json.dumps(old,ensure_ascii=False)
            new_json=json.dumps(new,ensure_ascii=False)
            found=False
            for idx in range(cursor,len(lines)):
                if old_json in lines[idx]:
                    lines[idx]=lines[idx].replace(old_json,new_json,1)
                    cursor=idx+1
                    found=True
                    break
            if not found:
                raise RuntimeError(f'Could not locate original verse in {path}; no changes written')
        updated=''.join(lines)
        check=json.loads(updated)
        expected=dict(data)
        expected['verses']=revised
        if check!=expected:
            raise RuntimeError(f'Unexpected JSON changes in {path}; no changes written')
        if apply:
            path.write_text(updated,encoding='utf-8')
        changes+=count
        print(f'{path.relative_to(ROOT)}: {count} changes')
    print(f'CHAPTER files scanned: {files}')
    print(f'{"APPLIED" if apply else "PREVIEW"}: {changes} replacements')
    if not files:
        raise SystemExit('ERROR: No chapter.json files found')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--apply',action='store_true')
    args=parser.parse_args()
    run(args.apply)
