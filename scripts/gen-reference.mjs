#!/usr/bin/env node
// Standalone reference-art generator (character sheets, wardrobe tests, style probes).
// Not page generation — no Gate 1 dependency, writes to kids/_brand/, spend booked to
// the "_brand" ledger key (series-level reference art).
//
// Usage: node scripts/kids/gen-reference.mjs <outName> <promptFile> [attempts] [--ref <img>]...
//   --ref may repeat; each image is sent ahead of the prompt as conditioning.
import fs from 'node:fs';
import path from 'node:path';
import * as ledger from './ledger.mjs';
const ROOT = '/Users/mananosm/Remotion';
const env = Object.fromEntries(fs.readFileSync(path.join(ROOT,'.env'),'utf8').split('\n')
  .map(l => l.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)$/)).filter(Boolean)
  .map(m => [m[1], m[2].trim().replace(/^["']|["']$/g,'')]));

const argv = process.argv.slice(2);
const refs = [];
for (let i = argv.indexOf('--ref'); i !== -1; i = argv.indexOf('--ref')) refs.push(...argv.splice(i, 2).slice(1));
const [outName, promptFile, attemptsArg] = argv;
if (!outName || !promptFile) {
  console.error('usage: gen-reference.mjs <outName> <promptFile> [attempts] [--ref <img>]...'); process.exit(1);
}
const attempts = Number(attemptsArg ?? 1);
const prompt = fs.readFileSync(promptFile, 'utf8');
const outDir = path.join(ROOT, 'kids', '_brand');
fs.mkdirSync(outDir, { recursive: true });
const BOOK = '_brand';

const refParts = refs.map(r => {
  const p = path.isAbsolute(r) ? r : path.join(ROOT, r);
  const mime = /\.png$/i.test(p) ? 'image/png' : 'image/jpeg';
  return { inlineData: { mimeType: mime, data: fs.readFileSync(p).toString('base64') } };
});

console.log(`  ${ledger.report(BOOK, env)}${refs.length ? `\n  refs: ${refs.join(', ')}` : ''}`);
let spend = 0;
for (let i = 1; i <= attempts; i++) {
  ledger.assertHeadroom(BOOK, 0.10, env);
  const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${env.KIDS_IMAGE_MODEL}:generateContent`, {
    method: 'POST',
    headers: { 'x-goog-api-key': env.GEMINI_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({ contents: [{ parts: refParts.concat([{ text: prompt }]) }],
      generationConfig: { responseModalities: ['IMAGE'], imageConfig: { aspectRatio: '4:3' } } }),
  });
  const j = await r.json();
  if (!r.ok) { console.error(`  ${i}: ${r.status} ${JSON.stringify(j).slice(0,200)}`); continue; }
  const p = (j.candidates?.[0]?.content?.parts ?? []).find(x => x.inlineData);
  if (!p) { console.error(`  ${i}: no image`); continue; }
  const f = path.join(outDir, `${outName}-${String(i).padStart(2,'0')}.jpg`);
  fs.writeFileSync(f, Buffer.from(p.inlineData.data, 'base64'));
  const u = j.usageMetadata ?? {};
  const cost = ((u.candidatesTokenCount ?? u.totalTokenCount - (u.promptTokenCount ?? 0))/1e6)*60;
  spend += cost;
  ledger.record(`ref: ${outName}-${i}`, cost, { book: BOOK });
  console.log(`  ${path.basename(f)}  $${cost.toFixed(4)}`);
}
console.log(`  this run $${spend.toFixed(4)} — ${ledger.report(BOOK, env)}`);
