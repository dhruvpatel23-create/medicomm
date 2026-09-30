import test from 'node:test';
import assert from 'node:assert/strict';
import { validateSupabaseState } from './stateStore.mjs';

const validate = rows => validateSupabaseState(rows, 'app_state', 'medicomm');

test('startup distinguishes missing state, migration, and invalid revision', () => {
  assert.throws(() => validate([]), /No readable database row.*SUPABASE_STATE_KEY/);
  assert.throws(() => validate([{ data: {} }]), /Missing revision column/);
  for (const revision of [null, '0', -1, 0.5, Number.MAX_SAFE_INTEGER + 1]) {
    assert.throws(() => validate([{ data: {}, revision }]), /Invalid revision/);
  }
});

test('invalid responses and data cannot silently become empty user databases', () => {
  assert.throws(() => validate({}), /Invalid Supabase response/);
  for (const data of [null, [], 'invalid']) {
    assert.throws(() => validate([{ data, revision: 0 }]), /Invalid database data/);
  }
  assert.throws(() => validate([{ data: {}, revision: 0 }, { data: {}, revision: 1 }]), /Expected one database row/);
});

test('valid state retains existing data and revision', () => {
  const row = { data: { users: [{ id: 'existing-user' }] }, revision: 4 };
  assert.equal(validate([row]), row);
});
