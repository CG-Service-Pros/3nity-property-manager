import test from 'node:test';
import assert from 'node:assert/strict';
import { emailSendingEnabled } from '../services/emailer/src/sendingpolicy.js';

test('production does not override an explicit or default send prohibition', () => {
  for (const value of [undefined, 'false', '', '1', 'TRUE']) {
    assert.equal(emailSendingEnabled({NODE_ENV:'production', ALLOW_SENDING_EMAILS:value}), false);
  }
  assert.equal(emailSendingEnabled({NODE_ENV:'production', ALLOW_SENDING_EMAILS:'true'}), true);
});
