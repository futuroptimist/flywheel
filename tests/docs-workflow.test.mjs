import { readFileSync } from 'node:fs';
import { test, expect } from '@jest/globals';

const workflow = readFileSync(new URL('../.github/workflows/03-docs.yml', import.meta.url), 'utf8');

test('docs workflow uses typos action', () => {
  expect(workflow).toMatch(/crate-ci\/typos@v1/);
});
