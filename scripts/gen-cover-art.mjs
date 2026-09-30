#!/usr/bin/env node
// Cover art generator. Full-colour, and unlike the interior this output stays
// RASTER in the PDF, so KDP's 300 DPI floor applies — hence imageSize.
import fs from 'node:fs';
import path from 'node:path';
import * as ledger from './ledger.mjs';
const ROOT='/Users/mananosm/Remotion';
const env=Object.fromEntries(fs.readFileSync(path.join(ROOT,'.env'),'utf8').split('\n')
  .map(l=>l.match(/^\s*([A-Z0-9_]+)\s*=\s*(.*)$/)).filter(Boolean)
  .map(m=>[m[1],m[2].trim().replace(/^["']|["']$/g,'')]));
const argv=process.argv.slice(2); const refs=[];
for(let i=argv.indexOf('--ref');i!==-1;i=argv.indexOf('--ref')) refs.push(...argv.splice(i,2).slice(1));
const [slug,outName,promptFile,aspect='3:4',size='4K',attemptsArg='1']=argv;
const refParts=refs.map(r=>({inlineData:{mimeType:/\.png$/i.test(r)?'image/png':'image/jpeg',data:fs.readFileSync(path.isAbsolute(r)?r:path.join(ROOT,r)).toString('base64')}}));
if(!slug||!fs.existsSync(path.join(ROOT,'kids',slug,'book.yaml'))){console.error('usage: gen-cover-art.mjs <book-slug> <outName> <promptFile> [aspect] [size] [attempts]');process.exit(1);}
const prompt=fs.readFileSync(promptFile,'utf8');
const outDir=path.join(ROOT,'kids',slug,'cover'); fs.mkdirSync(outDir,{recursive:true});
console.log(`  ${ledger.report(slug, env)}`);
let spend=0;
for(let i=1;i<=Number(attemptsArg);i++){
  ledger.assertHeadroom(slug, 0.25, env);
  const r=await fetch(`https://generativelanguage.googleapis.com/v1beta/models/${env.KIDS_IMAGE_MODEL}:generateContent`,{
    method:'POST',
    headers:{'x-goog-api-key':env.GEMINI_API_KEY,'Content-Type':'application/json'},
    body:JSON.stringify({contents:[{parts:refParts.concat([{text:prompt}])}],
      generationConfig:{responseModalities:['IMAGE'],imageConfig:{aspectRatio:aspect,imageSize:size}}}),
  });
  const j=await r.json();
  if(!r.ok){console.error(`  ${i}: ${r.status} ${JSON.stringify(j).slice(0,400)}`);continue;}
  const p=(j.candidates?.[0]?.content?.parts??[]).find(x=>x.inlineData);
  if(!p){console.error(`  ${i}: no image`);continue;}
  const f=path.join(outDir,`${outName}-${String(i).padStart(2,'0')}.jpg`);
  fs.writeFileSync(f,Buffer.from(p.inlineData.data,'base64'));
  const u=j.usageMetadata??{};
  const cost=((u.candidatesTokenCount??u.totalTokenCount-(u.promptTokenCount??0))/1e6)*60;
  spend+=cost;
  ledger.record(`cover: ${outName}-${i}`, cost, { book: slug });
  console.log(`  ${path.basename(f)}  $${cost.toFixed(4)}`);
}
console.log(`  this run $${spend.toFixed(4)} — ${ledger.report(slug, env)}`);
