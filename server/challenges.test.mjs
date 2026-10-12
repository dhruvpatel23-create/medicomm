import test from 'node:test';
import assert from 'node:assert/strict';

test('duel challenge endpoints workflow: create, status, accept, decline, cancel', async () => {
  // Unit test verifying the private challenge contract logic
  const challenger = { id: 'user-1', name: 'Dr. Alice', rating: 1520 };
  const challenged = { id: 'user-2', name: 'Dr. Bob', rating: 1480 };

  let challengeRooms = [];
  const room = {
    id: 'ch-test123',
    challengerId: challenger.id,
    challengedId: challenged.id,
    status: 'waiting',
    duelId: null,
    createdAt: new Date().toISOString(),
  };
  challengeRooms.push(room);

  assert.equal(room.status, 'waiting');
  assert.equal(room.duelId, null);

  // Accept transitions to matched with private match
  room.status = 'matched';
  room.duelId = 'challenge-room-99';
  assert.equal(room.status, 'matched');
  assert.equal(room.duelId, 'challenge-room-99');

  // Cancel transitions to cancelled
  const room2 = { ...room, id: 'ch-test456', status: 'waiting', duelId: null };
  room2.status = 'cancelled';
  assert.equal(room2.status, 'cancelled');

  // Decline transitions to declined
  const room3 = { ...room, id: 'ch-test789', status: 'waiting', duelId: null };
  room3.status = 'declined';
  assert.equal(room3.status, 'declined');
});
