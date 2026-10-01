#!/usr/bin/env node
// Deep Roots Kids — page generation.
// Usage: node scripts/kids/generate.mjs <book-slug> --page <n> [--attempts 3] [--dry-run]
//        node scripts/kids/generate.mjs <book-slug> --test <name> [--attempts 2] [--dry-run]
//   --test: a Stage 2 style-lock test from plan/style-tests.yaml (same prompt assembly, same
//   Gate 1 check, spend booked to THIS book's ledger), written to gen/test-<name>/.
import fs from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { checkGate1 } from './gate.mjs';
import * as ledger from './ledger.mjs';

const ROOT = '/Users/mananosm/Remotion';

function loadEnv(p = path.join(ROOT, '.env')) {
  const out = {};
  for (const line of fs.readFileSync(p, 'utf8').split('\n')) {
    const m = line.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)$/);
    if (m) out[m[1]] = m[2].trim().replace(/^["']|["']$/g, '');
  }
  return out;
}

// No node yaml dep in this workspace; python3+pyyaml is present and exact.
const readYaml = (p) =>
  JSON.parse(execFileSync('python3', ['-c',
    'import sys,yaml,json; json.dump(yaml.safe_load(open(sys.argv[1])), sys.stdout)', p],
    { encoding: 'utf8' }));

const args = process.argv.slice(2);
const slug = args[0];
const testName = args.includes('--test') ? args[args.indexOf('--test') + 1] : null;
const pageNo = testName ? null : Number(args[args.indexOf('--page') + 1]);
const attempts = args.includes('--attempts') ? Number(args[args.indexOf('--attempts') + 1]) : 1;
const dryRun = args.includes('--dry-run');
if (!slug || (!pageNo && !testName)) {
  console.error('usage: generate.mjs <slug> --page <n> | --test <name> [--attempts n] [--dry-run]');
  process.exit(2);
}

const bookDir = path.join(ROOT, 'kids', slug);

// ── GATE 1 ── nothing below this runs unless the review is signed.
const gate = checkGate1(bookDir);
if (!gate.ok) {
  console.error('\n  ⛔ GATE 1 BLOCKED — no generation, no spend.\n');
  console.error(`  ${gate.reason}\n`);
  process.exit(1);
}
console.log('  ✅ GATE 1 PASSED');
console.log(`     signed by : ${gate.signedBy}`);
console.log(`     dated     : ${gate.date}`);
console.log(`     signature : ${gate.reviewMtime}`);
console.log(`     gen/ files predating signature: none\n`);

const book = readYaml(path.join(bookDir, 'book.yaml'));
const plan = readYaml(path.join(bookDir, 'plan', 'pages.yaml'));
let planPage;
if (testName) {
  const tf = path.join(bookDir, 'plan', 'style-tests.yaml');
  if (!fs.existsSync(tf)) { console.error(`no ${tf}`); process.exit(2); }
  planPage = (readYaml(tf).tests ?? []).find(t => t.name === testName);
  if (!planPage) { console.error(`test ${testName} not in plan/style-tests.yaml`); process.exit(2); }
} else {
  planPage = plan.pages.find(p => p.page === pageNo);
}
if (!planPage) { console.error(`page ${pageNo} not in plan`); process.exit(2); }
const tag = testName ? `test-${testName}` : `p${pageNo}`;   // gen/ dir, prompt file, ledger label
// --edit-chosen "<change>": correct the CHOSEN image in place of re-rolling the scene. The
// chosen image is sent as the composition base; SCENE becomes the one change plus a lock on
// everything else. The plan itself is not modified.
const editChosen = args.includes('--edit-chosen') ? args[args.indexOf('--edit-chosen') + 1] : null;
let page = planPage;
if (editChosen) {
  const chosen = path.join(bookDir, 'gen', tag, 'CHOSEN');
  if (!fs.existsSync(chosen)) { console.error(`  --edit-chosen: p${pageNo} has no CHOSEN`); process.exit(2); }
  page = { ...planPage,
    base_ref: path.relative(ROOT, fs.realpathSync(chosen)),
    scene: `THE ONE CHANGE: ${editChosen} Keep everything else exactly as it is in reference C — ` +
           `every person, pose, face, hair, glasses, beads, head wrap, clothing, object, animal, ` +
           `background and the whole composition. Scene for context: ${planPage.scene}` };
}
if (page.placeholder || page.generate === false) {
  console.error(`\n  ⛔ page ${pageNo} is a HELD placeholder — no content may be generated for it.`);
  console.error(`     ${(page.note || '').split('\n')[0].trim()}\n`);
  process.exit(1);
}

