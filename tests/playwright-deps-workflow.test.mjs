import { readFileSync } from 'node:fs';
import { test, expect } from '@jest/globals';

const workflow = readFileSync(
  new URL('../.github/workflows/02-tests.yml', import.meta.url),
  'utf8'
);

test('JS workflow installs lightweight webapp deps', () => {
  expect(workflow).toMatch(/webapp\/requirements-playwright\.txt/);
});

test('test matrix uses a runner supported by Playwright 1.56', () => {
  expect(workflow).toMatch(/^ {4}runs-on: ubuntu-24\.04$/m);
});
