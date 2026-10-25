import test from 'node:test';
import assert from 'node:assert/strict';
import { isValidSignupPhone } from '../src/lib/phoneNumber.js';
import { signupStateOptions, ABROAD_STATE } from '../src/data/medicalColleges.js';

test('signup accepts exactly ten ASCII digits, not country codes or formatted numbers', () => {
  assert.equal(isValidSignupPhone('9876543210'), true);
  for (const value of ['', '987654321', '98765432101', '+919876543210', '98765 43210', '987654321a', 9876543210, null]) {
    assert.equal(isValidSignupPhone(value), false, String(value));
  }
});
test('Abroad is the first signup location, without duplicate states', () => {
  assert.equal(signupStateOptions[0], ABROAD_STATE);
  assert.equal(new Set(signupStateOptions).size, signupStateOptions.length);
});
