// Gate 1 enforcement. Imported by generate.mjs; never bypassed.
import fs from 'node:fs';
import path from 'node:path';

export function checkGate1(bookDir) {
  const reviewPath = path.join(bookDir, 'plan', 'theology-review.md');
  const genDir = path.join(bookDir, 'gen');

  if (!fs.existsSync(reviewPath)) {
    return { ok: false, reason: `missing ${reviewPath}` };
  }

  const text = fs.readFileSync(reviewPath, 'utf8');
  const status = text.match(/^\*\*Status:\*\*\s*(.+)$/m)?.[1]?.trim() ?? '';
  const signed = /^SIGNED\b/.test(status);
  if (!signed) {
    return { ok: false, reason: `Gate 1 NOT signed — Status reads: "${status}"` };
  }

  const signedBlock = text.match(/Signed:\s*(.+)/)?.[1]?.trim() ?? '';
  const dateBlock = text.match(/Date:\s*(.+)/)?.[1]?.trim() ?? '';
  if (!signedBlock || !dateBlock) {
    return { ok: false, reason: 'Status says SIGNED but the sign-off block is incomplete' };
  }

  const reviewMtime = fs.statSync(reviewPath).mtimeMs;

  // Back-dating guard: nothing already generated may predate the signature.
  const stale = [];
  if (fs.existsSync(genDir)) {
    const walk = (d) => {
      for (const e of fs.readdirSync(d, { withFileTypes: true })) {
        const p = path.join(d, e.name);
        if (e.isDirectory()) walk(p);
        else if (fs.statSync(p).mtimeMs < reviewMtime) stale.push(p);
      }
    };
    walk(genDir);
  }
  if (stale.length) {
    return {
      ok: false,
      reason: `${stale.length} file(s) in gen/ predate the signature — generated before review:\n` +
              stale.slice(0, 10).map(s => `    ${s}`).join('\n'),
    };
  }

  return {
    ok: true,
    signedBy: signedBlock,
    date: dateBlock,
    reviewMtime: new Date(reviewMtime).toISOString(),
  };
}
