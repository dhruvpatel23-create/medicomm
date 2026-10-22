import test from 'node:test';
import assert from 'node:assert/strict';
import { EventEmitter } from 'node:events';
import { createPracticeLive } from './practiceLive.mjs';
import { recordPracticeAttempt } from './dashboard.mjs';
import { createStateStore } from './stateStore.mjs';

function fixture() {
  const store = createStateStore({ initial: { users: [{ id: 'one', rating: 1480 }, { id: 'two', rating: 1480 }], practiceResults: [] }, persist: async () => {} });
  const live = createPracticeLive({ readDatabase: store.read,
    getSessionUser: (req, db) => req.revoked ? null : db.users.find(u => u.id === req.userId), sanitizeUser: u => u });
  function connect(userId) {
    const req = { userId }, res = new EventEmitter();
    res.frames = []; res.writeHead = (status, headers) => { res.headers = headers; };
    res.write = frame => { res.frames.push(frame); return true; };
    res.end = () => { res.ended = true; res.emit('close'); };
    live.connect(req, res, { id: userId });
    return { req, res, last: () => JSON.parse(res.frames.at(-1).split('data: ')[1]) };
  }
  return { store, live, connect };
}
const question = { id: 'q1', options: ['A', 'B'], answer: 'A' }, subject = { id: 's1', title: 'Subject' };
const payload = { id: 'attempt-0001', selectedAnswer: 'A', mode: 'pyq' };

test('committed first success reaches both account streams immediately and stays private', async () => {
  const { store, live, connect } = fixture();
  const a = connect('one'), b = connect('one'), other = connect('two');
  assert.equal(a.res.headers['Content-Type'], 'text/event-stream');
  const db = store.read(); recordPracticeAttempt(db, 'one', payload, subject, question);
  assert.equal(a.last().user.rating, 1480, 'uncommitted result is not broadcast');
  await store.write(db); live.publish(store.read());
  for (const client of [a, b]) {
    assert.equal(client.last().user.rating, 1481);
    assert.equal(client.last().progress.q1.firstAttemptCorrect, true);
  }
  assert.equal(other.res.frames.length, 1);
  assert.deepEqual(other.last().progress, {});
  const retry = store.read(); recordPracticeAttempt(retry, 'one', payload, subject, question);
  await store.write(retry); live.publish(store.read());
  assert.equal(a.res.frames.length, 2, 'duplicate delivery does not emit another rating gain');
  const reconnect = connect('one'); assert.equal(reconnect.last().user.rating, 1481);
  for (const client of [a, b, other, reconnect]) client.res.end();
});

test('wrong then right stays unmarked and revoked sessions stop receiving events', async () => {
  const { store, live, connect } = fixture(); const client = connect('one');
  for (const [id, answer] of [['attempt-0001', 'B'], ['attempt-0002', 'A']]) {
    const db = store.read(); recordPracticeAttempt(db, 'one', { ...payload, id, selectedAnswer: answer }, subject, question);
    await store.write(db); live.publish(store.read());
  }
  assert.equal(client.last().user.rating, 1480);
  assert.equal(client.last().progress.q1.firstAttemptCorrect, false);
  client.req.revoked = true; live.publish(store.read());
  assert.equal(client.res.ended, true);
});

test('a slow connection pauses updates without dropping a large first snapshot', async () => {
  const { store, live, connect } = fixture(); const client = connect('one');
  client.res.write = frame => { client.res.frames.push(frame); return false; };
  const db = store.read(); recordPracticeAttempt(db, 'one', payload, subject, question);
  await store.write(db); live.publish(store.read());
  assert.equal(client.res.ended, undefined);
  const next = store.read(); recordPracticeAttempt(next, 'one', { ...payload, id: 'attempt-0002' }, subject, { ...question, id: 'q2' });
  await store.write(next); live.publish(store.read());
  assert.equal(client.res.frames.length, 2);
  client.res.emit('drain'); live.publish(store.read());
  assert.equal(client.last().user.rating, 1482);
  client.res.end();
});
