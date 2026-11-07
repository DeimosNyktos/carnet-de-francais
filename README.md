# Carnet de Français

A free, offline-friendly web app to learn French with **spaced repetition**, **CEFR levels (A1–C2)** and a **choice of learning language: Catalan, Spanish or English**. One HTML file, no frameworks, no build step, no tracking.

<!-- TODO: add 2–3 screenshots in docs/ and link them here, e.g.
![Study screen](docs/study.png) -->

**Live demo:** https://deimosnyktos.github.io/carnet-de-francais/

## Features

- **CEFR levels A1 → C2.** Pick your level or take a short placement test (~2 min). You level up when you master 80% of the cards of your level.
- **Spaced repetition.** Each card moves through boxes with growing intervals (5 min, 1, 3, 7, 14 days). Mistakes come back sooner.
- **Active recall, not just recognition.** Flip cards, multiple choice (both directions), typing the answer (accent-tolerant, typo hints) and fill-in-the-blank sentences. The harder a card is for you, the more demanding the exercise.
- **Three interface/translation languages:** Catalan, Spanish and English.
- **Pronunciation** with the browser's speech synthesis (`fr-FR`), optional autoplay.
- **Verb conjugation tables** (présent, passé composé, imparfait, futur, conditionnel) for the main verbs in the deck.
- **Progress tracking:** daily goal, day streak, accuracy, per-level progress and a "difficult words" review.
- **Your own cards:** add them in the app or import/export them as CSV.
- **Light / dark / auto theme**, keyboard shortcuts (`Space` to flip, `1–4` to answer, `Esc` to close dialogs) and screen-reader announcements.
- **Installable (PWA)** when served over HTTPS, with an offline cache.
- **Private by design:** everything is stored in your browser (`localStorage`). Nothing is sent anywhere.

## Run it

Just open `index.html` in a browser.

To try the installable/offline version, serve the folder over HTTP(S):

```bash
python -m http.server 8000
```

Then open `http://localhost:8000/`.

## Add your own cards

In the app: **⚙ Options → My cards**. Or import a CSV with these columns:

```csv
lang,level,category,french,translation,note,sentence,sentence_translation
es,A2,vocab,la pomme,la manzana,,Je mange une [pomme].,Como una manzana.
```

- `lang`: `ca`, `es` or `en` (the language of the translation)
- `level`: `A1` … `C2`
- `category`: `vocab`, `verb` or `phrase`
- Put the target word in `[brackets]` in the sentence to enable fill-in-the-blank exercises.

## How it works

| Piece | Where |
|---|---|
| Deck (89 cards, 3 languages) | `BASE` array in the `<script>` of `index.html` |
| Spaced repetition | `grade()`, `pickNext()` and `INTERVALS` |
| Answer checking | `clean()`, `checkAnswer()` (normalises accents, apostrophes, `œ`, articles, pronouns) |
| Conjugation tables | `CONJ` + `conjTable()` (generated from a few stems per verb) |
| PWA | `manifest.webmanifest`, `sw.js`, `icon-*.png` |

Stack: vanilla HTML, CSS and JavaScript.

## Known limitations

- Small deck (89 cards): good for trying the method, not a complete course.
- Voices depend on the French voices installed on your device.
- Progress lives in one browser; it is not synced between devices.
- Reflexive and impersonal verbs have no conjugation table yet.

## Ideas / roadmap

- Larger decks by topic.
- Export/import of progress.
- More tenses (subjunctive) in the conjugation tables.

## License

<!-- TODO: choose a license (MIT is a common choice for small projects) and add a LICENSE file. -->
