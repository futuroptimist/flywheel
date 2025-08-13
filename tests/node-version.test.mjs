import { test, expect } from '@jest/globals';

function parseMajor(version) {
  return Number(version.split('.')[0]);
}

test('Node.js major version is at least 20', () => {
  const major = parseMajor(process.versions.node);
  expect(major).toBeGreaterThanOrEqual(20);
});
