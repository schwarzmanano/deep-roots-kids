// Spend ledger, keyed by book slug (per-book cap ruled 2026-09-28, made-like-him Gate 2).
// Every entry carries `book`: a book slug, or "_brand" for series-level reference art.
// Cap and checkpoint apply PER BOOK; the series total is reported alongside, never capped.
import fs from 'node:fs';
import path from 'node:path';
const ROOT = '/Users/mananosm/Remotion';
export const LEDGER = path.join(ROOT, 'kids/_brand/spend-ledger.json');

export function read() {
  if (!fs.existsSync(LEDGER)) return { total_usd: 0, by_book: {}, entries: [] };
  return JSON.parse(fs.readFileSync(LEDGER, 'utf8'));
}
const sum = (es) => Number(es.reduce((s, e) => s + e.usd, 0).toFixed(4));

/** Series total, or one book's total when `book` is given. */
export function total(book) {
  const es = read().entries;
  return sum(book ? es.filter(e => e.book === book) : es);
}

export function record(label, usd, meta = {}) {
  if (!meta.book) throw new Error(`ledger.record("${label}"): meta.book is required`);
  const l = read();
  l.entries.push({ ts: new Date().toISOString(), label, usd: Number(usd.toFixed(4)), ...meta });
  l.total_usd = sum(l.entries);
  l.by_book = {};
  for (const e of l.entries) l.by_book[e.book] = Number(((l.by_book[e.book] ?? 0) + e.usd).toFixed(4));
  fs.writeFileSync(LEDGER, JSON.stringify(l, null, 2));
  return total(meta.book);
}

/**
 * Cap and checkpoints for one book. Defaults from .env ($10 cap, one $6 checkpoint).
 * Per-book overrides in book.yaml (editor rulings):
 *   spend_cap_usd: 14
 *   spend_checkpoints_pct: [50, 80]   -> stop-and-report at 50% and 80% of the cap
 */
export function limits(env = {}, book) {
  let cap = Number(env.KIDS_SPEND_CAP_USD ?? 10);
  let checkpoints = [Number(env.KIDS_SPEND_CHECKPOINT_USD ?? 6)];
  let pct = null;
  const by = book && path.join(ROOT, 'kids', book, 'book.yaml');
  if (by && fs.existsSync(by)) {
    const y = fs.readFileSync(by, 'utf8');
    const m = y.match(/^spend_cap_usd:\s*([\d.]+)/m);
    if (m) cap = Number(m[1]);
    const p = y.match(/^spend_checkpoints_pct:\s*\[([\d.,\s]+)\]/m);
    if (p) {
      pct = p[1].split(',').map(Number).sort((a, b) => a - b);
      checkpoints = pct.map(x => Number((cap * x / 100).toFixed(2)));
    }
  }
  return { cap, checkpoint: checkpoints[0], checkpoints, pct };
}

export function report(book, env = {}) {
  const { cap, checkpoint } = limits(env, book);
  const { checkpoints, pct } = limits(env, book);
  const cps = checkpoints.map((c, i) => `$${c.toFixed(2)}${pct ? ` (${pct[i]}%)` : ''}`).join(', ');
  return `ledger: ${book} $${total(book).toFixed(4)} of $${cap.toFixed(2)} cap ` +
         `(checkpoint${checkpoints.length > 1 ? 's' : ''} ${cps}) — series $${total().toFixed(4)}`;
}

/**
 * Exits before any billable call that would take `book` past its checkpoint or cap.
 * Passing the checkpoint needs the editor's explicit go-ahead for THAT book:
 *   KIDS_PAST_CHECKPOINT=<book-slug> node scripts/kids/generate.mjs ...
 */
export function assertHeadroom(book, aboutToSpend = 0, env = {}) {
  // Passing a checkpoint needs the editor's explicit go-ahead for THAT book and THAT checkpoint:
  //   KIDS_PAST_CHECKPOINT=<book-slug>        single-checkpoint books (the .env default)
  //   KIDS_PAST_CHECKPOINT=<book-slug>@50     percentage books: passes the 50% stop only
  //   KIDS_PAST_CHECKPOINT=<book-slug>@80     ... passes the 50% and 80% stops
  const { cap, checkpoints, pct } = limits(env, book);
  const t = total(book);
  if (t + aboutToSpend > cap) {
    console.error(`\n  ⛔ PER-BOOK SPEND CAP — ${book}: $${t.toFixed(2)} spent of $${cap.toFixed(2)}.`);
    console.error(`     This call would pass the cap. Stop; only the editor raises spend_cap_usd.\n`);
    process.exit(1);
  }
  const go = process.env.KIDS_PAST_CHECKPOINT ?? '';
  const [goBook, goPct] = go.split('@');
  for (let i = 0; i < checkpoints.length; i++) {
    const cp = checkpoints[i];
    const cleared = goBook === book && (pct ? Number(goPct) >= pct[i] : true);
    if (t + aboutToSpend > cp && !cleared) {
      const label = pct ? `${pct[i]}% checkpoint` : 'checkpoint';
      console.error(`\n  ⏸  SPEND ${label.toUpperCase()} — ${book}: $${t.toFixed(2)} spent; ${label} is $${cp.toFixed(2)} of $${cap.toFixed(2)}.`);
      console.error(`     Stop and report. Continue only on the editor's go-ahead:`);
      console.error(`     KIDS_PAST_CHECKPOINT=${book}${pct ? '@' + pct[i] : ''} <same command>\n`);
      process.exit(1);
    }
  }
  return t;
}
