import fs from 'fs';

const list = JSON.parse(fs.readFileSync('scripts/oph_2017_2019_extracted.json', 'utf8'));
list.forEach(q => {
  console.log(`[${q.index}/27] ${q.id} (Year ${q.year})`);
  console.log(`  Source: ${q.images[0]}`);
  console.log(`  Prompt: ${q.prompt.replace(/\s+/g, ' ')}`);
  console.log(`  Options: ${JSON.stringify(q.options)}`);
  console.log(`  Answer: ${q.answer}`);
  console.log(`  Explanation: ${(q.explanation || '').slice(0, 150).replace(/\s+/g, ' ')}`);
  console.log('--------------------------------------------------');
});
