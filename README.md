# Deep Roots Kids — Creation to Glorification

Coloring-book series, one book per album track. Nested repo inside `~/Remotion`
(ignored by the outer repo, like `dr-os/` and `deep-roots/`).

| Path | What |
|---|---|
| `_brand/` | Series governance: character-bible, brand-spec, theology-guardrails, about-the-author, album sources, reference art, spend ledger |
| `scripts/` | Pipeline (`~/Remotion/scripts/kids` is a symlink here). Every stage takes the book slug first. |
| `<slug>/` | One book: `book.yaml`, `plan/` (pages + Gate 1 review), `prompts/`, `art/`, `qa/`, `provenance.yaml`, `publishing/` |

Run from `~/Remotion`; Python stages use `.venv-kids/bin/python`, e.g.
`node scripts/kids/generate.mjs made-like-him --page 3 --attempts 2`.

## Not in git

- **`<slug>/gen/`** — every raw generation attempt (the audit trail behind each CHOSEN page).
- **`<slug>/out/`** — interior/cover PDFs; rebuild with `layout.py` / `cover.py`.
- **Unchosen cover candidates** and `REJECTED-*` files.
- **`.env`** — API keys. Never commit it.

## Backups

`gen/` is the only thing here that cannot be regenerated identically (the model is not
deterministic). Back it up next to the album sources in iCloud Drive:

    rsync -a --exclude .DS_Store ~/Remotion/kids/*/gen \
      --relative ~/Remotion/kids/./ \
      "$HOME/Library/Mobile Documents/com~apple~CloudDocs/DEEP ROOTS/MEDIA/DEEP ROOTS KIDS/gen-archive/"

Run it after every generation batch and before any gate sign-off.
