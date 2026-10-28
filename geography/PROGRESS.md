# Geographical Bible — work checkpoint, 2026-10-28

This is **not the completed atlas requested in the brief**. Do not describe the full Bible, or even Genesis, as completed.

## Current deliverable

- `../geographical_bible.html`: self-contained bilingual event viewer, using the historical application's brown/gold visual language. Only new atlas files have been added.
- 45 drafted Genesis events, each with six paired Hebrew/English statements (270 per language), source links and evidence categories.
- Canonical verse strings copied exactly from the repository's `chapter.json` files. Existing verses, images, recordings and applications have not been edited.
- All 39 individual books appear in the owl menu. The other 38 have an explicit incomplete state, not fabricated content.
- Genesis chapters 1–50 received an initial geographical candidate pass. This is not an exhaustive scholarly survey. The 929 chapter records for the whole Tanakh were technically indexed; indexing is **not** a geographical review.
- All 45 selected illustrations were visually inspected in a contact sheet. One generated map with unverified place labels was rejected and replaced. Illustrations are labelled as artistic chapter scenes, not photographs or verified reconstructions of the featured sites.
- Gor(en) Atad was withdrawn: it lacked six independent geographical facts. Its draft remains in the authoring source and its status in `coverage.json`.

## Honest quality status

| Book | Chapters in initial pass | Draft events | Structural checks passed | Final ten-check scholarly approval | Withdrawn |
|---|---:|---:|---:|---:|---:|
| Genesis | 50 | 45 | 45 | 0 | 1 |
| Every other book | 0 | 0 | 0 | 0 | 0 |

All source links provide research context, but the existence of a URL is not a claim that every assertion has passed independent source verification. Some linked reference entries require further verification, and some facts are interpretive explanations of the text. An independent scholarly review remains outstanding. No book has `completed: true`.

## Explicit remaining scope

1. Continue Genesis review and investigate omitted candidates: Akkad and Calneh (10:10); Gaza (10:19); Elam (14:1); Ashteroth-karnaim, Ham, Shaveh-kiriathaim (14:5); Kadesh and Hazazon-tamar (14:7); Beer-lahai-roi (16:14); Zoar (19:23); Aram-naharaim and the city of Nahor (24:10); Dedan and Sheba (25:3); Mahanaim (32:3); Migdal-eder (35:21); Edomite royal centres (36:31–39); Chezib and Timnah (38:5,12); Atad (50:10). Listing these is not a claim of researched event content. Some identifications may remain unresolved.
2. Start Exodus at chapters 1–20, then continue automatically in 10–20 chapter sections through the remaining books. Hundreds of researched events remain to be written; this checkpoint does not meet the requested final quantity.
3. Replace artistic illustrations with correctly licensed and attributed site photographs wherever available; do not add AI maps with unverified labels.
4. Expand source support and independently review facts, archaeological attribution, direct verse relation, uncertainty wording, translation equivalence and meaningful differences between repeated sites.
5. Review all chapters again before marking a book complete. Zero events in a chapter does not certify absence of geographic material.

## Verification performed

- `python geography/build.py`: repeatable generation from authoring records and unchanged chapter assets.
- `python geography/validate.py`: 45 events; six facts in both languages; unique IDs; no repeated full fact strings; exact verse equality; local image existence; valid recording segment shapes; 39 book entries and 929 chapter entries. **No factual truth certification is implied.**
- DOM integration: 90 event/language renders; event navigation; all book choices and incomplete states; complete GPT context and correct `https://chatgpt.com/?q=` URLs; progress report; local saved position; mocked recording/speech handlers. Install jsdom outside the repo and set `NODE_PATH` to that installation to run `node geography/test_dom.cjs`.
- Actual browser visual/mobile tests were blocked because this environment had no Chromium binary and the browser download returned invalid ZIP files. DOM tests do not establish visual fit, real touch behaviour or media playback.
- Actual Hebrew/English audio delivery, device speech voices, Android screen layout, installed-PWA navigation and fullscreen behaviour still require device testing. The existing shared `manifest.json` is referenced; `index.html` and PWA files are unchanged.

## Design and behaviour

The viewer displays one event at a time. Long cards scroll naturally; vertical swipes or mouse-wheel movements at the appropriate scroll boundary advance events. Footer arrows always work. The title's audio button uses existing verse recordings with exact Hebrew string-aligned timing where possible; absent timing falls back to device speech. It does not invent recording timestamps.

GPT opens in a new tab with the same query-string method as the historical app, preceded by a reviewable context dialog. The user must click Open GPT; blocked popups leave the prompt available for copying. No external messages are sent.

## Files

`events.txt` and `sources.json` are the authoring inputs. `events.json`, `coverage.json`, `validation.json` and the root HTML are generated outputs. `coverage.json` contains chapter hashes and incomplete status. Never edit the historical application or index as part of this stage.
