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

/** Cap and checkpoint for one book, from .env (defaults: $10 cap, $6 checkpoint). */
export function limits(env = {}) {
  return { cap: Number(env.KIDS_SPEND_CAP_USD ?? 10), checkpoint: Number(env.KIDS_SPEND_CHECKPOINT_USD ?? 6) };
}

export function report(book, env = {}) {
  const { cap, checkpoint } = limits(env);
  return `ledger: ${book} $${total(book).toFixed(4)} of $${cap.toFixed(2)} cap ` +
         `(checkpoint $${checkpoint.toFixed(2)}) — series $${total().toFixed(4)}`;
}

/**
 * Exits before any billable call that would take `book` past its checkpoint or cap.
 * Passing the checkpoint needs the editor's explicit go-ahead for THAT book:
 *   KIDS_PAST_CHECKPOINT=<book-slug> node scripts/kids/generate.mjs ...
 */
export function assertHeadroom(book, aboutToSpend = 0, env = {}) {
  const { cap, checkpoint } = limits(env);
  const t = total(book);
  if (t + aboutToSpend > cap) {
    console.error(`\n  ⛔ PER-BOOK SPEND CAP — ${book}: $${t.toFixed(2)} spent of $${cap.toFixed(2)}.`);
    console.error(`     This call would pass the cap. Stop, or the editor raises KIDS_SPEND_CAP_USD.\n`);
    process.exit(1);
  }
  if (t + aboutToSpend > checkpoint && process.env.KIDS_PAST_CHECKPOINT !== book) {
    console.error(`\n  ⏸  SPEND CHECKPOINT — ${book}: $${t.toFixed(2)} spent; checkpoint is $${checkpoint.toFixed(2)}.`);
    console.error(`     Stop and report. Continue only on the editor's go-ahead:`);
    console.error(`     KIDS_PAST_CHECKPOINT=${book} <same command>\n`);
    process.exit(1);
  }
  return t;
}
