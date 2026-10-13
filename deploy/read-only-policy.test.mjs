import test from 'node:test';
import assert from 'node:assert/strict';
import { isReadOnlyRequestAllowed } from '../services/common/dist/utils/readOnlyPolicy.js';

test('reader rejects every mutating method and sensitive configuration route', () => {
  for (const method of ['POST', 'PATCH', 'PUT', 'DELETE', 'HEAD']) {
    for (const path of ['/properties', '/rents/payment/id/term', '/emails', '/realms', '/templates']) {
      assert.equal(isReadOnlyRequestAllowed(method, path), false);
    }
  }
  for (const path of ['/realms', '/realms/id', '/emails', '/templates', '/appcredz', '/properties-evil']) {
    assert.equal(isReadOnlyRequestAllowed('GET', path), false);
  }
});
test('reader can inspect only enumerated rental resources', () => {
  for (const path of ['/properties', '/properties/id', '/tenants/id', '/leases', '/rents/2026/10', '/dashboard']) {
    assert.equal(isReadOnlyRequestAllowed('GET', path), true);
  }
});
