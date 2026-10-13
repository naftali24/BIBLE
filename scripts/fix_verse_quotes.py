#!/usr/bin/env python3
"""Fix Hebrew verse-final punctuation only; leave audio, offsets and translations untouched."""
import argparse
import json
import re
from pathlib import Path

HEBREW_KEYS = ("verses", "hebrew", "verses_he", "hebrew_verses", "text_he", "he")
OBJECT_KEYS = ("text", "hebrew", "he", "text_he")

def fix_string(s):
    if not isinstance(s, str):
        return s, 0
    n = 0
    def end_quote(m):
        nonlocal n
        n += 1
        return "." + m.group(1) + m.group(2)
    s = re.sub(r'([״"])[\s\u00a0]*\.([\s\u00a0]*)$', end_quote, s)
    def space_before_quote(m):
        nonlocal n
        n += 1
        return "."
    s = re.sub(r'\.[\s\u00a0]+(?=[״"])', space_before_quote, s)
    return s, n

def fix_chapter(obj):
    count = 0
    for key in HEBREW_KEYS:
        values = obj.get(key)
        if not isinstance(values, list):
            continue
        for i, item in enumerate(values):
            if isinstance(item, str):
                values[i], n = fix_string(item)
                count += n
            elif isinstance(item, dict):
                for field in OBJECT_KEYS:
                    if isinstance(item.get(field), str):
                        item[field], n = fix_string(item[field])
                        count += n
    return count

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--book", default="*", help="Repository top-level book folder or *")
    parser.add_argument("--from-chapter", type=int, default=1)
    parser.add_argument("--to-chapter", type=int, default=150)
    parser.add_argument("--apply", action="store_true", help="Write changed files")
    args = parser.parse_args()
    if args.from_chapter < 1 or args.to_chapter < args.from_chapter:
        parser.error("Invalid chapter range")
    changed = fixes = errors = 0
    for path in sorted(Path(".").glob("*/chapter_*/chapter.json")):
        if args.book != "*" and path.parts[0] != args.book:
            continue
        try:
            chapter = int(path.parent.name.split("_")[-1])
            if not args.from_chapter <= chapter <= args.to_chapter:
                continue
            original = path.read_text(encoding="utf-8")
            obj = json.loads(original)
            n = fix_chapter(obj)
            if n:
                changed += 1
                fixes += n
                print(f"{path}: {n} fixes")
                if args.apply:
                    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        except Exception as exc:
            errors += 1
            print(f"ERROR {path}: {exc}")
    print(f"Files: {changed}; fixes: {fixes}; errors: {errors}; mode: {'APPLY' if args.apply else 'PREVIEW'}")
    if errors:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
