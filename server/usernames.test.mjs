import test from 'node:test';
import assert from 'node:assert/strict';
import { reconcileUsernames, requireAvailableUsername, assertUniqueUsernames, validateUsername } from './usernames.mjs';

test('legacy names become unique usernames without taking another existing name', () => {
  const data = { users: ['Alex', ' alex ', 'Alex_2', 'ALEX', 'Sam'].map((name, id) => ({ id, name, attemptedQuestions: 12 })) };
  assert.equal(reconcileUsernames(data), true);
  assert.deepEqual(data.users.map(user => user.username), ['Alex', 'alex_3', 'Alex_2', 'ALEX_4', 'Sam']);
  assert.equal(data.users[1].previousName, ' alex ');
  assert.equal(data.users[1].attemptedQuestions, 12);
  assertUniqueUsernames(data);
  assert.equal(reconcileUsernames(data), false);
});

test('signup rejects obvious gibberish while allowing names and multilingual handles', () => {
  for (const name of ['qwerty', 'asdfgh123', 'zxcvbnm', 'abcd', 'aaaaaa', 'ababab', 'xjksdf', '123456', '!!!', 'a', 'a'.repeat(41), 'Alex\nSmith']) {
    assert.ok(validateUsername(name), name);
    assert.throws(() => requireAvailableUsername([], name), { status: 400 }, name);
  }
  for (const name of ['Dhruv', 'Li', 'Dr. A.P. Singh', 'Anne-Marie', "O’Connor", 'med_student2026', 'Srinivasan', 'Rhythm', 'श्रुति', 'محمد', '李明']) {
    assert.equal(validateUsername(name), null, name);
    requireAvailableUsername([], name);
  }
});

test('availability rejects case, whitespace and compatibility equivalents but allows own name', () => {
  const users = [{ id: 'one', username: 'Alex Smith' }];
  for (const name of ['alex smith', ' ALEX  SMITH ', 'Ａlex Smith']) {
    assert.throws(() => requireAvailableUsername(users, name), /already taken/);
  }
  requireAvailableUsername(users, 'ALEX Smith', 'one');
  requireAvailableUsername(users, 'Alex Smith_2');
  for (const name of ['', '  ', 'a'.repeat(255), 'alex\u200b']) {
    assert.throws(() => requireAvailableUsername(users, name), /Enter a username/);
  }
});
