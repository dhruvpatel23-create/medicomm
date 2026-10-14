import test from 'node:test';
import assert from 'node:assert/strict';
import { createShortNotesHandler, ownsTheoryAnswerImage } from './shortNotes.mjs';

const png = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aWQAAAABJRU5ErkJggg==';
function fixture() {
  let db = { shortNoteReviews: [{ userId: 'other', questionId: 'q', answer: 'Private', answerPages: [{ imagePath: 'other.png' }] }] };
  const files = new Map();
  let evaluationInput, failure = '', sequence = 0;
  const handler = createShortNotesHandler({
    questions: new Map([['q', { id: 'q', kind: 'short-note', subjectTitle: 'Anatomy', prompt: 'Heart' }]]),
    readDatabase: () => structuredClone(db),
    writeDatabase: async value => {
      if (failure === 'write') throw new Error('Storage unavailable');
      db = value;
      if (failure === 'uncertain-write') throw new Error('Interrupted after commit');
    },
    requireSessionUser: (req, res) => { if (!req.user) { res.status = 401; return null; } return { id: req.user }; },
    parseRequestBody: async req => req.body,
    sendJson: (res, status, body) => Object.assign(res, { status, body }),
    parseAnswerImage: value => value ? { mimeType: 'image/png', data: value.split(',')[1] } : null,
    saveAnswerImage: async data => {
      if (failure === 'upload' && files.size) throw new Error('Upload failed');
      const name = `page-${++sequence}.png`; files.set(name, data); return name;
    },
    removeAnswerImage: async name => files.delete(name),
    evaluate: async input => { evaluationInput = input; if (failure === 'ai') throw new Error('AI unavailable'); return { score: 8, feedback: 'Good answer.', modelAnswerSections: [] }; },
  });
  return { files, get db() { return db; }, get input() { return evaluationInput; }, fail: value => { failure = value; },
    async request(method = 'GET', body = {}, user = 'learner', query = '') {
      const response = {}; await handler({ method, body, user, url: `/api/short-notes/reviews${query}` }, response); return response;
    } };
}
const submission = { questionId: 'q', privacyAccepted: true, answer: 'My original answer', answerPages: [
  { dataUrl: png, source: 'notepad', name: 'Notepad page 1' }, { dataUrl: png, source: 'upload', name: 'Photo page 2' },
] };

test('saved library preserves ordered pages and earlier attempts with owner-only access', async () => {
  const f = fixture();
  assert.equal((await f.request('GET', {}, null)).status, 401);
  const first = await f.request('POST', submission);
  assert.equal(first.status, 201);
  assert.equal(first.body.review.answerPages.length, 2);
  assert.deepEqual(first.body.review.answerPages.map(page => page.source), ['notepad', 'upload']);
  assert.equal(f.input.studentAnswerImages.length, 2);
  assert(!JSON.stringify(first.body).includes('base64'));
  assert(!('userId' in first.body.review));
  const image = f.db.shortNoteReviews[0].answerPages[0].imagePath;
  assert(ownsTheoryAnswerImage(f.db, 'learner', image));
  assert(!ownsTheoryAnswerImage(f.db, 'other', image));
  const second = await f.request('POST', { questionId: 'q', privacyAccepted: true, answer: 'Second attempt' });
  assert.equal(second.body.review.attemptCount, 2);
  assert.notEqual(first.body.review.id, second.body.review.id);
  const list = (await f.request()).body.reviews;
  assert.equal(list.length, 1); assert.equal(list[0].answer, 'Second attempt');
  const history = (await f.request('GET', {}, 'learner', '?questionId=q')).body.reviews;
  assert.equal(history.length, 2); assert.equal(history[1].answer, 'My original answer');
  assert.equal(history[1].answerPages[0].imageUrl, `/uploads/${image}`);
  assert.equal((await f.request('GET', {}, 'other', '?questionId=q')).body.reviews.length, 1);
  assert.equal(f.files.size, 2);
});

test('failed uploads, AI and writes retain previous answers and clean unreferenced pages', async () => {
  for (const failure of ['upload', 'ai', 'write']) {
    const f = fixture(); f.fail(failure);
    assert.equal((await f.request('POST', submission)).status, 502);
    assert.equal(f.files.size, 0, failure);
    assert.equal(f.db.shortNoteReviews.length, 1);
    f.fail(''); assert.equal((await f.request('POST', submission)).status, 201);
  }
});

test('an interrupted write response never deletes images that committed', async () => {
  const f = fixture(); f.fail('uncertain-write');
  assert.equal((await f.request('POST', submission)).status, 502);
  assert.equal(f.files.size, 2);
  assert.equal((await f.request()).body.reviews[0].answerPages.length, 2);
});

test('invalid pages are rejected before storage and legacy image submissions still save', async () => {
  const f = fixture();
  for (const answerPages of [{}, Array(9).fill({ dataUrl: png }), [{ dataUrl: '' }], [{ dataUrl: 'data:image/png;base64,YmFk' }]]) {
    assert.equal((await f.request('POST', { ...submission, answerPages })).status, 400);
    assert.equal(f.files.size, 0);
  }
  assert.equal((await f.request('POST', { ...submission, privacyAccepted: false })).status, 400);
  const legacy = await f.request('POST', { questionId: 'q', privacyAccepted: true, answerImageDataUrl: png });
  assert.equal(legacy.status, 201); assert.equal(legacy.body.review.answerPages.length, 1);
});
