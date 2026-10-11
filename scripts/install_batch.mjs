import fs from 'fs';
import path from 'path';
import crypto from 'crypto';

const ROOT = 'd:/medullaprep/dhruv1';
const BATCH_DIR = path.join(ROOT, 'output/imagegen/ophthalmology-2017-2019-img1');
const REVIEWED_FILE = path.join(BATCH_DIR, 'reviewed-images.json');

const items = JSON.parse(fs.readFileSync(REVIEWED_FILE, 'utf8'));
console.log(`Loaded ${items.length} items from reviewed-images.json`);

if (items.length !== 27) {
  throw new Error(`Expected 27 items, got ${items.length}`);
}

const stamp = new Date().toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
const backupDir = path.join(BATCH_DIR, 'backups', stamp);
fs.mkdirSync(backupDir, { recursive: true });

const bankPaths = [
  path.join(ROOT, 'data/practice-question-bank.json'),
  path.join(ROOT, 'public/practice-question-bank.json'),
  path.join(ROOT, 'dist/practice-question-bank.json')
];

// 1. Create backups of question banks
bankPaths.forEach(bp => {
  const destBackup = path.join(backupDir, `${path.basename(path.dirname(bp))}-practice-question-bank.json`);
  fs.copyFileSync(bp, destBackup);
  console.log(`Backed up ${bp} to ${destBackup}`);
});

// 2. Install images to all 4 upload directories
const uploadDirs = [
  path.join(ROOT, 'public/uploads'),
  path.join(ROOT, 'data/uploads'),
  path.join(ROOT, 'dist/uploads'),
  path.join(ROOT, 'runtime-data/uploads')
];

uploadDirs.forEach(dir => fs.mkdirSync(dir, { recursive: true }));

items.forEach(item => {
  const srcPng = path.join(BATCH_DIR, item.filename);
  const data = fs.readFileSync(srcPng);
  const hash = crypto.createHash('sha256').update(data).digest('hex');
  item.sha256 = hash;
  item.targetUrl = `/uploads/${item.filename}`;
  const atlasAlias = item.filename.replace('medicomm-img1-', 'medicomm-atlas-');

  uploadDirs.forEach(dir => {
    const dest1 = path.join(dir, item.filename);
    const dest2 = path.join(dir, atlasAlias);
    fs.writeFileSync(dest1, data);
    fs.writeFileSync(dest2, data);
  });
});
console.log('Installed images and atlas aliases across all 4 upload directories.');

// 3. Update question banks
const lookup = {};
items.forEach(i => { lookup[i.id] = i; });

bankPaths.forEach(bp => {
  console.log(`Updating bank: ${bp}`);
  const bank = JSON.parse(fs.readFileSync(bp, 'utf8'));
  let updatedCount = 0;
  
  bank.subjects.forEach(subject => {
    if (subject.questions) {
      subject.questions.forEach(q => {
        if (lookup[q.id]) {
          const item = lookup[q.id];
          const url = item.targetUrl;
          q.imageUrl = url;
          q.imageUrls = [url];
          q.images = [url];
          q.atlasImageTargetUrls = [url];
          q.assetNote = 'Original AI-generated Medicomm /img1 educational illustration (strictly copyright-safe, watermark-free); visually verified with source PYQ; no spoiler diagnostic labels.';
          updatedCount++;
        }
      });
    }
  });

  fs.writeFileSync(bp, JSON.stringify(bank, null, 2) + '\n', 'utf8');
  console.log(`Updated ${updatedCount} questions in ${bp}`);
});

// 4. Write installed-manifest.json
const manifest = {
  subject: 'ophthalmology',
  years: [2017, 2018, 2019],
  note: 'Complete /img1 replacement for all 27 Ophthalmology PYQ images across 2017, 2018, and 2019 (AIIMS & NEET-PG).',
  tool: 'built-in generate_image & precision clinical atlas illustration',
  watermark: 'None (strictly removed per /img1 prompt standard)',
  installedAt: stamp,
  images: items
};

fs.writeFileSync(path.join(BATCH_DIR, 'installed-manifest.json'), JSON.stringify(manifest, null, 2), 'utf8');
console.log('Successfully wrote installed-manifest.json');
