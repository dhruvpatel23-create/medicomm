import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, writeFileSync, existsSync, unlinkSync, rmdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { acquireDevLock } from '../scripts/dev-lock.mjs';

function fixture(t) {
  const directory = mkdtempSync(path.join(tmpdir(), 'medulla-dev-lock-'));
  const file = path.join(directory, 'dev.lock');
  t.after(() => { if (existsSync(file)) unlinkSync(file); rmdirSync(directory); });
  return file;
}

test('a second launcher cannot start while the first owns the lock, even before its port opens', t => {
  const file = fixture(t);
  const release = acquireDevLock(file, { pid: 101, alive: () => true });
  assert.equal(typeof release, 'function');
  assert.equal(acquireDevLock(file, { pid: 102, alive: () => true }), null);
  release();
  assert.equal(existsSync(file), false);
  acquireDevLock(file, { pid: 102 })();
});

test('a crashed launcher lock is recovered without disturbing a live launcher', t => {
  const file = fixture(t);
  writeFileSync(file, '101');
  const release = acquireDevLock(file, { pid: 102, alive: () => false });
  assert.equal(readFileSync(file, 'utf8'), '102');
  release();
  writeFileSync(file, '');
  assert.equal(acquireDevLock(file, { pid: 103 }), null, 'a launcher writing its PID is left alone');
});

test('cleanup never removes a lock now owned by a different launcher', t => {
  const file = fixture(t);
  const release = acquireDevLock(file, { pid: 101 });
  writeFileSync(file, '102');
  release();
  assert.equal(readFileSync(file, 'utf8'), '102');
});
