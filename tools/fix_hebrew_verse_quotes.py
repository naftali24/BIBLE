#!/usr/bin/env python3
"""Correct Hebrew closing-quote punctuation in CHAPTER source files.

Before: לְמִינָהּ. ״ וַיְהִי כֵן.
After:  לְמִינָהּ". וַיְהִי כֵן.

Preview is the default. --apply modifies files. Works with CHAPTER source
files regardless of extension (HTML, JS, TXT, JSON or extensionless).
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEBREW = r'\u0590-\u05FF'
# Require Hebrew just before the period to avoid touching English prose.
# Quote can be U+05F4 Hebrew gershayim, U+201C/U+201D curly quote,
# or a literal ASCII double quote.
PATTERN = re.compile(r'([' + HEBREW + r'])(\.)[ \t\u00a0]*[״“”"][ \t\u00a0]*')
SKIP_DIRS = {'.git', '.github', 'node_modules', 'image', 'images', 'audio', 'backup', 'backups'}
TEXT_SUFFIXES = {'.json', '.html', '.htm', '.txt', '.js', '.mjs', '.jsonl', '.xml', '.md', ''}

def chapter_file(path):
    rel = path.relative_to(ROOT)
    if any(part.lower() in SKIP_DIRS for part in rel.parts[:-1]):
        return False
    # Files may live inside CHAPTER/ or have CHAPTER in their names.
    return path.name.lower() == 'chapter.json' and any(part.lower().startsWith('chapter_') for part in rel.parts[:-1])

def correct(text):
    # JSON strings escape ASCII quotes, so never introduce a bare quote inside JSON.
    return PATTERN.sub(lambda m: m.group(1) + '". ', text)

def process(path, apply):
    try:
        original = path.read_text(encoding='utf-8-sig')
    except (UnicodeError, OSError):
        return 0
    if not re.search('[' + HEBREW + ']', original):
        return 0
    # For JSON files, ASCII quotes must be escaped to keep valid JSON.
    if path.suffix.lower() in {'.json', '.jsonl'}:
        # JSON can have escaped quoted values; replace with escaped quote.
        changed, count = PATTERN.subn(lambda m: m.group(1) + '\\". ', original)
    else:
        changed, count = PATTERN.subn(lambda m: m.group(1) + '". ', original)
    if apply and count:
        path.write_text(changed, encoding='utf-8')
    return count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    candidates = 0
    changed_files = 0
    total = 0
    for path in ROOT.rglob('*'):
        if not path.is_file() or not chapter_file(path):
            continue
        if path.stat().st_size > 12_000_000:
            continue
        candidates += 1
        count = process(path, args.apply)
        if count:
            changed_files += 1
            total += count
            print(f'{path.relative_to(ROOT)}: {count} replacements')
    print(f'CHAPTER candidate files scanned: {candidates}')
    print(f'{"APPLIED" if args.apply else "PREVIEW"}: {total} replacements in {changed_files} files')
    if not candidates:
        print('WARNING: No CHAPTER files found. Check source file paths in the repository.')

if __name__ == '__main__':
    main()
