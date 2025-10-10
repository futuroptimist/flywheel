import { readFileSync } from 'node:fs';
import { test, expect } from '@jest/globals';

const workflow = readFileSync(
  new URL('../.github/workflows/02-tests.yml', import.meta.url),
  'utf8'
);

test('JS workflow installs lightweight webapp deps', () => {
  expect(workflow).toMatch(/webapp\/requirements-playwright\.txt/);
});