// Style contract → prompt. Sections are lifted verbatim so the prompt can never
// drift from the reviewed document.
const style = fs.readFileSync(path.join(bookDir, 'prompts', 'style.md'), 'utf8');
// Keep only directive lines (bullets and sub-labels). Explanatory prose in
// style.md is for the human reader and only adds noise to the prompt.
const section = (h) => (style.split(/^## /m).find(s => s.startsWith(h)) ?? '')
  .replace(/^.*\n/, '')
  .split('\n')
  .filter(l => /^\s*-\s/.test(l) || /^\S.*:$/.test(l.trim()) || /^\s{2,}\S/.test(l))
  .join('\n')
  .replace(/\*\*/g, '')
  .trim();

const prompt = [
  `Black and white line art for a children's coloring book page, ages ${book.age_band}.`,
  ``,
  `SCENE: ${page.scene.replace(/\s+/g, ' ')}`,
  ``,
  `STYLE — follow exactly:`,
  section('Positive'),
  ``,
  `DO NOT INCLUDE:`,
  section('Negative'),
  ``,
  // A page names its figure treatment(s) in pages.yaml `figures:` — each value is the
  // suffix of a "## Human figures — <value>" heading in style.md. No page, no figures.
  ...[page.figures ?? []].flat().flatMap(f => {
    const body = section(`Human figures — ${f}`);
    if (!body) { console.error(`  style.md has no "## Human figures — ${f}" section`); process.exit(2); }
    return [`HUMAN FIGURES — follow exactly:`, body, ``];
  }),
  // Character-bible v2.0: per-page outfits, one fixed outfit per person for the whole page.
  ...(page.outfits ? [`OUTFITS — each person wears exactly this, and nothing else:`,
    ...Object.entries(page.outfits).map(([who, what]) =>
      `- ${who.replace(/([a-z])([A-Z0-9])/g, '$1 $2')}: ${what}`), ``] : []),
  `FRAMING:`,
  section('Safe area'),
].join('\n');

fs.mkdirSync(path.join(bookDir, 'prompts', 'pages'), { recursive: true });
fs.writeFileSync(path.join(bookDir, 'prompts', 'pages', `${tag}.txt`), prompt);

console.log(`  ${testName ? 'style test ' + testName : 'page ' + pageNo} — ${page.title}  (${page.ref})`);
console.log(`  prompt: ${prompt.length} chars -> prompts/pages/${tag}.txt`);
if (page.ruling) console.log(`  ruling: ${page.ruling.split('\n')[0].trim()}`);

if (dryRun) { console.log('\n  --dry-run: no API call made.\n'); process.exit(0); }

const env = loadEnv();
const model = env.KIDS_IMAGE_MODEL;
const outDir = path.join(bookDir, 'gen', tag);
fs.mkdirSync(outDir, { recursive: true });

// Style conditioning. A reference locked in a document does nothing if it never
// reaches the model — every call is otherwise independent text-to-image.
const refParts = [];
const lockRel = book.generation?.style_lock;
if (lockRel) {
  const lockPath = path.join(bookDir, lockRel);
  if (fs.existsSync(lockPath) && !lockRel.includes(`p${pageNo}.`)) {
    refParts.push({ inlineData: { mimeType: 'image/png', data: fs.readFileSync(lockPath).toString('base64') } });
    refParts.push({ text: 'REFERENCE A (LINE STYLE ONLY): copy only the line weight, level of ' +
      'detail and sparse ink density of this image. It is a style swatch, NOT content. Do NOT ' +
      'reproduce any animal, plant, object or composition that appears in it. The scene you draw ' +
      'is described in the SCENE section below and nowhere else.' });
    console.log(`  style lock: ${lockRel} sent as reference A`);
  }
}

// Optional composition base: preserve a solved layout and change only what SCENE says.
const baseRel = page.base_ref;
if (baseRel) {
  const basePath = path.join(ROOT, baseRel);
  if (!fs.existsSync(basePath)) { console.error(`  base_ref not found: ${baseRel}`); process.exit(2); }
  refParts.push({ inlineData: { mimeType: 'image/jpeg', data: fs.readFileSync(basePath).toString('base64') } });
  refParts.push({ text: 'REFERENCE C (COMPOSITION BASE — the starting point): reproduce this image ' +
    'closely. Keep its composition, its layout, its scenery, its line style, its figure ' +
    'construction and its ink density. Change ONLY the one thing the SCENE section below asks ' +
    'you to change. Everything else stays as it is in this image.' });
  console.log(`  base ref: ${baseRel} sent as reference C`);
}

// Optional second conditioning image: character construction, per page.
const charRel = page.character_ref;
if (charRel) {
  const charPath = path.join(ROOT, charRel);
  if (!fs.existsSync(charPath)) {
    console.error(`  character_ref not found: ${charRel}`); process.exit(2);
  }
  refParts.push({ inlineData: { mimeType: 'image/jpeg', data: fs.readFileSync(charPath).toString('base64') } });
  refParts.push({ text: 'REFERENCE B (human figure construction): draw ONLY the human figures ' +
    'using this exact construction — circle head, one simple rounded tunic, every arm and leg a ' +
    'SINGLE THIN LINE with no sleeve/tube/outline around it, hands and feet as plain ovals with ' +
    'no fingers and no shoes. Each head must have a simple outlined HAIR SHAPE drawn on it — a ' +
    'bare empty circle with nothing on it is a defect. Heads are small relative to the body, not ' +
    'oversized. Copy this figure method exactly. ' +
    (book.generation?.style_mode === 'flat-vector'
      // Flat-vector books: the whole page is one style, and the sheet also carries the cast's
      // fixed identity markers, which must be copied exactly where the SCENE names a cast member.
      ? 'Where the SCENE names a family member (Father, Mother, Daughter 1/2/3, Son, the dog, the ' +
        'cat), copy that character\'s fixed markers from this sheet exactly — hair, glasses, beads, ' +
        'head wrap, garment shape. Figures the SCENE does not name as family carry NONE of these ' +
        'markers. Do NOT copy the sheet\'s line-up pose or blank background — draw the SCENE. ' +
        'Scenery, animals and objects use this same simple flat-vector detail level.'
      : 'Do NOT copy its blank background or apply this flat style to the scenery — the scenery ' +
        'follows REFERENCE A.') });
  console.log(`  character ref: ${charRel} sent as reference B`);
}

// Continue numbering past existing attempts — never overwrite prior work.
const existing = fs.existsSync(outDir)
  ? fs.readdirSync(outDir).map(f => Number(f.match(/^attempt-(\d+)\./)?.[1] ?? 0))
  : [];
const startAt = (existing.length ? Math.max(...existing) : 0) + 1;

let spend = 0;
console.log(`  ${ledger.report(slug, env)}\n`);
for (let i = startAt; i < startAt + attempts; i++) {
  ledger.assertHeadroom(slug, 0.10, env);   // refuse before the call, not after
  const t0 = Date.now();
  const r = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`, {
    method: 'POST',
    headers: { 'x-goog-api-key': env.GEMINI_API_KEY, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      contents: [{ parts: refParts.concat([{ text: prompt }]) }],
      generationConfig: { responseModalities: ['IMAGE'], imageConfig: { aspectRatio: book.generation.aspect_ratio } },
    }),
  });
  const secs = ((Date.now() - t0) / 1000).toFixed(1);
  const j = await r.json();
  if (!r.ok) { console.error(`  attempt ${i}: ${r.status} — ${JSON.stringify(j).slice(0, 300)}`); continue; }

  const part = (j.candidates?.[0]?.content?.parts ?? []).find(p => p.inlineData);
  if (!part) { console.error(`  attempt ${i}: no image returned`); continue; }

  const ext = part.inlineData.mimeType.includes('png') ? 'png' : 'jpg';
  const file = path.join(outDir, `attempt-${String(i).padStart(2, '0')}.${ext}`);
  fs.writeFileSync(file, Buffer.from(part.inlineData.data, 'base64'));

  const u = j.usageMetadata ?? {};
  const outTok = u.candidatesTokenCount ?? (u.totalTokenCount - (u.promptTokenCount ?? 0));
  const cost = (outTok / 1e6) * 60;
  spend += cost;
  const run = ledger.record(`${tag} attempt-${i}`, cost, testName ? { book: slug, test: testName } : { book: slug, page: pageNo });
  console.log(`  attempt ${i}: ${path.basename(file)}  ${secs}s  $${cost.toFixed(4)}   ${slug} $${run.toFixed(4)}`);
}
console.log(`\n  this run $${spend.toFixed(4)} — ${ledger.report(slug, env)}\n`);
