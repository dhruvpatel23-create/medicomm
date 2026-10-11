import fs from 'fs';

const qb = JSON.parse(fs.readFileSync('data/practice-question-bank.json', 'utf8'));
const oph = qb.subjects.find(s => s.id === 'ophthalmology');
const targetYears = ['2017', '2018', '2019'];

const selected = oph.questions.filter(q => {
  const y = String(q.year || q.examYear || '');
  return targetYears.includes(y) && ((q.images && q.images.length > 0) || (q.imageUrls && q.imageUrls.length > 0) || q.imageUrl);
});

console.log(`Total questions: ${selected.length}`);
const summary = selected.map((q, idx) => ({
  index: idx + 1,
  id: q.id,
  year: q.year,
  examId: q.examId,
  prompt: q.prompt,
  options: q.options,
  answer: q.answer,
  images: q.images,
  imageUrls: q.imageUrls,
  sourceImageUrls: q.sourceImageUrls,
  atlasImageTargetUrls: q.atlasImageTargetUrls,
  assetNote: q.assetNote,
  explanation: q.explanation
}));

fs.writeFileSync('scripts/oph_2017_2019_extracted.json', JSON.stringify(summary, null, 2));
console.log('Saved to scripts/oph_2017_2019_extracted.json');
