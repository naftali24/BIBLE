#!/usr/bin/env python3
"""Remove the upper underlined idea heading from tanakh.html, both languages.
Keep the lower inline heading. Preview by default; --apply to save.
"""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "tanakh.html"
OLD = "c.innerHTML=ideaHead+'<div class=\"num "
NEW = "c.innerHTML='<div class=\"num "

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    original = TARGET.read_text(encoding="utf-8-sig")
    count = original.count(OLD)
    if count == 0 and NEW in original:
        print("Already fixed: upper underlined idea title is not rendered.")
        return
    if count != 1:
        raise SystemExit(f"Expected exactly one upper title render, found {count}; no changes made")
    updated = original.replace(OLD, NEW, 1)
    if args.apply:
        TARGET.write_text(updated, encoding="utf-8")
    print(f'{"APPLIED" if args.apply else "PREVIEW"}: Removed upper underlined heading; lower idea heading preserved for Hebrew and English.')

if __name__ == "__main__":
    main()
