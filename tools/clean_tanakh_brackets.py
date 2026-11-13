#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Remove bracketed content from Hebrew verse strings in every chapter.json.
Run without --apply to preview; with --apply to save.
"""
import argparse
import json
import re
from pathlib import Path

PAIRS = dict(zip(
    "([{<（［｛【〔〈《⟨⟦«‹",
    ")]}>）］｝】〕〉》⟩⟧»›"
))
DOT = re.compile(r"^[ \t\u00a0]*[.．。]")

def clean(s):
    stack, spans = [], []
    for i, char in enumerate(s):
        if char in PAIRS:
            stack.append((char, i))
        elif char in PAIRS.values() and stack and PAIRS[stack[-1][0]] == char:
            _, start = stack.pop()
            if not stack:
                end = i + 1
                match = DOT.match(s[end:])
                if match:
                    end += match.end()
                spans.append((start, end))
    if stack:
        # Malformed verse: leave it untouched for manual review.
        return s, 0
    for start, end in reversed(spans):
        s = s[:start] + s[end:]
    return re.sub(r" {2,}", " ", s).strip(), len(spans)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("repo", nargs="?", type=Path, default=Path("."))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    files = changed = verses = removed = 0
    for path in sorted(args.repo.rglob("chapter.json")):
        if ".git" in path.parts:
            continue
        files += 1
        try:
            original = path.read_text(encoding="utf-8-sig")
            data = json.loads(original)
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            print("ERROR", path, error)
            continue
        if not isinstance(data, dict) or not isinstance(data.get("verses"), list):
            continue
        affected = []
        for index, verse in enumerate(data["verses"]):
            if isinstance(verse, str):
                new, n = clean(verse)
                if n:
                    data["verses"][index] = new
                    affected.append(index + 1)
                    removed += n
            elif isinstance(verse, dict):
                for key in ("hebrew", "he", "text"):
                    if isinstance(verse.get(key), str):
                        new, n = clean(verse[key])
                        if n:
                            verse[key] = new
                            affected.append(index + 1)
                            removed += n
        if affected:
            changed += 1
            verses += len(set(affected))
            print(path, "verses:", ",".join(map(str, sorted(set(affected)))))
            if args.apply:
                indent = 2 if re.search(r'\n  "', original) else 4
                path.write_text(json.dumps(data, ensure_ascii=False, indent=indent) + "\n", encoding="utf-8")
    print(f"Scanned {files} chapters; changed {changed} files, {verses} verses; removed {removed} bracketed sections.")
    print("APPLIED" if args.apply else "PREVIEW ONLY")

if __name__ == "__main__":
    main()
